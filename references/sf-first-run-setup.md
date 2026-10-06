# Shared SF prerequisite and robots evidence validation

This filename remains the entry for older documentation links. Profile loading and manual run preparation now belong to the independent [sf-shared-config skill](https://github.com/timn-firstpage/On-_site_SF_shared_config/blob/main/SKILL.md), with installation/profile details in its [README](https://github.com/timn-firstpage/On-_site_SF_shared_config). This robots package does not bundle or automatically install it. Do not rebuild another first-install configuration workflow here.

## Choose the route

| Situation | Action |
| --- | --- |
| Suitable existing crawl/exports | Verify site, time, scope, completion and check-specific fields; reuse directly. No profile load or exhaustive historical-settings gate. |
| Partly usable evidence | Keep supported checks; inspect existing exports, then use permitted finite read-only static identity/response/redirect checks. Only remaining SF-specific/rendering gaps need a new user-run crawl. |
| Active user crawl | Do not load over it or interrupt it. Deliver the current final Excel with Human Check and a checkpoint now; update after user handover, without indefinite polling. |
| SF-specific/rendering evidence still needed; follow-up permitted | Invoke the installed shared skill for preparation. Main is selected automatically for a full crawl; targeted profile only for necessary content/response follow-ups. |
| Shared skill absent | Give its install link or equivalent manual Load, sitemap, Start and save instructions. Do not claim it ran; suitable existing files remain usable. |

source.allow_new_crawl determines whether this flow can request a new discovery/List crawl. It never authorizes agent-started crawling. When false, archive candidates and exact gaps, request existing exports or an explicit change to the scope instruction; do not silently start or bypass it with another crawler. Direct robots collection and finite selected-URL static identity/response/redirect checks are separately controlled by checks.live_checks and the shared request budget; see [retrieval boundaries](delivery-boundaries.md#evidence-retrieval-order-and-bounded-static-follow-up). A false allow_new_crawl does not disable these permitted static checks or authorize recursive crawling.

Resolve bundled profile paths from the actual installed shared skill on the SF host. Respect explicit user profile overrides; invalid overrides require correction, not fallback. Reliable evidence of the intended loaded, unchanged profile allows skipping load; a filename alone does not. HTTPS and robots reuse the same preparation record/session rather than each reloading main.

## Manual run boundary

Only supported standalone loading or native UI may load a profile. sf_crawl(config_path) starts crawling and is not a loader. Any load failure immediately receives the shared skill's manual UI Load + sitemap instructions. Preserve the original error/source; no native retries, helper-file hunts, CLI guessing or pending setup loop. This does not block independent checks 10.1/10.6/10.7 or evidence-supported conclusions.

Before directing manual Load, shared preparation saves the selected .seospiderconfig to the user's actual Downloads on the SF host and verifies readability, nonzero size and source/copy equality. Supply that Downloads path, then guide sitemap confirmation. Reuse identical copies and preserve different same-name files. If host access prevents saving, give the download/copy-to-Downloads step first, disclosing unverified delivery; do not claim success. Suitable existing evidence or a reliably unchanged loaded profile skips copying/reloading. The delivered config is not the later .seospider crawl result.

The user confirms site/scope and sitemap discovery or manually adds the actual sitemap/index in UI, then manually Starts and supervises. Do not reload generic profiles after site-specific sitemap changes. Missing sitemap limits discovery but does not invalidate unrelated robots-file checks. Candidate List follow-ups use the supplied URL list rather than forcing another whole-site sitemap crawl. Shared main uses JS and avoids whole-page HTML storage; targeted content stores source/rendered HTML. Static results already supported do not require re-rendering, and stored HTML is not proof the connector can export it.

User saves/exports to their actual Downloads folder after crawl and required Crawl Analysis completion, and supplies exact paths/status. Automatic database storage alone is not this handover. Preserve partial/stopped status. Sustained website 429/connection errors or URL loops receive user UI review; ordinary 404/redirects remain audit evidence, not automatic restart triggers. Distinguish website 429 from MCP/tool errors and preserve Retry-After and affected coverage. This flow does not automatically restart crawls.

## Caller validation after handover

Keep the shared sf-handover.json path in the local manifest/handover; it records preparation/provenance, not a worksheet Result or complete audit evidence. A binary .seospider needs actual supported SF loading and export inspection; size/signature/filename alone is insufficient. Readable exports need expected columns, full rows and scope. Record tool-verified versus user-confirmed observations accurately. Configuration changes today do not amend historical crawl evidence.

| Check | Necessary evidence |
| --- | --- |
| 10.1 / 10.6 / 10.7 | Direct robots response, content, lowercase endpoint and declarations; these can proceed without SF setup |
| 10.2 | Sitemap/fallback URL inventory and effective Googlebot permissions; successful HTTP fetch and extra purpose confirmation are not pass prerequisites |
| 10.3 | Agent selects applicable families from site evidence before follow-up; effective Googlebot rules for those finite enumeration samples; all blocked supports scoped Yes without existence proof. No non-empty effective Disallow in readable robots gives audit-standard No with further validation |
| 10.4 | Actual CSS/JS identity, intended-public source-page relationships, responses and effective bot permissions; qualify verified private-only exclusions and dynamic scope |
| 10.5 | Actual purpose/access-control evidence plus relevant meta/header noindex, canonical or redirects |

Use independently interpretable live rules and explicit response/directive evidence where sufficient. Verify SF user-agent/robots mode only when a conclusion depends on that crawl's behavior; verify rendering only for dynamic claims. Do not request all settings solely because native control failed. Ignore-robots diagnostics must be separate and cannot establish Google can read a blocked noindex. Obey-mode missing blocked-page content requires a specific diagnostic/export gap, not invented absence.

Robots inventory/series/candidate limits apply to this flow's supplemental discovery only, not the shared main crawl or other audits. content_batch_size is a batch size, not a total cap; preserve all necessary batches and their distinct timestamps/IDs. Configuration transitions use shared preparation and accepted user confirmations, preserving the main crawl and actual sitemap. Record exact missing URL/field/relationship/purpose and next action in evidence_gaps.json. Unknown/errors are Human Check, not NA. The robots caller always exports the final workbook with gaps, reasons and manual actions, even if preparation or supplementary evidence remains incomplete; return useful progress rather than indefinite pending.

Follow-up preparation is not a reason to wait before delivery: first export the current final workbook with Human Check gaps and the candidate/manual-action handover, then update after the user supplies evidence. See [delivery boundaries](delivery-boundaries.md) for NA, minimum evidence and protected-route cases.
