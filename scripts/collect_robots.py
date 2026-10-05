"""Cache robots.txt evidence and prepare URL candidates; no page/directive crawl."""
import argparse
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

SEEDS = {
    "cart": ["/cart", "/basket", "/shopping-cart", "/checkout/cart", "/checkout"],
    "thank_you": ["/thank-you", "/thankyou", "/order/success", "/checkout/success", "/order-confirmation"],
    "admin": ["/admin", "/administrator", "/backend", "/dashboard", "/wp-admin"],
    "account": ["/account", "/my-account", "/profile", "/login", "/signin", "/register"],
    "search": ["/search"],
}
RECOGNISED = {"user-agent", "allow", "disallow", "sitemap", "crawl-delay"}
MAX_BYTES = 512 * 1024


def origin_of(url):
    parts = urlsplit(url)
    if parts.scheme not in {"http", "https"} or not parts.hostname or parts.username or parts.password:
        raise ValueError("A public HTTP(S) URL without embedded credentials is required")
    return f"{parts.scheme}://{parts.netloc}"


def analyse(text, status, truncated=False):
    directives, sitemaps = [], []
    for number, line in enumerate(text.splitlines(), 1):
        content = line.split("#", 1)[0].strip()
        if ":" not in content:
            continue
        key, value = content.split(":", 1)
        key, value = key.strip().lower(), value.strip()
        if key in RECOGNISED:
            directives.append({"line": number, "key": key, "value": value})
        if key == "sitemap":
            try:
                origin_of(value)
                if not re.search(r"\s", value):
                    sitemaps.append(value)
            except ValueError:
                pass
    if truncated:
        kind = "unresolved_truncated"
    elif status in {404, 410}:
        kind = "missing"
    elif status != 200:
        kind = "unresolved_response"
    elif re.search(r"<!doctype\s+html|<html\b|<body\b", text, re.I):
        kind = "invalid_html"
    elif not any(line.split("#", 1)[0].strip() for line in text.splitlines()):
        kind = "empty"
    elif not directives:
        kind = "invalid_no_recognised_directives"
    else:
        kind = "directives_present"
    return {"kind": kind, "directives": directives, "sitemaps": list(dict.fromkeys(sitemaps)),
            "has_nonempty_disallow": any(d["key"] == "disallow" and d["value"] for d in directives)}


