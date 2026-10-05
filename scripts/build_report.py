"""Render agent-reviewed robots.txt findings. No network or MCP calls."""
import argparse
import json
import math
import re
from datetime import date
from pathlib import Path

CHECK_IDS = {f"10.{i}" for i in range(1, 8)}
SHEETS = {
    "Checklist": (["Check", "Result", "Findings", "Coverage"], ["check", "result", "findings", "coverage"]),
    "Issues": (["Issue", "Issue Description", "How to Fix", "Address"], ["issue", "description", "how_to_fix", "address"]),
}


def report_filename(site_name, audit_date):
    if not isinstance(site_name, str) or not site_name.strip():
        raise ValueError("site name is required")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", audit_date):
        raise ValueError("audit date must use YYYY-MM-DD")
    date.fromisoformat(audit_date)
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", site_name.strip()).strip(" .")
    if not name:
        raise ValueError("site name contains no usable filename characters")
    return f"{name}_robots_audit_{audit_date}.xlsx"


def required_text(row, fields):
    for field in fields:
        if not isinstance(row.get(field), str) or not row[field].strip():
            raise ValueError(f"Missing/non-string {field}")
        if len(row[field]) > 32767:
            raise ValueError(f"{field} exceeds Excel cell limit; split issue groups")


def normalize(data):
    if "overview" in data:
        raise ValueError("Legacy schema: migrate to checklist/issues with separate description and fix")
    checks, issues = data.get("checklist"), data.get("issues")
    if not isinstance(checks, list) or not checks or not isinstance(issues, list):
        raise ValueError("Non-empty checklist and issues list required")
    ids = {}
    for source in checks:
        row = dict(source)
        required_text(row, ["id", "check", "findings", "coverage"])
        if row["id"] not in CHECK_IDS or row["id"] in ids:
            raise ValueError("Unknown/duplicate check ID")
        if row.get("result") not in {"Yes", "No", "NA", ""}:
            raise ValueError("Result must be Yes, No, NA or blank")
        reason_field = "na_reason" if row["result"] == "NA" else "unresolved_reason" if row["result"] == "" else None
        if reason_field:
            required_text(row, [reason_field])
            if row[reason_field] not in row["findings"]:
                row["findings"] += "\n" + row[reason_field]
        required_text(row, ["findings"])
        ids[row["id"]] = row
    unique, linked = {}, set()
    for source in issues:
        row = dict(source)
        required_text(row, ["issue", "description", "how_to_fix"])
        refs = row.get("check_ids")
        if not isinstance(refs, list) or not refs or any(not isinstance(cid, str) or cid not in ids or ids[cid]["result"] != "No" for cid in refs):
            raise ValueError("Each issue must link only to included No checks")
        addresses = row.get("addresses")
        if not isinstance(addresses, list) or not addresses or any(not isinstance(url, str) or not re.match(r"^https?://[^\s/]+(?:/[^\s]*)?$", url) for url in addresses):
            raise ValueError("Issue addresses must be absolute HTTP(S) URLs")
        row["address"] = "\n".join(dict.fromkeys(addresses))
        required_text(row, ["address"])
        identity = tuple(row[field] for field in ["issue", "description", "how_to_fix", "address"])
        unique[identity] = row
        linked.update(refs)
    if {cid for cid, row in ids.items() if row["result"] == "No"} != linked:
        raise ValueError("Every No requires an Issues row")
    return sorted(ids.values(), key=lambda r: tuple(map(int, r["id"].split(".")))), list(unique.values())


def build(data, output):
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation
    checklist, issues = normalize(data)
    output = Path(output)
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite {output}; select a new path")
    output.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    wb.remove(wb.active)
    datasets = {"Checklist": checklist, "Issues": issues}
    widths = {"Checklist": [64, 12, 90, 64], "Issues": [42, 90, 80, 90]}
    for title, (headers, fields) in SHEETS.items():
        sheet = wb.create_sheet(title)
        sheet.append(headers)
        for row in datasets[title]:
            sheet.append([row[field] for field in fields])
        sheet.freeze_panes = "A2"
        sheet.auto_filter.ref = sheet.dimensions
        sheet.row_dimensions[1].height = 25
        for cell in sheet[1]:
            cell.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="2F75B5")
        for j, width in enumerate(widths[title], 1):
            sheet.column_dimensions[sheet.cell(1, j).column_letter].width = width
        for excel_row in sheet.iter_rows(min_row=2):
            line_count = 1
            for j, cell in enumerate(excel_row):
                cell.font = Font(name="Calibri", size=11)
                cell.alignment = Alignment(vertical="top", wrap_text=True)
                if isinstance(cell.value, str):
                    cell.data_type = "s"
                    cell.number_format = "@"
                    line_count = max(line_count, sum(max(1, math.ceil(len(part) / max(1, widths[title][j] // 2))) for part in cell.value.split("\n")))
                    if "\n" not in cell.value and cell.value.startswith(("https://", "http://")):
                        cell.hyperlink = cell.value
                        cell.font = Font(name="Calibri", size=11, color="0563C1", underline="single")
            sheet.row_dimensions[excel_row[0].row].height = min(409, max(30, line_count * 16 + 8))
            if title == "Checklist":
                color = {"No": "FCE4D6", "NA": "E7E6E6", "": "FFF2CC"}.get(excel_row[1].value)
                if color:
                    excel_row[1].fill = PatternFill("solid", fgColor=color)
        if title == "Checklist":
            validation = DataValidation(type="list", formula1='"Yes,No,NA"', allow_blank=True)
            validation.showErrorMessage = True
            sheet.add_data_validation(validation)
            validation.add(f"B2:B{sheet.max_row}")
    wb.save(output)
    verified = load_workbook(output)
    try:
        if verified.sheetnames != list(SHEETS):
            raise RuntimeError("Workbook sheet verification failed")
        for title, (headers, fields) in SHEETS.items():
            sheet = verified[title]
            if [c.value for c in sheet[1]] != headers or sheet.max_row != len(datasets[title]) + 1:
                raise RuntimeError(f"Workbook header/count verification failed: {title}")
            for i, source in enumerate(datasets[title], 2):
                if [sheet.cell(i, j).value or "" for j in range(1, 5)] != [source[f] for f in fields]:
                    raise RuntimeError("Workbook value preservation failed")
    finally:
        verified.close()
    return {"output": str(output.resolve()), "checks": len(checklist), "issues": len(issues)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--site-name", required=True)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD in the user's timezone")
    args = parser.parse_args()
    print(json.dumps(build(json.loads(args.input.read_text(encoding="utf-8-sig")), args.output_dir / report_filename(args.site_name, args.date)), ensure_ascii=False))
