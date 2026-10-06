# Report and evidence contract

This is the skill's normalized input, not the original SF tool schema. Map actual export headers and archive the mapping. Agent-reviewed decisions go into findings.json; raw exports alone are not a report.

```json
{
  "requested_checks": ["10.1", "10.5"],
  "checklist": [
    {"id":"10.1","check":"10.1 Does a robots.txt document exist?","result":"No","findings":"robots.txt 返回 200，但内容为空。","coverage":"检查主站 /robots.txt；保存原始内容。"},
    {"id":"10.5","check":"10.5 Are special pages handled appropriately?","result":"Human Check","findings":"候选清单已准备，尚未验证特殊页用途。","human_check_reason":"缺少候选响应、内容和访问控制证据。","coverage":"已准备候选，未验证；未执行订单或登录。"}
  ],
  "issues": [
    {"check_ids":["10.1"],"issue":"Empty robots.txt","description":"robots.txt 可访问，但未包含有效指令。按约定 audit 标准判为问题，不代表安全漏洞。","how_to_fix":"根据网站需求配置有效规则，并声明实际 sitemap；不要添加无必要的限制。","addresses":["https://example.com/robots.txt"]},
    {"check_ids":["10.5"],"kind":"human_check","issue":"Human Check: Special-page evidence missing","description":"缺少特殊页实际响应、内容和访问控制证据；尚未确认网站缺陷。","how_to_fix":"人工核对已准备候选的响应、用途、noindex／canonical／访问控制，保存必要证据后更新判断；不提交订单或登录私人账户。","addresses":["https://example.com/"]}
  ],
  "evidence_gaps": [{"check":"10.5","missing":"候选响应、内容和访问控制证据","next_action":"人工核对候选并保存响应／指令／用途证据。"}]
}
```

Include every requested check exactly once; full robots audit requires 10.1–10.7. Partial audit may include only user-requested checks, explicitly stated in handover. Internal id/check_ids/kind are not additional Excel columns. Final results are Yes/No/NA/Human Check. Always export the final workbook even with unresolved evidence; never omit difficult checks or turn unknown into NA/Yes/No. Every Human Check requires human_check_reason visible in Findings and a kind=human_check Issues row. Human-check issues link to Human Check or No, are visibly prefixed Human Check, explain the evidence gap and give a concrete manual action. Every No requires a confirmed kind=defect issue (default when kind omitted), linking only to No. A No with additional gaps keeps its defect and gets an extra human_check issue plus Human Check Findings. NA requires na_reason and has no issue. Each optional evidence_gaps item requires check, missing and next_action, and links to a human_check issue; it is appended to that check's Findings. Gaps never block export when properly labelled. requested_checks defaults to all seven; the example is explicitly partial. Yes still requires evidence and coverage. The builder validates structure, not substantive claims.

Issues group only identical cause/action and review versus defect kind. Description includes observations and supported impact, or Human Check evidence gaps without claiming a defect. How to Fix contains repair or manual verification actions. addresses lists full known actual/candidate URLs, deduplicated and one per line; label candidate existence as unverified. If individual URLs are unknown, use the audited site's origin/robots endpoint and describe the missing inventory, not invented verified pages. Keep every affected page for a shared blocked resource. Preserve relationships in raw evidence. Do not manufacture impact claims or real indexing status.

Run archive:

```text
<run_root>/<run_id>/
  config.json
  manifest.json       source crawl, time, rendering, user-agent, field mapping, completeness, file hashes/counts
  usage.json          cumulative live_requests, mcp_calls, retries, paid_api_calls
  raw/                robots text/response metadata, sitemap/crawl/directive/resource exports
  candidates-<origin-hash>.txt
  robots-<origin-hash>.json
  inventory/          URL sources, classifications and excluded candidate reasons
  evidence_gaps.json   gaps also represented by Human Check workbook rows/issues
  findings.json
  {site name}_robots_audit_{YYYY-MM-DD}.xlsx
  handover.md
  sf-handover.json     optional shared preparation record or its path in manifest
```

Record missing fields, unknown version/rendering and truncation explicitly. Crawl evidence keeps its original time; it is not a new live check. Usage is shared with integrated flows, never reset to gain more budget. The collector updates live_requests for its initial/redirect requests; the agent records SF calls, candidate crawl coverage and other requests. Do not commit client data or machine-local settings.

sf-handover.json belongs to shared preparation and records selected profile, user confirmations, file paths and limitations. It is not findings.json, is not consumed by build_report.py, and does not establish audit completeness. Verify actual exports and per-check evidence before creating final decisions. Config-load errors belong in preparation diagnostics; concrete missing audit evidence belongs in evidence_gaps.json. Keep website 429 separate from MCP/tool 429, preserving source, status, Retry-After and affected coverage.
