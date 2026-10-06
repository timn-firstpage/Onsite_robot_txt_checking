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
    {"id":"10.1","check":"10.1 Does a robots.txt document exist?","result":"No","findings":"robots.txt 返回 200，但内容为空。","coverage":"检查主站 /robots.txt；保存原始内容。"},
    {"id":"10.5","check":"10.5 Are special pages handled appropriately?","result":"Human Check","findings":"已检查：读取 robots 和已有 crawl，整理特殊页候选；尚未验证候选用途。","human_check_reason":"缺少候选响应、内容及适用控制证据。","human_check_action":"人工核对候选的响应、用途及适用控制，保存只读证据；不执行订单或私人账户登录。","coverage":"候选已准备，页面未验证；未执行交易或登录。"}
  ],
  "issues": [
    {"check_ids":["10.1"],"kind":"defect","issue":"Empty robots.txt","description":"robots.txt 可访问，但未包含有效指令。按约定 audit 标准判为配置问题，不代表安全漏洞。","how_to_fix":"核实网站需求后配置合适规则，保留重要页面及必要资源的抓取权限。","addresses":["https://example.com/robots.txt"]}
  ],
  "evidence_gaps": [{"check":"10.5","missing":"候选响应、内容及适用控制证据","next_action":"人工核对候选并保存响应／指令／用途证据。"}]
}
```

Include every requested check exactly once; requested_checks defaults to all seven. Narrow the list only for an explicitly partial request. Results are Yes/No/NA/Human Check, never blank. Unknown evidence is Human Check, not NA/Yes/No. Always deliver final Excel without waiting for unresolved evidence. The builder validates structure, not substantive claims.

Every Human Check requires human_check_reason. Findings records **Already checked**, **Missing/failed**, **Next action**; Coverage records actual sources/counts and verified versus unresolved scope. Supply human_check_action for a precise action in the requested report language; absent action uses the per-check default. There is no requirement for a linked review issue. A confirmed No with additional gaps retains its defect row and records Human Check details only in its Checklist Findings.

Every No requires at least one confirmed defect in issues linked through check_ids; kind defaults to defect. Defects link only to No. NA requires na_reason visible in Findings and has no defect row. Each evidence_gaps item requires check, missing and next_action, referring to a No or Human Check Checklist row; its details are appended to Findings without requiring any issue. No extra Excel columns are added by internal fields.

Compatibility: old kind=human_check issue objects are accepted only when linked to Human Check or No. Their description, manual action and addresses migrate into the corresponding Checklist Findings; they are excluded from the normalized defect list and the delivered defect sheet. They cannot substitute for a confirmed defect linked to No. New input should put review details in Checklist/evidence_gaps, not issues.

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

Confirmed unused/inapplicable template directives belong in issues as kind=defect linked to 10.3 No and are exported to 10. Robot.txt. Description records the exact groups/directives and the site evidence confirming they are unnecessary; How to Fix removes only those confirmed remnants and rechecks important URLs/resources. This is a configuration finding, not proof of private exposure or ranking harm. Unverified template purpose remains Human Check only in Checklist.
