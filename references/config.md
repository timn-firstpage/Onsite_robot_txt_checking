# Configuration ownership and integration

Use config.template.json for robots-only runs. Integrated configs may carry additional HTTPS keys; this flow ignores those rather than starting HTTPS checks. This preserves compatibility without copying irrelevant defaults into the standalone template. Configuration does not install Python packages or register MCP.

| Settings | Executor / purpose |
| --- | --- |
| site.start_url, allowed_hosts | Collector uses scope; agent uses site selection. site.name is used by agent when naming report |
| run_id; source.* | Agent selects completed SF crawl/exports and honours allow_new_crawl for any new discovery/List Mode crawl. crawl_config_path points to the primary metadata profile; content_crawl_config_path points to a separate targeted-content profile; crawl_settings_file records verified settings tied to the relevant crawl; collector reads neither |
| mcp.* | Agent uses the actual server/allowed-base/tool schema; collector does not connect to MCP |
| checks.robots_txt | Agent routes this flow; explicitly false prevents collector execution |
| checks.live_checks | Collector skips network and records unresolved status when false; agent must also avoid new live URL checks |
| budget.max_live_requests, max_redirect_hops, timeout_seconds | Collector enforces its requests/redirects/timeouts; agent applies the same limits to other live operations |
| budget.max_mcp_calls, poll_interval_seconds, max_poll_calls | Agent enforces against cumulative usage; collector has no MCP/poll operations |
| budget.max_preview_rows, max_preview_chars | Agent limits chat previews, not evidence exports |
| budget.max_paid_api_calls | Agent keeps optional paid integrations disabled (default 0) |
| cache.reuse_same_crawl_exports | Agent reuses archived SF exports when source/filter/field/version keys match |
| output.* | Agent resolves language, timezone, audit date and run paths; report CLI receives explicit site/date/output directory |
| robots.candidate_url_file, observed_locale_prefixes, candidate_limit | Collector prepares bounded candidate lists; file must contain one absolute URL per line. Resolve its path for the executing machine |
| robots.requests_per_second | Collector throttles its redirect requests; agent applies the configured rate to other live checks |
| robots.user_agent | Agent configures/verifies Googlebot permissions in SF; collector's HTTP identifier is OnsiteRobotsAudit/1.0, not simulated Googlebot |
| robots.temporary_inventory_page_limit, temporary_inventory_depth_limit | Agent caps robots supplemental discovery only, never the shared primary crawl or another task; collector does not crawl the site |
| robots.dynamic_resources | Agent enables/verifies SF rendering/resource coverage; collector does not render JavaScript |
| robots.pagination_pages_per_series, variants_per_category | Agent caps robots supplemental series/variant samples only; these do not restrict another task or the shared primary crawl |
| robots.content_evidence_strategy, content_batch_size | Agent uses targeted HTML collection (default targeted), in staged batches of 25 unresolved URLs; batch size is not a total cap. Collector does not launch/apply SF profiles |

Agent-owned settings are execution instructions, not a proxy that automatically enforces SF server limits. Record actual coverage and consumption in manifest/usage. One integrated agent shares cumulative usage and operates on a Spider serially.

## Deliberately excluded from the standalone template

- checks.http_urls, mixed_content, hostname_consistency, hostname_page_limit and site.preferred_origin belong to HTTPS. They may remain in an integrated config but have no effect here.
- cache.force_refresh and live_response_ttl_hours are not implemented by this collector. It returns the archived response/candidates for the same run and origin, including failed responses. Use a new run for fresh evidence; preserve cumulative usage when still part of the same integrated job. Do not promise freshness from inherited cache settings.
- budget.max_retries and stop_after_consecutive_errors are not implemented by the collector. It does not auto-retry. A follow-up run is an agent decision within remaining budget, not automatic behavior activated by an inherited key.
- robots.empty_file_is_issue is not configurable. Empty/blank/comment-only robots.txt is always a defect under this agreed audit standard, even if an older config contains false.

## Libraries and runtime

Each flow keeps its own requirements.txt. The robots runtime currently requires Python 3.9+ and openpyxl>=3.1,<4; all collection helpers use standard libraries. The current HTTPS flow has the same third-party requirement, so one verified AUDIT_PYTHON/venv can serve both. If future dependency versions conflict, use separate environments/explicit interpreter paths instead of overwriting a shared environment. No pip/install/version changes happen merely by reading config. Author-only validation tooling (e.g. PyYAML) is not an audit runtime dependency.

Shared primary crawl scope/budget comes from the orchestrator. Do not reinterpret max_live_requests as an SF page-count limit; the collector only enforces this on its counted requests. Maintain cumulative usage and approved overall budget, isolate robots supplemental profiles, and restore prior settings when changing jobs. Metadata-first does not guarantee every decision can be made without source/rendered content.