def candidates(origin, prefixes, known_urls, limit):
    if not isinstance(limit, int) or limit < 1:
        raise ValueError("candidate_limit must be a positive integer")
    rows = {}
    for url in known_urls:
        if origin_of(url) == origin:
            rows[url] = {"url": url, "source": "observed", "class_hint": None}
    for prefix in [""] + prefixes:
        if not isinstance(prefix, str) or any(c in prefix for c in "?#") or "://" in prefix or ".." in prefix.split("/"):
            raise ValueError("Locale prefixes must be observed relative paths")
        for category, suffixes in SEEDS.items():
            for suffix in suffixes:
                url = origin + "/" + (prefix.strip("/") + suffix).lstrip("/")
                rows.setdefault(url, {"url": url, "source": "enumerated", "class_hint": category})
    result = list(rows.values())
    return result[:limit], len(result) - min(limit, len(result))


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def collect(config, run_dir, origin=None, known_urls=()):
    if config.get("checks", {}).get("robots_txt", True) is False:
        raise ValueError("robots_txt flow is disabled in config")
    origin = origin_of(origin or config["site"]["start_url"])
    allowed = set(config["site"].get("allowed_hosts", []))
    allowed.add(urlsplit(config["site"]["start_url"]).hostname)
    if urlsplit(origin).hostname not in allowed:
        raise ValueError("Origin outside configured allowed_hosts")
    run = Path(run_dir)
    run.mkdir(parents=True, exist_ok=True)
    raw = run / "raw"
    raw.mkdir(exist_ok=True)
    key = hashlib.sha256(origin.encode()).hexdigest()[:12]
    summary_path = run / f"robots-{key}.json"
    if summary_path.exists():
        # Preserve immutable per-run evidence and usage; new evidence needs a new run.
        return json.loads(summary_path.read_text(encoding="utf-8"))
    settings = config.get("robots", {})
    rows, excluded = candidates(origin, settings.get("observed_locale_prefixes", []), known_urls, settings.get("candidate_limit", 100))
    candidate_path = run / f"candidates-{key}.txt"
    candidate_path.write_text("".join(row["url"] + "\n" for row in rows), encoding="utf-8")
    budget = config["budget"]
    usage_path = run / "usage.json"
    usage = json.loads(usage_path.read_text(encoding="utf-8")) if usage_path.exists() else {}
    usage.setdefault("live_requests", 0)
    interval = 1 / max(0.01, settings.get("requests_per_second", 1))
    opener = build_opener(NoRedirect())
    url, hops, text, error, status, truncated = origin + "/robots.txt", [], "", None, None, False
    if not config.get("checks", {}).get("live_checks", True):
        error = "live_checks_disabled"
    else:
        for _ in range(budget.get("max_redirect_hops", 5) + 1):
            if usage["live_requests"] >= budget["max_live_requests"]:
                error = "budget"
                break
            if hops:
                time.sleep(interval)
            usage["live_requests"] += 1
            usage_path.write_text(json.dumps(usage, indent=2) + "\n", encoding="utf-8")
            try:
                request = Request(url, headers={"User-Agent": "OnsiteRobotsAudit/1.0", "Accept": "text/plain"})
                try:
                    response = opener.open(request, timeout=budget.get("timeout_seconds", 15))
                except HTTPError as http_error:
                    response = http_error
                with response:
                    status = response.code
                    location = response.headers.get("Location")
                    body = response.read(MAX_BYTES + 1)
                    truncated = len(body) > MAX_BYTES
                    text = body[:MAX_BYTES].decode("utf-8-sig", errors="replace")
                hops.append({"url": url, "status": status, "location": location})
                if status in {301, 302, 303, 307, 308} and location:
                    target = urljoin(url, location)
                    origin_of(target)
                    if urlsplit(target).hostname not in allowed:
                        error = "redirect_outside_scope"
                        break
                    url = target
                    if url in {hop["url"] for hop in hops}:
                        error = "redirect_loop"
                        break
                    continue
                break
            except (URLError, OSError, ValueError) as exc:
                error = type(exc).__name__
                break
        else:
            error = "redirect_budget"
    analysis = analyse(text, status, truncated)
    if error:
        analysis["kind"] = "unresolved_" + error
    raw_path = raw / f"robots-{key}.txt"
    raw_path.write_text(text, encoding="utf-8")
    summary = {"origin": origin, "requested_url": origin + "/robots.txt", "last_requested_url": hops[-1]["url"] if hops else None,
               "time_utc": datetime.now(timezone.utc).isoformat(), "hops": hops, "status": status,
               "error": error, "truncated": truncated, "raw_file": str(raw_path.resolve()),
               "sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest(), "analysis": analysis,
               "candidate_file": str(candidate_path.resolve()), "candidates": rows, "excluded_candidates": excluded,
               "note": "Candidates unverified; Googlebot permissions and noindex require SF evidence."}
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--origin", help="Optional scoped CDN/subdomain HTTP(S) origin")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8-sig"))
    known_path = config.get("robots", {}).get("candidate_url_file")
    known = Path(known_path).read_text(encoding="utf-8-sig").splitlines() if known_path else []
    result = collect(config, args.run_dir, args.origin, [url.strip() for url in known if url.strip()])
    print(json.dumps({"origin": result["origin"], "kind": result["analysis"]["kind"], "candidates": len(result["candidates"]), "error": result["error"]}, ensure_ascii=False))
