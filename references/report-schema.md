# Report and evidence contract

Agent-reviewed decisions go into findings.json; raw exports alone are not a report. Map actual export headers and preserve provenance. Delivered workbook has exactly two sheets:

| Sheet | Columns |
| --- | --- |
| Checklist | Check; Result; Findings; Coverage |
| 10. Robot.txt | Issue; Issue Description; How to Fix; Address |

The second sheet contains only confirmed defects linked to No. Human Check details belong exclusively in Checklist Findings/Coverage and supporting evidence/handover, never as rows in 10. Robot.txt. Keep the defect sheet headers when there are no confirmed issues.

```json
{
  "requested_checks": ["10.1", "10.5"],
  "checklist": [
    {"id":"10.1","check":"10.1 Does a robots.txt document exist?","result":"No","findings":"robots.txt 返回 200，但内容为空。","findings_bold":["内容为空"],"coverage":"检查主站 /robots.txt；保存原始内容。"},
    {"id":"10.5","check":"10.5 Are special pages handled appropriately?","result":"Human Check","findings":"Human Check：尚未确认这些页面的用途，以及是否设有需要的抓取、收录或登录限制。","human_check_reason":"尚未确认这些页面的用途，以及是否设有需要的抓取、收录或登录限制。","human_check_action":"查看这些页面的公开内容，确认用途及相应限制；不要登录私人账户或提交订单。","coverage":"已读取 robots 和已有 crawl，整理特殊页候选；候选页面未验证，未执行交易或登录。"}
  ],
  "issues": [
    {"check_ids":["10.1"],"kind":"defect","issue":"Empty robots.txt","description":"robots.txt 可访问，但未包含有效指令。按约定 audit 标准判为配置问题，不代表安全漏洞。","how_to_fix":"核实网站需求后配置合适规则，保留重要页面及必要资源的抓取权限。","addresses":["https://example.com/robots.txt"]}
  ],
  "evidence_gaps": [{"check":"10.5","missing":"尚未确认这些页面的用途，以及是否设有需要的抓取、收录或登录限制。","next_action":"查看这些页面的公开内容，确认用途及相应限制；不要登录私人账户或提交订单。"}]
}
```

Include every requested check exactly once; requested_checks defaults to all seven. Narrow the list only for an explicitly partial request. Results are Yes/No/NA/Human Check, never blank. Unknown evidence is Human Check, not NA/Yes/No. Always deliver final Excel without waiting for unresolved evidence. The builder validates structure, not substantive claims.

Every Human Check requires human_check_reason. Findings records a concise conclusion, specific cause/gap and necessary next action (normally one to three short lines). Coverage exclusively records sources, counts, sampling, already-checked evidence, verified versus unresolved scope and exclusions. Do not duplicate Coverage in Findings; keep full evidence in the supporting files rather than repeating URL inventories. Supply human_check_action for a precise action in the requested report language; absent action uses the per-check default. There is no requirement for a linked review issue. A confirmed No with additional gaps retains its defect row and records Human Check details only in its Checklist Findings.

Every No requires at least one confirmed defect in issues linked through check_ids; kind defaults to defect. Defects link only to No. NA requires na_reason visible in Findings and has no defect row. Each evidence_gaps item requires check, missing and next_action, referring to a No or Human Check Checklist row; its details are appended to Findings without requiring any issue. No extra Excel columns are added by internal fields.

Compatibility: old kind=human_check issue objects are accepted only when linked to Human Check or No. Their description and manual action migrate into Checklist Findings; addresses migrate into Checklist Coverage; they are excluded from the normalized defect list and the delivered defect sheet. They cannot substitute for a confirmed defect linked to No. New input should put review details in Checklist/evidence_gaps, not issues.

Defects group only identical cause/action. Description includes observations and supported impact; How to Fix contains actual repair or justified further-validation recommendations. addresses lists full known URLs, deduplicated and one per line. Label unverified candidates; do not invent verified pages or exposure. Keep every affected page for shared blocked resources. Preserve actual relationships in raw evidence. Do not manufacture ranking/index-status claims.

## Partial progress delivery completion

Use build_report.py --site-url <actual audited URL> --prepared-input <new findings-delivery.json path> when the current evidence pass ends. It completes missing requested rows as Human Check and fills reason/action details in Checklist, without generating review issues. A gap attached to provisional Yes/NA changes it to Human Check; No remains No with its confirmed defect and Checklist gap details. Archive/review/translate the completed input. A fresh path is required; prior files are not overwritten. Invalid IDs/schema or No without its confirmed defect remain errors to correct, not reasons to omit checks. See [delivery boundaries](delivery-boundaries.md).

