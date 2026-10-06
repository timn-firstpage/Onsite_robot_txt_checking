# Robots.txt checks 10.1–10.7

## Evidence workflow

Read this reference when a robots audit is requested. Python fetches /robots.txt once per origin per run (including required CDN/subdomain origins), caches the raw response, URL, redirects, status and timestamp. Distinguish HTML error responses, empty content, comments, recognised directives and failures. A declared origin is scheme + host + port. Do not use simple substring matching or Python's basic robot parser as proof of Google's effective permissions. Prefer Screaming Frog robots results and matched directive evidence for Googlebot, recording relevant configuration when relying on SF behavior. A simple unambiguous live policy can instead be interpreted directly; unknown SF configuration must not block that independent decision. Complex or ambiguous matching still requires reliable rule evidence.

Read robots Sitemap declarations first, then reuse available sitemap/crawl URL exports. If no usable sitemap exists, prepare a local temporary inventory using public same-site links and existing SF crawl data. This is not a sitemap published to the website. Use configured discovery/request budgets, record page/depth limits and link exclusions, and avoid unbounded filter/query combinations. If no existing data can support discovery, a bounded public crawl needs source.allow_new_crawl; without it save candidates and leave affected checks unresolved. Never enable a new crawl silently.

Collect known candidate URLs from the crawl, sitemaps and a bounded path enumeration. Cache requests; do not treat missing URLs in an existing crawl as 404. Reuse candidate exports first; any new SF List/discovery crawl uses [shared preparation](sf-first-run-setup.md), source.allow_new_crawl scope permission and manual user Start. Capture all candidate results, not only the Noindex filter. Discover actual tool/filter/field names using references/screaming-frog-mcp.md; do not invent a List Mode API. Provide the URL-list file for the user and accept its export; affected checks remain in evidence_gaps.json until evidence arrives. No automated Start or indefinite waiting for manual completion.

SF evidence required per URL: status/redirect/final address, robots blocked/allowed status, relevant matched rule if available, Meta Robots, X-Robots-Tag and their target bot, canonical, title/H1 or targeted content for classification. Record missing fields explicitly. Directives > Noindex supplies meta/header noindex findings. Response Codes > Blocked by robots.txt supplies blocking evidence. Use resource exports for CSS/JS and rendering mode for dynamic coverage. Indexability=Non-Indexable alone does not prove noindex (it can reflect redirects/canonical/blocking). A missing field or filter row is not proof that noindex is absent.

Separate an obey-robots crawl from any explicitly configured ignore-robots diagnostic crawl. A noindex found only while ignoring robots cannot establish that Google can read it. JS-inserted directives require rendering evidence; static-only exports leave that scope unverified. Do not claim deindexing has occurred without search-index evidence.

## Decision table

| Check | Yes | No | NA / unresolved |
| --- | --- | --- | --- |
| 10.1 Does a robots.txt document exist? | Valid file containing at least one recognised directive | Confirmed missing/HTML-invalid file or empty, whitespace-only or comment-only file. Report empty as Empty robots.txt, not missing | Timeout/403/429/5xx or ambiguous content: Record evidence gap and block final export, not NA |
| 10.2 Are important pages being disallowed? | Positively phrased result: all tested applicable homepage/product/category/article URLs allowed for Googlebot and successfully fetched | At least one intended important page blocked or confirmed unusable; explain whether robots or HTTP caused it | Subtypes absent: explain NA in Findings. Critical uncertainty blocks final export unless a confirmed defect establishes No |
| 10.3 Are appropriate disallow blocks in place? | All confirmed applicable URLs designated should-not-crawl are effectively blocked | A confirmed should-not-crawl URL is allowed | No verified applicable objects: NA with discovery scope, not proof none exist. No non-empty Disallow is disclosed in Findings, not automatically a defect |
| 10.4 Are CSS and JS allowed? | All tested necessary CSS/JS allowed and accessible | Necessary resource blocked or confirmed broken | No external resources in tested pages: NA with reason. Unknown resource purpose/response: unresolved |
| 10.5 Are special pages handled appropriately? | Applicable classes meet the policies below | Confirmed class violates its policy | No verifiable objects: NA with attempted paths/sources and limitations. Class uncertainty: unresolved |
| 10.6 Is the lowercase robots.txt endpoint valid? | /robots.txt valid, even if uppercase also works | Only uppercase endpoint works or lowercase endpoint returns wrong content | Confirmed file absent: NA, refer to 10.1. Failed requests: unresolved |
| 10.7 Is sitemap declared in robots.txt? | At least one syntactically valid absolute HTTP(S) Sitemap URL | File present but no valid declaration | File absent: NA with reference to 10.1. Missing declaration is not proof sitemap does not exist |

For 10.2 the original wording asks whether pages are blocked, but Yes means the audit passes (no unintended blocking); Findings must make this explicit. Empty robots.txt is a user-specific audit defect, not an assertion that Google forbids empty files. A file with valid User-agent rules but no Disallow is not an empty file. Lack of sitemap declaration is an audit finding, not a claim the optional field is mandatory for Google.

