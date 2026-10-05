"""Offline tests; no real site requests."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from collect_robots import analyse, candidates, collect, origin_of


class CollectorTests(unittest.TestCase):
    def test_disabled_flow_has_no_side_effects(self):
        with patch("collect_robots.build_opener") as opener:
            with self.assertRaises(ValueError):
                collect({"checks": {"robots_txt": False}}, "unused")
            opener.assert_not_called()

    def test_empty_comments_html_and_failures(self):
        for content in ["", " \n", "# comment\n"]:
            self.assertEqual(analyse(content, 200)["kind"], "empty")
        self.assertEqual(analyse("<html>error</html>", 200)["kind"], "invalid_html")
        self.assertEqual(analyse("", 404)["kind"], "missing")
        self.assertEqual(analyse("", 403)["kind"], "unresolved_response")
        self.assertEqual(analyse("User-agent: *", 200, True)["kind"], "unresolved_truncated")

    def test_directives_and_sitemaps(self):
        data = analyse("User-agent: *\nDisallow:\nSITEMAP: https://example.com/site.xml\nSitemap: /bad.xml\n", 200)
        self.assertEqual(data["kind"], "directives_present")
        self.assertFalse(data["has_nonempty_disallow"])
        self.assertEqual(data["sitemaps"], ["https://example.com/site.xml"])
        self.assertTrue(analyse("Disallow: /admin", 200)["has_nonempty_disallow"])

    def test_bounded_candidates_and_queries(self):
        known = ["https://example.com/a?x=1&y=2", "https://other.com/cart"]
        rows, excluded = candidates("https://example.com", ["/zh-hant"], known, 3)
        self.assertEqual(rows[0]["url"], known[0])
        self.assertEqual(len(rows), 3)
        self.assertGreater(excluded, 0)
        self.assertTrue(all(origin_of(r["url"]) == "https://example.com" for r in rows))

    def test_budget_and_immutable_cache(self):
        config = {"site": {"start_url": "https://example.com"}, "budget": {"max_live_requests": 2}, "robots": {}}
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as directory:
            path = Path(directory)
            (path / "usage.json").write_text(json.dumps({"live_requests": 2, "mcp_calls": 7}), encoding="utf-8")
            with patch("collect_robots.build_opener") as opener:
                first = collect(config, path)
                second = collect(config, path)
                self.assertEqual(first, second)
                self.assertEqual(first["error"], "budget")
                opener.return_value.open.assert_not_called()
            self.assertEqual(json.loads((path / "usage.json").read_text())["mcp_calls"], 7)

    def test_fragments_deduplicate_without_losing_pagination_queries(self):
        urls = ["https://example.com/category/a?page=2#top", "https://example.com/category/a?page=2#bottom", "https://example.com/category/a?page=3"]
        rows, _ = candidates("https://example.com", [], urls, 100)
        observed = [row["url"] for row in rows if row["source"] == "observed"]
        self.assertEqual(observed, ["https://example.com/category/a?page=2", "https://example.com/category/a?page=3"])


if __name__ == "__main__":
    unittest.main()
