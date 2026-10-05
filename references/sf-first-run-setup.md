# Screaming Frog first-run configuration

Use on the first audit after installing/importing this skill, when the user requests setup, or when the executing machine/SF version/profile changes. Installing a skill alone does not start background UI work. Routine SF configuration needed for the requested audit is within this workflow; do not repeatedly ask permission to toggle these audit settings. Starting a new crawl still follows source.allow_new_crawl and the actual requested scope.

Use the computer-use skill/tools actually provided by the executing environment to inspect and configure the native SF UI when MCP cannot read/apply the relevant settings. Read that environment's Computer Use instructions before UI control. Mac needs a Mac-capable native-app tool: do not copy Windows sky APIs or assume browser-only automation can control SF. If native control is unavailable, provide this table as manual steps and keep setup incomplete; do not claim settings were changed. Existing exports and verified existing profiles can still be used.

## Two profiles, with isolated scope

Reuse the integrated agent's main metadata crawl, retaining status, redirects, title/H1, robots/directive/canonical and resource relationships. Do not save every page's HTML for this flow. Do not apply robots inventory, pagination, variant or candidate limits to that shared crawl or to other tasks. The main crawl retains its owner/orchestrator-defined site scope and budget. Other tasks may need HTML and can select their own profile; this flow does not disable their required evidence.

Use a separate targeted-content profile only for selected URLs whose purpose, soft-404/duplicate status or dynamic behavior cannot be resolved from existing evidence. Its new crawl has a separate ID, original settings/profile are saved and restored, and results are joined by exact URL, timestamp and actual configuration. Start with content_batch_size URLs (25 by default); this is a batch size, not a total check limit. Process further necessary batches under remaining approved budget rather than discarding evidence after the first batch. Source HTML and conditional JS-rendered HTML are stored only in these batches. Do not automatically re-crawl the full site.

## Configuration checklist

UI paths below follow current official documentation; inspect the actual version/menu labels, especially macOS application Settings. Values are this audit's chosen profile, not universal SF defaults.

| Setting | Location / where to inspect | Desired value | Reason / verification |
| --- | --- | --- | --- |
| Licence/version | Actual application UI | Version/licence supports requested configuration and MCP if using MCP | Record actual version/features, not a guessed capability |
| Storage mode (MCP only) | File > Settings > Storage Mode, or macOS equivalent | Database storage | MCP requires database mode; export-only audit does not require MCP |
| MCP connection (MCP only) | Actual MCP menu / Settings > MCP Server | Reuse active server and allowed base; start if needed and available | Record actual local URL and allowed directory; reuse integrated agent connection. Confirm live tools/schema rather than only an 'active' UI badge |
| User-Agent | Configuration > HTTP Header > User-Agent | Googlebot variant appropriate to target (prefer smartphone for mobile-focused audit) | Record exact selection/string; verify applicable rules. This is not Google's real IP/access or proof of indexing |
| robots.txt | Configuration > robots.txt > Settings | Obey robots.txt for main profile | Preserve true blocking. Use separate Ignore robots.txt but report status profile only for necessary diagnostics; never use plain Ignore as sole permission evidence |
| Custom robots | Configuration > robots.txt > Custom | No override for production validation | Ensure evidence uses site's live rules. Archive any intentional separate diagnostic override |
| CSS and JavaScript | Configuration > Spider > Crawl | Store/Crawl enabled for CSS and JavaScript; external resource checking where needed | Retain actual resource records and page/resource links; test representative CDN resources within scope |
| Rendering | Configuration > Spider > Rendering | Text Only for static scope; JavaScript when robots.dynamic_resources=true or evidence establishes JS dependence | Record chosen mode and excluded dynamic scope. Do not force JS for every site; dynamic mode may execute analytics and make extra requests |
| Source HTML | Configuration > Spider > Extraction > Store HTML | Shared metadata profile: disabled unless another task requires it. Targeted-content profile: enabled | Retain HTML only for unresolved page-purpose/soft-404/duplicate checks |
| Rendered HTML | Same extraction settings | Targeted dynamic batches only; disabled in metadata profile unless another task needs it | Store rendered evidence when needed, not every page by default |
| HTTP headers | Configuration > Spider > Extraction > HTTP Headers | Enabled | Preserve response headers, including X-Robots-Tag evidence |
| Meta robots / canonical evidence | Actual page fields and exports | Verify Meta Robots, X-Robots-Tag and canonical data present | Do not invent an extraction toggle when the version exposes default fields instead. Distinguish missing field from inspected absence |
| Respect Noindex | Configuration > Spider > Advanced | Disabled for this audit profile | This SF option suppresses noindex URLs from reported results; disabling retains the URLs for auditing and does not alter site directives |
| Respect Canonical | Configuration > Spider > Advanced | Disabled for this audit profile | Retain canonicalised URLs for duplicate-content checks; still extract canonicals |
| Redirect follow-through | Configuration > Spider > Advanced / actual List Mode options | Follow redirects for targeted candidate testing within scope and configured hop limits | Preserve initial candidate, every hop and final response. SF's automatic crawl requests are not automatically bounded by the Python helper |
| Speed / limits | Configuration > Speed; Spider > Limits / actual equivalent | For robots-only supplemental discovery use configured rate and URL/depth/series limits; leave shared primary crawl settings intact | Confirm total SF behavior fits the job budget. JS renders may make additional requests; record actual consumption and stop when budget requires |
| Optional paid integrations | Actual API Access / AI/embedding integrations | No optional paid calls for audit profile | No AI embeddings or SEO provider API is needed to classify pages using the executing agent |
| Candidate mode | Mode > List and upload URL list (for follow-up crawl) | Actual candidate list; use Spider only for bounded public discovery | Keep URL count and original candidate results, including 404/redirect/blocked rows. Selecting/configuring mode does not itself start a crawl |
| Saved profile | File > Configuration > Save As | Save audit-specific .seospiderconfig outside source files | Save metadata and targeted-content profiles separately; do not replace the user's default/global profile |

