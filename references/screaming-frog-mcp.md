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

## Crawl settings and minimum evidence

The skill run config does not change a saved SF crawl. Record the settings used when that crawl was made; a setting chosen today cannot retrospectively verify an older crawl. If MCP does not expose settings, accept the saved SF configuration or operator-confirmed settings tied to the crawl ID/time; do not label them tool-verified.

| SF setting/evidence | Purpose and audit boundary |
| --- | --- |
| HTTP Header > User-Agent | Determine requested server response and applicable bot rules. Configure Googlebot for Google-focused validation; this does not reproduce Google's real IP/access or index status |
| robots.txt mode | Obey robots for the main permission check. A separate Ignore robots.txt but report status diagnostic can fetch blocked content while reporting blocking; it cannot establish Google reads its noindex. Plain Ignore robots.txt is unsuitable as sole robots-permission evidence |
| Spider > Rendering | Text Only checks initial HTML; JavaScript executes/rendering and can reveal dynamic links/resources/directives. Use JS when needed, not as an unconditional prerequisite for every static URL. Declare static-only limitations |
| Spider > Extraction > Store HTML / Store Rendered HTML | Retain source/rendered HTML for page-type, soft-404 and content verification. Enable before collection where needed; it does not guarantee the MCP connector can expose stored content. If unavailable through MCP, obtain actual local SF exports or targeted permitted content evidence |
| CSS/JS crawling and resource relationships | For 10.4 include resource URL, source page, HTTP response and applicable robots status. Resource counts alone are insufficient; record exclusions and dynamic coverage |
| List Mode | Load the 22 (or actual run's) candidate URLs for targeted response/content/directive evidence rather than blindly crawling the whole site. Requires allow_new_crawl permission; missing old crawl rows prove nothing |

Resolve each check independently: 10.2 needs important-page inventory + HTTP/Googlebot permissions; 10.3 needs real applicable should-not-crawl targets + effective rules; 10.4 needs required-resource source/target relationships + response/permissions; 10.5 needs page-purpose/control evidence + relevant directives. Missing JS rendering blocks a dynamic-scope conclusion, not a supported static result automatically. Missing extraction or settings is Needs Review only where material to that check. '/training' and HTTP 200 do not establish private exposure.

Fresh robots and older crawl evidence must each retain their dates. State the time mismatch, and use targeted fresh validation for critical cases before claiming current compliance. No confirmed Issues is not an overall pass while any applicable checks are Needs Review.