## Run archive

```text
<run_root>/<run_id>/
  config.json
  manifest.json       source crawl, time, settings, field mapping, hashes/counts
  usage.json          cumulative requests/MCP calls/retries
  raw/                robots responses and sitemap/crawl/directive/resource exports
  candidates-<origin-hash>.txt
  robots-<origin-hash>.json
  inventory/          URL classifications and sample selection/exclusions
  evidence_gaps.json
  findings.json
  findings-delivery.json
  {site name}_robots_audit_{YYYY-MM-DD}.xlsx
  handover.md
  sf-handover.json     optional preparation record, not audit completeness
```

Preserve original crawl time, incomplete exports, missing material fields and actual settings. Shared usage is cumulative. No client data or machine-local settings are committed. Website 429 and MCP/tool 429 remain distinct with source, Retry-After and affected coverage.

10.2 NA reasons are confirmed absent robots or explicit user waiver; missing page subtypes do not establish NA. For 10.3 record site nature, evidence and selected/excluded families with reasons; do not require cart/checkout on non-shopping sites. No-Disallow is an audit-standard configuration issue with site-appropriate further validation, not proof of private exposure.

Confirmed unused/inapplicable template directives belong in issues as kind=defect linked to 10.3 No and are exported to 10. Robot.txt. Checklist Findings must name the confirmed residual directives and briefly explain their inapplicability (not merely say "template issue"); Coverage records sources and discovery scope. Description records the exact groups/directives and the site evidence confirming they are unnecessary; How to Fix removes only those confirmed remnants and rechecks important URLs/resources. This is a configuration finding, not proof of private exposure or ranking harm. Unverified template purpose remains Human Check only in Checklist.

## Findings emphasis

Checklist Findings supports real Excel rich-text bold inside each cell. It automatically emphasizes labels such as 已检查、结论、缺少／失败、下一步动作、排除原因、Human Check, Already checked and Next action. For unstructured text it emphasizes a short leading sentence when available. An optional `findings_bold` array selects exact existing text phrases for key conclusions, blocked causes or exclusions. Example: `["缺少前台引用关系", "仅供登录页使用，已排除"]`, provided those phrases actually occur in findings. No new Excel column is added. Unmatched phrases have no effect; malformed arrays require input correction. Do not insert Markdown `**` markers or bold the entire cell. Text, URLs, line breaks, result values and confirmed-defect-only sheet behavior remain preserved. Reloading without rich-text support still returns the original plain Findings text.

## Plain-language Findings

Write for a client who does not know SEO or Screaming Frog. Lead with the current conclusion; explain its specific reason in familiar words. For Human Check, say what cannot yet be confirmed and what information/action will resolve it. Keep the Result values unchanged. Normally use one to three short sentences. Counts, sources, dates, sampling and checked/unchecked inventories belong in Coverage. Keep full technical proof in the evidence files or Issue Description.

Retain a path or directive when it identifies the problem, but explain what it does. Avoid unexplained SF, inlinks, effective permissions, applicable families, control evidence and "further validate". Do not replace precise limits with stronger claims: crawlable is not indexed; blocked is not broken; a login gate is not proof that all private functions are secure. Default script messages are English fallbacks; the agent must write/review Findings and follow-up actions in the requested report language before delivery.

Illustrative wording only; use each statement only when supported by the actual evidence:

| Situation | Plain-language Findings |
| --- | --- |
| 10.1 valid file | robots.txt 可以正常打开，包含有效的网站抓取设置。 |
| 10.2 checked pages allowed | robots.txt 没有阻止 Google 抓取本次检查的重要页面。 |
| 10.3 confirmed cart-rule remnant | 发现无用的购物车规则 `/*?add-to-cart=`：已确认本站没有购物功能，也不需要保留这条限制。 |
| 10.4 required public asset blocked | robots.txt 阻止 Google 读取首页需要的样式文件 `/assets/site.css`，可能影响页面显示。 |
| 10.4 source relationship unknown | 尚未确认这些文件是否被前台页面使用。请补充显示哪些页面使用这些文件的导出资料。 |
| 10.5 protected route verified | 本次检查的后台入口会先要求登录，未显示受保护内容。 |
| 10.6 valid lowercase endpoint | 小写地址 `/robots.txt` 可以正常打开。 |
| 10.7 declaration present | robots.txt 已列出网站地图链接。 |
| SF export incomplete | 导出资料不完整，暂时无法确认剩余页面是否被 robots.txt 阻挡。请补充这些页面的抓取权限结果。 |

Use selective Excel bold for the main conclusion or concrete problem, not the entire paragraph. These are writing examples, not fixed findings to paste without checking.
