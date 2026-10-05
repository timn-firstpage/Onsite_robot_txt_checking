# Report and evidence contract

This is the skill's normalized input, not the original SF tool schema. Map actual export headers and archive the mapping. Agent-reviewed decisions go into findings.json; raw exports alone are not a report.

```json
{
  "requested_checks": ["10.1", "10.5"],
  "checklist": [
    {"id":"10.1","check":"10.1 Does a robots.txt document exist?","result":"No","findings":"robots.txt 返回 200，但内容为空。","coverage":"检查主站 /robots.txt；保存原始内容。"},
    {"id":"10.5","check":"10.5 Are special pages handled appropriately?","result":"NA","findings":"未发现可验证的特殊页面。","na_reason":"已测试 15 个候选路径并检查 sitemap/站内链接；无可验证对象，不能确认页面不存在。","coverage":"15 个候选；未执行订单或登录。"}
  ],
  "issues": [
    {"check_ids":["10.1"],"issue":"Empty robots.txt","description":"robots.txt 可访问，但未包含有效指令。按约定 audit 标准判为问题，不代表安全漏洞。","how_to_fix":"根据网站需求配置有效规则，并声明实际 sitemap；不要添加无必要的限制。","addresses":["https://example.com/robots.txt"]}
  ]
}
```

Include every requested check exactly once; full robots audit requires 10.1–10.7. Partial audit may include only requested checks, explicitly stated in handover. Internal id/check_ids are not exported as extra columns. Every No has an issue referencing its ID; issues link only to No checks. NA requires na_reason visible in Findings. Final results accept only Yes/No/NA. Missing evidence is recorded separately in evidence_gaps.json and handover; unresolved checks cannot be exported or relabeled NA. requested_checks defaults to all seven; a smaller scope requires an actual user-requested partial audit, never just omission of difficult checks. The example above is an explicitly partial audit. Yes still requires evidence and coverage. The builder validates these structural conditions; it cannot prove substantive claims.

Issues group only identical cause/fix. Description includes observations and supported impact; How to Fix contains actions; addresses lists full affected URLs, deduplicated and written one per line. Keep every affected page for a shared blocked resource. Preserve page/resource relationships in descriptions and raw evidence. Do not manufacture impact claims or real indexing status.

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
  evidence_gaps.json   unresolved check, missing evidence, next action (not a workbook result)
  findings.json
  {site name}_robots_audit_{YYYY-MM-DD}.xlsx
  handover.md
```

Record missing fields, unknown version/rendering and truncation explicitly. Crawl evidence keeps its original time; it is not a new live check. Usage is shared with integrated flows, never reset to gain more budget. The collector updates live_requests for its initial/redirect requests; the agent records SF calls, candidate crawl coverage and other requests. Do not commit client data or machine-local settings.
