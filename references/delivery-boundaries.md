# Decision and delivery boundaries

Read alongside robots-rules.md. Apply these boundaries before requesting more evidence. The audit has a finite current evidence pass: available exports, permitted bounded collection and classification. It is not a requirement to finish every possible follow-up.

## Deliver before waiting

1. Reuse current evidence. Evaluate each requested check independently; an unavailable MCP/native app, unconfirmed historical configuration or unavailable sitemap does not invalidate unrelated evidence.
2. Finish permitted bounded work. Stop a blocked retrieval, exhausted budget, missing export or unverified business-policy branch; archive its precise gap. Do not poll indefinitely, repeatedly request permission, or require a fresh full-site crawl.
3. Deliver the final two-sheet Excel now. Missing evidence is Human Check; confirmed defects remain No even when another part needs Human Check. Send candidate lists and manual actions with that report. Further user-run SF work can update a later report.
4. If partial progress JSON omits requested rows or Human Check issues, use build_report.py with --site-url and --prepared-input to complete those as Human Check and archive the delivered input. requested_checks defaults to all seven; narrow it only for an explicitly partial user request. Use the real audited URL. Review/translate fallback wording to the requested language. Completion does not repair a fabricated No, invalid ID/schema, or proven defect without its issue; fix those inputs rather than dropping checks.

A runtime/write failure is a technical delivery failure, not a website No or NA. Resolve available runtime/path problems and retry a valid export. If writing an actual Excel is impossible, report the exact technical blocker and preserve findings; do not claim a file exists.

## Minimum sufficient evidence per decision

Require only evidence material to the decision. Do not demand every candidate have HTML, meta, headers, canonical, matched rules and rendering settings simultaneously.

Distinguish absent fields from verified absent directives. A missing column/row, failed fetch, unavailable extraction or unexplained null is unknown. An explicitly completed applicable extraction/export that represents absent directives as an empty value can establish absence when that field's meaning and page scope are verified. A blank Meta Robots does not establish absence of header X-Robots-Tag; check whichever applicable sources are needed before claiming neither exists. A Noindex filter containing no rows alone is not a full candidate inventory. A static extraction supports the static response only; require rendering evidence only where dynamic directives/content materially affect the decision.

| Check | Evidence sufficient for the stated scope | Conditional evidence / boundary |
| --- | --- | --- |
| 10.1 | Lowercase response/redirect evidence and actual text, screened for error HTML, empty content and recognised directives | Truncated/unavailable response is Human Check. A recognised token alone does not validate an otherwise malformed file; valid sitemap-only robots can establish existence without a User-agent group. |
| 10.2 | Intended public-page inventory, effective Googlebot permission and final response for tested URLs | A clear effective block confirms No without downloading blocked content, once page identity/intent is independently established. Meta noindex/canonical are not prerequisites for this crawl-permission check. HTTP errors must be described as accessibility failures rather than invented robots blocking. |
| 10.3 | Actual applicable should-not-crawl targets, explicit policy/default policy rationale and effective matching rules | A robots-only synthetic path proves a match, not target existence. Missing content behind an independently known block need not force a diagnostic fetch merely to confirm that block. Authentication/noindex/canonical are assessed separately in 10.5. |
| 10.4 | Necessary page-to-CSS/JS relationships and effective permission/response evidence | Include same-origin and external/CDN resources. Inline-only pages with a verified complete resource inventory can be NA. Missing resource exports are Human Check, not “no resources”. Do not require meta/canonical or full HTML for every asset. Third-party origins count only when their resources are necessary to the tested pages. |
| 10.5 | Actual page/flow classification and evidence of at least one accepted control for that category | Noindex needs its applicable meta/header plus readable Googlebot access; canonical needs the relevant source/destination relationship; access control needs an unauthenticated response or gate tied to known protected content/function. Do not require absent alternative controls once one sufficient policy is verified. |
| 10.6 | Evidence that the lowercase HTTP endpoint serves the valid robots file | No need to probe uppercase when lowercase works. Server filesystem names are unknown and irrelevant to this endpoint check. Confirmed absent file is NA here with 10.1 No; lowercase invalid content is No; failed observation is Human Check. |
| 10.7 | Complete raw robots text containing at least one syntactically valid absolute HTTP(S) Sitemap declaration | Does not require sitemap download, every child sitemap, or every listed URL to return 200. Record any independently observed sitemap health problem separately and link its affected URL; do not change a valid declaration to No solely because its fetch is 429. Unread robots text is Human Check, not “no declaration”. |

An empty robots file is No for 10.1; it also has no Sitemap declaration (10.7 No) and does not serve a valid configured file under this audit standard (10.6 No). Rules absence does not automatically make 10.2–10.5 fail: actual pages, resources and applicable policies still determine those checks. A confirmed 404/410 makes 10.1 No and dependent file checks 10.6/10.7 NA; an inaccessible 403/429/5xx leaves those file conclusions Human Check.

## NA versus unknown

| Situation | Decision |
| --- | --- |
| Owner confirms the site has no ecommerce/transaction flow, with no contradictory current evidence | Relevant cart/transaction thank-you subcategories NA; record confirmation, sources and scope. Other categories remain independent. |
| Completed bounded discovery has no live-function clues; tested candidates are verified missing, soft 404 or generic fallback | Category NA within the tested scope, with sources/counts/exclusions. Do not claim exhaustive nonexistence. |
| Candidate exists in inventory but its response/content was not obtained; a family was omitted by a limit; 403/429 prevented meaningful checking | Human Check for the materially unverified category; not NA. |
| Known checkout or submission flow may generate thank-you URLs only after a transaction | Human Check unless supplied read-only evidence or owner confirmation resolves the applicable control. Never create an order to obtain evidence. |
| Template WooCommerce rules with no independent live-flow evidence | Hints only. Use completed discovery or owner confirmation for scoped NA; an untested candidate list is insufficient. |
| Duplicates not demonstrated after completed scoped comparison | Duplicate subcategory NA with comparison scope. Matching names/titles or query strings alone are insufficient. Unperformed comparison of a material suspected pair is Human Check. |

Policy source precedence: explicit site-specific user/owner policy, then the published special-page defaults in robots-rules.md. Record justified deviations. Missing extra business preferences does not require asking again when the default clearly applies. For 10.3, require an actual crawl-control target and rationale; do not designate every category/account URL should-not-crawl solely from its name. A public login gate can support the scoped protected-route access-control check without inspecting private content. A generic login page alone does not prove all admin routes secure. An unexplained 403/WAF challenge alone is ambiguous, not proof of authentication or exposure. Never claim a full security audit.

Googlebot is the default required discovery bot for this Google SEO audit. List other site-wide blocks in Findings where relevant. Unknown policy for optional training/SEO/AI bots does not by itself downgrade a Googlebot-supported result or block delivery. Evaluate additional channels only when requested or explicitly required by site policy; unresolved required-channel intent/access becomes Human Check for that scope.

Aggregation: any confirmed applicable defect => No, retaining Human Check gaps when present; all tested applicable objects pass and no material unresolved objects => Yes with scoped coverage; all categories inapplicable under the above rules => NA with reasons; otherwise => Human Check. Subcategory NA does not turn a check with other passing applicable categories into NA. Sampling supports only the stated sample, never an unqualified whole-site pass.