Use actual existing should-not-crawl objects in 10.3; candidate names alone cannot establish that a URL must be blocked. Authentication is assessed under 10.5 and is not equivalent to Disallow. Not-found candidates are excluded, but 401/403/login redirects are access-control evidence or ambiguity, not absence. A 200 must be screened for soft 404 and generic homepage fallback. Report findings only when content/response corroborates classification.

## Default/plugin-generated rules are hints, not live functionality

A non-empty robots file may contain broad plugin/template rules unrelated to the site's current public features. Patterns such as /wp-content/uploads/wc-logs/, /woocommerce_transient_files/, /woocommerce_uploads/ and add-to-cart parameters suggest plugin-related intent, but do not prove an installed/active plugin, cart, account, exposed log directory or actual file existence. Do not label the entire file invalid, arbitrary or defective solely from this pattern. Record the suspected template origin as an inference, not a verified platform/default attribution.

Separate three statements: a directive exists; it effectively matches a test URL for Googlebot; a real page/feature has been verified. A synthetic blocked /cart or ?add-to-cart URL proves only a rule match, not an active shopping cart. add-to-cart parameter rules also do not prove /cart or /checkout is blocked. A 200 response requires content corroboration and soft-404/homepage-fallback exclusion. Missing from sitemap alone does not prove absence. If obeying robots prevents content verification, do not turn blocking alone into existence evidence; record that limit or use a separately permitted diagnostic.

For 10.3 evaluate confirmed applicable crawl-control targets, not how many generic Disallow lines exist. For 10.5 apply cart policy only to verified cart objects/flow. If bounded discovery yields no verifiable cart, use cart subcheck NA with the attempted paths, sources and limitations; do not give Yes just because generic ecommerce rules exist, or No because an assumed cart route is unblocked. Overall 10.5 still aggregates other applicable classes (e.g. admin), so cart NA does not automatically make the entire check NA.

Treat Allow: /wp-admin/admin-ajax.php as an exception whose actual effects are evaluated against required resource/function evidence. Its presence alone does not prove private admin exposure. Retained unused rules produce no Issues row merely for being unused; report only demonstrated effects such as blocking an important live page/resource, or a verified required target left unblocked. Removing template rules is not an automatic fix recommendation.

