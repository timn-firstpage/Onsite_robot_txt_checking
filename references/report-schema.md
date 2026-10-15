# Report and evidence contract

Agent-reviewed decisions go into findings.json. Deliver exactly two worksheets:

| Sheet | Columns |
| --- | --- |
| Checklist | Item No.; Item Name; Initial Check; Findings; Instruction |
| 10. Robot.txt | Issue; Issue Description; How to Fix; Address |

Item No. contains the check ID. Item Name contains the exact original English item name listed in SKILL.md, without an ID prefix. The JSON id/check fields remain compatible with existing inputs. Never paraphrase, shorten, correct grammar or translate these names. Report language applies to Findings, Instruction and issue explanations.

Result displays **√ / X / NA / Human Check**. √ means the check passes; X means a confirmed defect or failure of the agreed audit standard. For 10.2, √ means the important pages were not incorrectly blocked. Legacy JSON Yes/No remains accepted and is rendered as √/X; the normalizer uses Yes/No internally. NA and Human Check are never converted to √ or X.

## Findings and Instruction

- **Findings:** what was found and the short reason, normally one or two simple sentences. For Human Check, say what cannot yet be confirmed. Include any material limit needed to avoid an unsupported whole-site claim, but no long inventory or next-step list.
- **Instruction:** what a person needs to do next. Use a short, concrete verb-led sentence such as “请提供购物车页面地址。” or “请补充这些文件的引用页面。” Name the relevant page/file when needed. Avoid “进一步验证适用控制” or vague “优化配置”. Usually one sentence; multiple distinct required actions may use short separate lines. Passing/NA checks with no human action use `—`. Do not invent work just to fill the cell.
- **Coverage is not an Excel column.** Keep counts, source dates, tested/untested URLs and sampling details in raw evidence, manifest or optional internal coverage metadata. Do not move the old Coverage paragraph into Instruction.
- Keep findings_bold selective: key conclusion or exact problem only. Plain text input contains no Markdown bold markers; the builder writes real Excel rich text.

## Issue numbering

Only confirmed X defects go in `10. Robot.txt`; Human Check stays in Checklist. The Issue cell begins with the linked check number: `10.1 Missing robots.txt`, `10.3 Unused shopping cart rules`. The builder derives this prefix from check_ids. A shared cause linked to multiple checks is labelled with all relevant IDs, e.g. `10.1, 10.7 Empty robots.txt`, without duplicating the issue merely to add numbers. Existing prefixes are normalized, not repeated. No separate number column is added.

Issue Description explains the observed problem. How to Fix states the concise repair action. Address preserves affected full URLs and query strings. Keep both sheet headers even when no confirmed defects exist. Template remnants confirmed under 10.3 receive X: identify the specific residual rule and why it does not apply in Findings, then put cleanup in Instruction and the numbered issue row.

## Input example

Illustrative only; these are not customer findings.

```json
{
  "requested_checks": ["10.1", "10.4"],
  "checklist": [
    {"id":"10.1","check":"10.1 Does a robots.txt document exist?","result":"X","findings":"robots.txt 内容为空。","findings_bold":["内容为空"],"instruction":"请确认需要限制的页面，再补充对应规则。"},
    {"id":"10.4","check":"10.4 Are we allowing bot access to CSS and JS documents?","result":"Human Check","findings":"尚未确认哪些前台页面使用这些文件。","human_check_reason":"尚未确认哪些前台页面使用这些文件。","instruction":"请补充这些文件的引用页面。"}
  ],
  "issues": [
    {"check_ids":["10.1"],"kind":"defect","issue":"Empty robots.txt","description":"文件可以打开，但没有配置内容。按约定审核标准判为问题。","how_to_fix":"确认需要限制的页面，再补充对应规则。","addresses":["https://example.com/robots.txt"]}
  ],
  "evidence_gaps": [{"check":"10.4","missing":"尚未确认哪些前台页面使用这些文件。","next_action":"请补充这些文件的引用页面。"}]
}
```

Every requested check appears once; requested_checks defaults to all seven and is narrowed only for an explicitly partial request. Each X/legacy No requires a linked confirmed defect. NA requires na_reason; Human Check requires human_check_reason. Reasons belong in Findings, actions in Instruction. Unknown evidence is Human Check, not NA or a pass. The builder validates structure, not truth.

Instruction may be supplied directly. For compatibility, the builder moves explicitly labelled legacy Next action/下一步 lines from Findings into Instruction, accepts human_check_action, and collects evidence_gaps.next_action. Exact repeated actions appear once. If a failed check has no instruction, its linked How to Fix supplies a fallback; Human Check uses its per-check fallback. The agent must review/translate all fallback text into short plain language before delivery. Unlabelled mixed prose cannot be reliably separated by code: review it rather than guessing.

Legacy kind=human_check issue rows migrate their description to Findings, action to Instruction and addresses to internal evidence; they never appear in the defect sheet. Legacy coverage is optional and retained internally, never displayed. Keep original input/evidence for traceability.

## Partial delivery and archive

Always deliver all requested checks using current supported findings, even when more evidence is needed. Use `python scripts/build_report.py --site-url <actual audited URL> --prepared-input <new findings-delivery.json path>` with the remaining required CLI arguments to fill missing rows as Human Check. Gaps downgrade provisional √/Yes or NA to Human Check; confirmed X/No and its defect remain. Do not overwrite an old report. Runtime/write errors must be reported accurately rather than claiming a file exists.

Archive config, manifest, cumulative usage, raw responses/exports, URL inventory, evidence_gaps.json, original findings.json, prepared findings-delivery.json, final workbook and handover under the unique run directory. Retain evidence dates and scope. Do not commit customer files. Workbook name is `{item range}_{site name}_robots_audit_{YYYY-MM-DD}.xlsx`, using the user's timezone.

## Findings emphasis

Optional findings_bold is a list of exact existing phrases, e.g. `["内容为空"]`. Labels or a short leading conclusion may be emphasized automatically. Do not bold whole paragraphs or URL lists. Formula-like values remain text in every column, including Instruction. Plain-text workbook readers retain the wording.

## Plain-language Findings

| Situation | Findings | Instruction |
| --- | --- | --- |
| Valid robots file | robots.txt 可以正常打开，包含有效设置。 | — |
| Important pages allowed | robots.txt 没有阻止 Google 抓取本次检查的重要页面。 | — |
| Confirmed unused shopping rule | 发现无用的购物车规则 `/*?add-to-cart=`，本站已确认不需要这条限制。 | 请删除这条无用规则。 |
| Required public asset blocked | robots.txt 阻止 Google 读取首页需要的样式文件 `/assets/site.css`。 | 请允许 Google 抓取这个文件。 |
| Resource source unknown | 尚未确认哪些前台页面使用这些文件。 | 请补充这些文件的引用页面。 |
| Protected admin entry | 本次检查的后台入口会先要求登录。 | — |
| Lowercase endpoint valid | 小写地址 `/robots.txt` 可以正常打开。 | — |
| Sitemap declaration missing | robots.txt 没有网站地图链接。 | 请添加正确的 Sitemap 链接。 |

Use examples only when evidence supports them. Preserve distinctions between crawling, indexing, access protection and response health. No ranking claims without evidence. Instruction is a human action, not an explanation of how the agent works.

Filename prefix uses the lowest and highest item IDs actually included in the delivered Checklist, in numeric order, including NA and Human Check. Full robots reports use `10.1-10.7`; a single-item report uses just `10.4`. A range is a filename summary; the Checklist lists the exact included items for partial/non-contiguous requests. Example: `10.1-10.7_Example_robots_audit_2026-10-15.xlsx`.