## Computer Use procedure

1. Locate the actual SF application and inspect active crawl state. Do not interrupt a running crawl, overwrite unsaved crawl data or silently replace another job's settings. Wait for it to finish or keep setup pending while doing independent local work.
2. Record existing relevant settings. Save the current configuration to a unique local backup profile before changing it, where supported. Record machine/version and backup path; do not commit machine-local profiles, endpoint settings or crawl data.
3. Reuse the existing MCP/storage setup. Apply only needed rows to the current audit profile, checking the visible resulting state after each related group. If changing storage would require an app restart, first save relevant state and follow the executing environment's actual UI rules; do not terminate other work.
4. Save the metadata profile and derive a targeted-content profile through the real UI. Do not apply robots-specific discovery limits to another task's primary crawl. If diagnostics are needed, derive a separate named ignore-but-report profile and keep its evidence separate. Avoid 'Save as Default' and global client-setting changes.
5. Record verification in <run>/sf-setup.json: machine, version, observed settings, prior settings/backup path, profile path, timestamps, and per-setting verification source (UI/MCP/export/operator). Confirm metadata/directive fields are retrievable; for targeted content batches separately verify selected HTML evidence is retrievable. A stored HTML checkbox does not guarantee MCP has a content-export capability; use available local SF bulk exports (All Page Source) when necessary.
6. Record source.crawl_config_path, source.content_crawl_config_path and source.crawl_settings_file in the resolved run config. sf-setup.json describes current setup; only associate it with crawls subsequently performed with that profile. Keep old crawl settings separately, unknown unless verified. Changes today do not repair old crawl evidence.
7. Start a small test only if a new crawl is permitted. Inspect representative static/dynamic/redirect/404 candidates and a page/resource relationship to confirm the required evidence exists. Save the new crawl ID and actual settings. No new crawl permission: finish configuration, prepare candidate list and report the exact remaining action.
8. Reuse profile on subsequent runs after checking machine/version/profile compatibility and site scope. Re-verify when changed, instead of blindly trusting an 'installed' marker. In a shared HTTPS+robots agent, configure a compatible per-run profile serially and restore previous configuration when switching jobs.

Setup success requires observed phase-specific settings, saved profiles and verified access to the evidence required for that phase, not full-site HTML storage. A Python install, tool connection or screen toggle alone is not a completed audit. Final reports accept only Yes/No/NA; missing evidence belongs in the handover/gap list until resolved.

## Primary references

- [SF configuration](https://www.screamingfrog.co.uk/seo-spider/user-guide/configuration/)
- [Source HTML and HTTP headers](https://www.screamingfrog.co.uk/seo-spider/user-guide/tabs/)
- [JavaScript rendering](https://www.screamingfrog.co.uk/seo-spider/tutorials/crawl-javascript-seo/)
- [Saving a configuration profile](https://www.screamingfrog.co.uk/seo-spider/tutorials/seo-spider-cloud/)
