"""Render agent-reviewed robots.txt findings. No network or MCP calls."""
import argparse
import copy
import json
import math
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

CHECK_IDS = {f"10.{i}" for i in range(1, 8)}
CHECK_NAMES = {
    '10.1': 'Does a robots.txt document exist?',
    '10.2': 'Are important pages allowed for Googlebot?',
    '10.3': 'Are appropriate crawl restrictions in place?',
    '10.4': 'Are required CSS and JS allowed?',
    '10.5': 'Are special pages handled appropriately?',
    '10.6': 'Is the lowercase robots.txt endpoint valid?',
    '10.7': 'Is a sitemap declared in robots.txt?',
}
REVIEW_ACTIONS = {
    '10.1': 'Verify the lowercase robots response and its actual text; record status and redirects.',
    '10.2': 'Complete the sitemap/fallback URL inventory and verify effective Googlebot permissions for unresolved URLs; retain already-checked results.',
    '10.3': 'Use actual site evidence to select applicable sample families and record exclusions; verify effective Googlebot rules and non-empty Disallow, then further validate relevant targets before adding restrictions. Do not require cart/checkout on non-shopping sites.',
    '10.4': 'Identify SF crawl/export errors or missing CSS/JS rows, relationships or permission results; obtain only the missing evidence and retain tested resources.',
    '10.5': 'Verify candidate purpose and the applicable control without logging in or submitting orders.',
    '10.6': 'Verify the lowercase endpoint; do not infer casing from an unknown server filename.',
    '10.7': 'Inspect the raw robots text for a valid absolute Sitemap declaration.',
}
SHEETS = {
    "Checklist": (["Check", "Result", "Findings", "Coverage"], ["check", "result", "findings", "coverage"]),
    "10. Robot.txt": (["Issue", "Issue Description", "How to Fix", "Address"], ["issue", "description", "how_to_fix", "address"]),
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


def complete_for_export(data, site_url):
    """Explicit delivery fallback, using the actual audited origin; never invent a pass.

    Strict normalize remains the final validator. Invalid IDs, unsupported results,
    and unsubstantiated No/defect associations are not silently repaired.
    """
    if not isinstance(data, dict) or not isinstance(site_url, str):
        raise ValueError('Completion requires a report object and actual site URL string')
    parsed = urlsplit(site_url)
    if parsed.scheme not in {'http', 'https'} or not parsed.hostname or parsed.username or parsed.password or any(c.isspace() for c in site_url):
        raise ValueError('site_url must be the actual absolute HTTP(S) audited URL without credentials')
    result = copy.deepcopy(data)
    if 'overview' in result:
        raise ValueError('Legacy schema must be migrated before completion')
    requested = result.get('requested_checks', sorted(CHECK_IDS))
    if not isinstance(requested, list) or not requested or any(not isinstance(cid, str) or cid not in CHECK_IDS for cid in requested) or len(set(requested)) != len(requested):
        raise ValueError('requested_checks must contain unique supported check IDs')
    rows = result.setdefault('checklist', [])
    issues = result.setdefault('issues', [])
    gaps = result.setdefault('evidence_gaps', [])
    if not all(isinstance(value, list) for value in (rows, issues, gaps)):
        raise ValueError('checklist, issues and evidence_gaps must be lists')
    ids = {}
    for row in rows:
        if not isinstance(row, dict) or row.get('id') not in requested or row['id'] in ids:
            raise ValueError('Unknown/duplicate/unrequested check ID')
        ids[row['id']] = row
    by_check = {}
    for gap in gaps:
        if not isinstance(gap, dict):
            raise ValueError('Each evidence gap must be an object')
        required_text(gap, ['check', 'missing', 'next_action'])
        if gap['check'] not in requested:
            raise ValueError('Evidence gap references an unrequested check')
        by_check.setdefault(gap['check'], []).append(gap)
    for cid in requested:
        if cid not in ids:
            row = {'id': cid, 'check': cid + ' ' + CHECK_NAMES[cid], 'result': 'Human Check',
                   'findings': 'No agent-reviewed decision supplied for this requested check.',
                   'coverage': 'Not verified; no completed scope supplied.'}
            rows.append(row)
            ids[cid] = row
        row = ids[cid]
        check_gaps = by_check.get(cid, [])
        if check_gaps and row.get('result') in {'Yes', 'NA'}:
            row['findings'] = 'Earlier provisional result: ' + row['result'] + '.\n' + row.get('findings', '')
            row['result'] = 'Human Check'
        if row.get('result') != 'Human Check' and not (row.get('result') == 'No' and check_gaps):
            continue
        reason = '\n'.join(gap['missing'] for gap in check_gaps) or row.get('human_check_reason') or ('Required evidence for ' + cid + ' is incomplete; see the manual verification action.')
        if row['result'] == 'Human Check':
            row.setdefault('human_check_reason', reason)
            if not row['human_check_reason']:
                row['human_check_reason'] = reason
        action = '\n'.join(gap['next_action'] for gap in check_gaps) or REVIEW_ACTIONS[cid]
        row['human_check_action'] = action
    completed_rows, defects = normalize(result)
    result['checklist'] = completed_rows
    result['issues'] = defects
    return result


def normalize(data):
    if "overview" in data:
        raise ValueError("Legacy schema: migrate to checklist/issues with separate description and fix")
    gaps = data.get("evidence_gaps", [])
    if not isinstance(gaps, list):
        raise ValueError("evidence_gaps must be a list")
    requested = data.get("requested_checks", sorted(CHECK_IDS))
    if not isinstance(requested, list) or not requested or any(not isinstance(cid, str) or cid not in CHECK_IDS for cid in requested) or len(set(requested)) != len(requested):
        raise ValueError("requested_checks must contain unique supported check IDs")
    checks, issues = data.get("checklist"), data.get("issues")
    if not isinstance(checks, list) or not checks or not isinstance(issues, list):
        raise ValueError("Non-empty checklist and issues list required")
    ids = {}
    for source in checks:
        row = dict(source)
        required_text(row, ["id", "check", "findings", "coverage"])
        if row["id"] not in CHECK_IDS or row["id"] in ids:
            raise ValueError("Unknown/duplicate check ID")
        if row.get("result") not in {"Yes", "No", "NA", "Human Check"}:
            raise ValueError("Final Result must be Yes, No, NA or Human Check")
        reason_field = {"NA": "na_reason", "Human Check": "human_check_reason"}.get(row["result"])
        if reason_field:
            required_text(row, [reason_field])
            if row[reason_field] not in row["findings"]:
                row["findings"] += "\n" + row[reason_field]
        required_text(row, ["findings"])
        if row["result"] == "Human Check" and "Human Check" not in row["findings"]:
            row["findings"] = "Human Check: " + row["findings"]
        required_text(row, ["findings"])
        ids[row["id"]] = row
    if set(ids) != set(requested):
        raise ValueError("Final report must include every requested check; do not silently omit unresolved checks")
    unique, linked = {}, set()
    for source in issues:
        row = dict(source)
        required_text(row, ["issue", "description", "how_to_fix"])
        refs = row.get("check_ids")
        kind = row.get("kind", "defect")
        if kind not in {"defect", "human_check"}:
            raise ValueError("Issue kind must be defect or human_check")
        permitted = {"No"} if kind == "defect" else {"No", "Human Check"}
        if not isinstance(refs, list) or not refs or any(not isinstance(cid, str) or cid not in ids or ids[cid]["result"] not in permitted for cid in refs):
            raise ValueError("Defects link to No; human_check issues link to No or Human Check")
        if kind == "human_check":
            # Compatibility: move legacy review rows to Checklist, never the defect tab.
            marker = 'Human Check: ' + row['issue'] + '\n' + row['description'] + '\nNext action: ' + row['how_to_fix']
            addresses = row.get('addresses', [])
            if not isinstance(addresses, list) or any(not isinstance(url, str) for url in addresses):
                raise ValueError('Legacy review addresses must be a list of strings')
            if addresses:
                marker += '\nReview addresses: ' + '\n'.join(addresses)
            for cid in refs:
                if marker not in ids[cid]['findings']:
                    ids[cid]['findings'] += '\n' + marker
                required_text(ids[cid], ['findings'])
            continue
        linked.update(refs)
        required_text(row, ["issue"])
        addresses = row.get("addresses")
        if not isinstance(addresses, list) or not addresses or any(not isinstance(url, str) or not re.match(r"^https?://[^\s/]+(?:/[^\s]*)?$", url) for url in addresses):
            raise ValueError("Issue addresses must be absolute HTTP(S) URLs")
        row["address"] = "\n".join(dict.fromkeys(addresses))
        required_text(row, ["address"])
        identity = (kind,) + tuple(row[field] for field in ["issue", "description", "how_to_fix", "address"])
        if identity in unique:
            unique[identity]['check_ids'] = list(dict.fromkeys(unique[identity]['check_ids'] + refs))
        else:
            unique[identity] = row
    if {cid for cid, row in ids.items() if row["result"] == "No"} != linked:
        raise ValueError("Every No requires a confirmed-defect row in 10. Robot.txt")
    for gap in gaps:
        if not isinstance(gap, dict):
            raise ValueError("Each evidence gap must be an object")
        required_text(gap, ["check", "missing", "next_action"])
        cid = gap["check"]
        if cid not in ids or ids[cid]["result"] not in {"No", "Human Check"}:
            raise ValueError("Every evidence gap must reference a No or Human Check Checklist row")
        marker = "Human Check: " + gap["missing"] + "\n" + gap["next_action"]
        if marker not in ids[cid]["findings"]:
            ids[cid]["findings"] += "\n" + marker
        required_text(ids[cid], ["findings"])
    for cid, row in ids.items():
        if row['result'] == 'Human Check' or row.get('human_check_action'):
            action = row.get('human_check_action', REVIEW_ACTIONS[cid])
            required_text({'action': action}, ['action'])
            marker = 'Next action: ' + action
            if marker not in row['findings']:
                row['findings'] += '\n' + marker
            required_text(row, ['findings'])
    return sorted(ids.values(), key=lambda r: tuple(map(int, r["id"].split(".")))), list(unique.values())


def build(data, output, site_url=None):
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation
    if site_url is not None:
        data = complete_for_export(data, site_url)
    checklist, issues = normalize(data)
    output = Path(output)
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite {output}; select a new path")
    output.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    wb.remove(wb.active)
    datasets = {"Checklist": checklist, "10. Robot.txt": issues}
    widths = {"Checklist": [64, 14, 90, 64], "10. Robot.txt": [42, 90, 80, 90]}
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
                color = {"No": "FCE4D6", "NA": "E7E6E6", "Human Check": "FFF2CC"}.get(excel_row[1].value)
                if color:
                    excel_row[1].fill = PatternFill("solid", fgColor=color)
        if title == "Checklist":
            validation = DataValidation(type="list", formula1='"Yes,No,NA,Human Check"', allow_blank=False)
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
    parser.add_argument("--site-url", help="Actual audited URL: explicitly complete missing checks/review details in Checklist as Human Check")
    parser.add_argument("--prepared-input", type=Path, help="Archive completed report input to a new JSON path (requires --site-url)")
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8-sig"))
    if args.prepared_input and not args.site_url:
        parser.error('--prepared-input requires --site-url')
    if args.site_url:
        data = complete_for_export(data, args.site_url)
    output = args.output_dir / report_filename(args.site_name, args.date)
    if output.exists():
        raise FileExistsError(f'Refusing to overwrite {output}; select a new path')
    if args.prepared_input:
        args.prepared_input.parent.mkdir(parents=True, exist_ok=True)
        with args.prepared_input.open('x', encoding='utf-8') as stream:
            stream.write(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(build(data, output), ensure_ascii=False))