Example Findings (conditional on an actual completed check, not a claim about the user's example domain): 'robots.txt contains add-to-cart and plugin upload-path rules. Tested cart/checkout candidates and available crawl/sitemap links did not reveal a verifiable shopping flow. Cart subcheck NA within this scope; rules alone cannot establish active ecommerce. Other special-page classes assessed separately.'

## Bounded candidate discovery

Use these seed suffixes beneath the root and observed locale prefixes, within configured budgets. They are examples to extend from actual site evidence, not a claim of exhaustive site discovery. Preserve real URLs/queries. Store tested/not-tested candidates, reasons and result counts in raw evidence.

| Class | Candidate suffixes |
| --- | --- |
| Cart | /cart, /basket, /shopping-cart, /checkout/cart, /checkout |
| Thank-you | /thank-you, /thankyou, /order/success, /checkout/success, /order-confirmation |
| Admin | /admin, /administrator, /backend, /dashboard, /wp-admin |
| Account | /account, /my-account, /profile, /login, /signin, /register |
| Crawl-control candidates | /search and observed filter/sort/search parameter variants |
| Pagination | /page/2, /?page=2, /?paged=2; actual /category/<observed-slug>/page/2 and next links from the inventory |
| Category | /category, /categories; actual category slugs and their observed sort/filter/pagination variants |

Duplicate content requires observed variants plus actual content comparison; a query parameter or matching title is not sufficient. No login, registration, form submission, order creation or private-account access. This is an SEO audit, not a penetration test or exhaustive sensitive-path scanner.

## Pagination/category variants and crawl loops

For 10.2 preserve valuable category landing pages and meaningful pagination needed to discover products/articles. /page/ or /category/ alone is not an automatic Disallow/noindex requirement. Distinct paginated item sets are not duplicates simply because the template/title is shared; do not recommend canonicalising all distinct pages to page 1. Verify relevant self-canonicals and page-specific responses where indexable pagination is intended.

For 10.3/10.5 inspect observed low-value filter/sort combinations, equivalent query/path representations, repeated/empty/out-of-range pagination, and recursive URL growth. Confirm actual content and crawl-control intent before reporting absent controls. Out-of-range page numbers should not repeat the last page or silently return a normal homepage; record the response/content evidence. Noindex and canonical do not themselves impose a hard crawl boundary.

For temporary discovery the agent must keep a visited/requested set, strip fragments from request identity, preserve path/query evidence and avoid unsafe lowercasing or indiscriminate query removal. Do not request a known URL twice, follow redirect/pagination cycles indefinitely, invent thousands of page numbers, or enumerate the Cartesian product of filters. Follow actual links; cap each pagination series at robots.pagination_pages_per_series and each category's variant sample at robots.variants_per_category, plus global page/depth/request limits. Exceeding an audit sample limit is a coverage limitation, not proof the site is defective.

Stop further expansion of a series when it cycles, points to already-tested pages, returns verified 404/410, or repeatedly serves the same confirmed item set/content for different page numbers. Use source/target link pairs, final destinations and actual item/content fingerprints; shared header/footer alone is insufficient. Keep counts and excluded families in Coverage, and fetch targeted evidence for a suspected site defect before writing an Issue.

These per-family limits are enforced by the agent's discovery workflow/SF scope configuration, not by the collector (which only generates a finite candidate list). For broad SF discovery configure actual scope exclusions/limits from observed patterns, or use staged bounded List Mode batches; do not claim this helper automatically controls an independent SF crawl.

## Bot-specific full-site blocking

Always inspect User-agent grouping, not just the presence/count of Disallow: /. A full-site rule applies to its matching bot group; many named groups without Googlebot or a matching wildcard do not establish Googlebot is blocked. Merge duplicate group names for counting; preserve raw line evidence and evaluate effective matching rules, including Allow exceptions. Disallow count is not an automatic defect threshold.

Summarize bots blocked site-wide and distinguish search/index discovery, AI search/retrieval, training/extended-use controls, SEO/backlink tools and unknown/legacy names. Use current primary vendor documentation for roles; do not assign purpose solely from a bot's name. Google-Extended does not control Google Search inclusion/ranking. Applebot differs from Applebot-Extended. GPTBot differs from OAI-SearchBot, and user-triggered ChatGPT-User requests have different robots behavior; a listed rule alone does not prove actual service denial.

For 10.2, No is supported when an important live page is blocked for a bot the site's stated discovery policy requires. For 10.3, evaluate alignment with both allowed important-page discovery and intended restrictions. Site-wide blocking of a required discovery bot is a separate cause from missing restrictions on low-value paths. Confirm required channels from user policy; do not silently make every named bot mandatory. If policy is not yet known, disclose the block list and exact unanswered policy question in the handover rather than guessing a final result. Restricted training or backlink tools alone need not be defects; omitted bots are not proof of real access through HTTP/WAF.

Confirmed policy conflict creates an Issues row such as 'Required discovery bot blocked site-wide', naming the specific bot, applicable rules, affected public URLs and the intended channel. Describe potential restricted access, not proven ranking loss or absence from an index. Recommend adjusting only the conflicting group after owner policy is known, preserving intentional restrictions. Never recommend deleting every bot block solely because the list is long.

## Special-page policies (10.5)

| Class | Accepted policy | Confirmed defect |
| --- | --- | --- |
| Cart | Effective Disallow (crawl control), or crawlable applicable noindex (index control) | Public verified cart has neither control |
| Thank-you | Ordinary page: effective Disallow or readable noindex. Private order data additionally requires access control | Neither SEO control for ordinary page, or confirmed unauthorized exposure of private order data |
| Admin | Protected functions/content require authentication/authorization. Public login page alone is not exposure | Confirmed protected admin function/content exposed without authorization; Disallow alone cannot protect it |
| Account | Private account content requires authorization. Public login/register pages should have effective Disallow or readable noindex under this audit policy | Confirmed private exposure, or verified public login/register page with neither SEO control |
| Duplicate content | Valid corresponding canonical, appropriate redirect or readable noindex; verified unnecessary crawl variants may be disallowed | Confirmed duplication without appropriate treatment, or wrong/unusable canonical destination |

Label whether accepted control limits crawling or indexing; do not claim Disallow guarantees no indexing. Disallow plus hidden noindex is not verified readable noindex. Apply bot-specific directives to Googlebot, not arbitrary bots. Do not infer that an account is protected solely from its URL name or that a 200 login page exposes private content.

## Findings, coverage and aggregation

Every NA explains the unmet prerequisite and tested scope, e.g. 'Tested 15 thank-you candidates and sitemap/crawl links; none was verifiable. Such pages may require a completed order; no transaction was performed.' Never write 'page does not exist' solely from enumeration. Coverage includes counts, URL sources, full/sample scope, excluded variants, rendering mode and unverified flows. Private page classes that were not actually verified remain clearly qualified.

Any confirmed failing applicable class establishes No; all applicable classes passing with none unresolved establishes Yes; all classes genuinely inapplicable/no verifiable objects establishes NA with reasons. Critical unresolved evidence prevents Yes. Unknown/errors go to evidence_gaps.json with required evidence and next action; do not export a final report until resolved. Every No creates a linked Issues row; NA creates none. Same defect may link to multiple checks. Do not invent security/crawl-budget impacts without relevant evidence.

## Primary references

- https://www.screamingfrog.co.uk/seo-spider/issues/directives/noindex/
- https://www.screamingfrog.co.uk/seo-spider/user-guide/tabs/
- https://www.screamingfrog.co.uk/seo-spider/tutorials/robots-txt-tester/
- https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec
- https://developers.google.com/search/docs/crawling-indexing/robots/intro

- https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading
- https://developers.google.com/crawling/docs/faceted-navigation

- https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers
- https://developers.openai.com/api/docs/bots
- https://support.apple.com/en-ie/119829
- https://duckduckgo.com/duckduckgo-help-pages/results/duckduckbot
