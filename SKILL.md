---
name: onsite-audit-robots
description: Audit robots.txt configuration and special-page handling using Python evidence collection, Screaming Frog exports and agent classification, producing Checklist and Issues Excel sheets.
---

# Onsite Robots.txt Audit

Audit checks 10.1–10.7 for a supplied site. Use Python for raw robots collection/candidate preparation, Screaming Frog for crawl permissions and directives, and agent reasoning for classification and policy decisions. Do not replace SF with a custom noindex/canonical crawler.

## Inputs and shared configuration

Use [config.template.json](config.template.json), or the user's integrated config with robots settings. Read [configuration ownership](references/config.md): share connection/runtime/site/source/budget/output settings, but keep per-flow check settings and dependency declarations. The standalone template omits HTTPS-only keys and unimplemented collector switches. This skill executes only robots checks, even when the shared config includes enabled HTTPS keys. Set checks.robots_txt=true. Preserve the shared MCP endpoint, allowed-base directory, existing crawl and AUDIT_PYTHON runtime; never copy a different machine's absolute paths.

Read [robots rules](references/robots-rules.md) for classifications, candidate paths and Yes/No/NA boundaries. Read [report schema](references/report-schema.md) before writing findings.json. For live SF retrieval, read [MCP guide](references/screaming-frog-mcp.md); supplied exports do not require an MCP connection. For a new runtime, read [Python runtime](references/runtime-python.md).

On the first audit after skill import/install, or when SF machine/version/profile changes, read [first-run SF configuration](references/sf-first-run-setup.md). Use the executing environment's available native Computer Use skill/tools for necessary UI-only settings, verify the actual UI, save separate metadata/targeted-content profiles and record setup evidence. Do not enable full-site HTML storage or apply robots discovery caps to the integrated agent's primary crawl/other tasks. This user has requested first-run configuration assistance; do not stop to reconfirm ordinary audit toggles. Mac requires actual Mac-capable tools, not Windows APIs or browser-only control. Reuse established settings when verified; do not change global defaults or interrupt another crawl. Setup permission does not enable an otherwise disallowed new crawl.

## Workflow

1. Create a unique writable run directory; save resolved config, audit date in the user's timezone and provenance. In an integrated run, reuse the orchestrator's manifest, raw evidence, cache and cumulative usage.json. Do not reset request/MCP budgets for each skill or load shared SF crawls concurrently.
2. Run [collect_robots.py](scripts/collect_robots.py) to archive /robots.txt once per scoped origin, extract Sitemap declarations and write bounded candidate URL lists. This helper does not test candidates, crawl sitemaps, or judge effective Googlebot permissions. Record its errors and remaining coverage. Collector caching is fixed per-run; it does not implement TTL, force-refresh, automatic retries or a consecutive-error counter. Obtain fresh evidence in a new run without resetting an integrated budget. A recognised directive is not necessarily a complete valid robots group; confirm interpretation with SF.
3. Reuse completed SF crawl/sitemap exports to identify important pages and special-page candidates, including category landing pages, /page/ and page/paged parameters. Apply the pagination/category loop boundaries in the robots reference: visited-set deduplication, bounded series/variant samples, no unlimited page-number/filter generation. Do not blanket-block useful category/pagination pages. Without a usable sitemap, use bounded public same-site link discovery in SF to produce a local temporary inventory, never a published sitemap. Missing candidates require an explicitly permitted SF List Mode crawl or user exports. Honour source.allow_new_crawl; otherwise save the URL list and leave dependent checks unresolved.
4. Export full candidate responses, robots blocking, Meta Robots, X-Robots-Tag, canonical and required resource metadata. Reuse this metadata first. Only unresolved classifications/content comparisons require targeted HTML batches; content_batch_size is not a total evidence limit. Store rendered HTML only for necessary dynamic batches, restore prior SF profile after each supplemental crawl, and keep new crawl provenance separate. Use the actual tool schema and export fields. Noindex-filter-only data is insufficient to judge the remaining candidates. Verify Googlebot rules and the crawl's rendering mode. Absent/null fields and URLs missing from the crawl are unknown, not a pass or 404.
5. Apply checks 10.1–10.7, using response/content evidence to exclude soft 404s and classify real pages. Enumerated path names and default/plugin robots rules alone cannot establish existence or purpose: add-to-cart or woocommerce paths do not prove an active cart. Follow the template-rule boundary in the robots reference. Empty, whitespace-only and comment-only robots.txt produce No plus an Empty robots.txt issue under this audit standard. No Disallow alone is disclosed, not automatically a security issue. Disallow controls crawling, not private access or proven deindexing.
6. Write agent-reviewed findings.json, then run [build_report.py](scripts/build_report.py). Every NA requires a specific reason; No requires linked issue evidence; errors/unknowns go to evidence_gaps.json and handover, and block final export. Scope limitations cannot be converted into Yes. The report generator validates schema and associations, not the correctness of agent reasoning.
7. Verify workbook headers/values and readable layout, save raw evidence and handover, and return the report plus material limitations. Do not claim real Google index status from SF directives. No login, form submission, registration or order creation. Do not modify website/server settings.

## Delivery

Exactly two sheets, no extra columns:

| Sheet | Headers |
| --- | --- |
| Checklist | Check; Result; Findings; Coverage |
| Issues | Issue; Issue Description; How to Fix; Address |

Use only Yes/No/NA; never leave a delivered Result blank. Missing evidence is not NA. Resolve all requested checks before final export; do not omit unresolved checks to make the report look complete. Findings is narrative evidence; NA explanations must be visible there. Coverage states counts, URL sources, full/sample scope, rendering and exclusions. Issues only contain confirmed defects linked to No checks. Group only same-cause/same-fix findings; Address contains full URLs, one per line. Keep both sheet headers when no issues exist. Protect against formula-like untrusted input and preserve URL/query strings.

Filename: `{site name}_robots_audit_{YYYY-MM-DD}.xlsx`. Use the user's site name or hostname without www. Never overwrite a previous report; use a new run directory. Match the requested report language. Keep machine setup messages out of customer-facing Findings/Coverage.
