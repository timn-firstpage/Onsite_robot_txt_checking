# Screaming Frog evidence retrieval

Reuse the HTTPS flow's existing MCP endpoint, allowed directory, completed crawl and runtime. Do not register a second server or guess port/tool names. Local exports are equally supported and need no live MCP connection.

1. Discover actual live tools/schema and filter/field names, and save the mapping/version in manifest. This repository has not performed an SF MCP end-to-end test.
2. Select the supplied crawl ID or explicitly confirm the matching site/time. Never load whichever crawl is latest without checking. Work serially when the integrated agent shares a Spider instance.
3. Confirm crawl completion/rendering/user-agent/robots behavior. Incomplete evidence cannot prove an overall Yes. Existing records are timestamped crawl evidence, not fresh HTTP tests.
4. Export complete URL data to files within the actual SF allowed base; only counts and a few examples go into chat. Map address, status, redirect/final URL, robots status, Meta Robots, X-Robots-Tag, canonical, title/H1 and required resource links. Use raw fields, not only Indexability.
5. Directives > Noindex identifies meta/header noindex. Response Codes > Blocked by robots.txt identifies blocked URLs and matched rules where available. Discover actual MCP filter names, not assumed UI-to-API equivalence. Get all candidate responses rather than only noindex matches.
6. Missing candidate URLs require an authorized List Mode crawl or user exports; do not infer 404/noindex absence from missing crawl rows. Honour source.allow_new_crawl. If live schema cannot perform the needed operation, retain candidate file and explain unresolved checks rather than inventing API calls.
7. Without a usable sitemap, generate a temporary local inventory from public internal links using SF, bounded by config. Dynamic CSS/JS requires rendering evidence. A diagnostic ignore-robots crawl must be separate and cannot prove Google can read the hidden noindex.

Usage: reuse shared cache keys containing crawl ID/filter/fields/version. Track cumulative mcp_calls and live_requests in usage.json across flows, including redirects/retries. Stop at config limits and record missing coverage. No paid SEO/AI integrations required. Do not replace the whole usage object when adding counters from another flow.

Primary references:
- https://www.screamingfrog.co.uk/seo-spider/user-guide/configuration/#mcp-server
- https://www.screamingfrog.co.uk/seo-spider/issues/directives/noindex/
- https://www.screamingfrog.co.uk/seo-spider/user-guide/tabs/
- https://www.screamingfrog.co.uk/seo-spider/tutorials/robots-txt-tester/
