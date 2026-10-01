"""Tests de collect.py, avec des réponses d'API simulées : python3 -m unittest upgrade/scripts/test_collect.py"""

import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import collect  # noqa: E402

TODAY = date(2026, 9, 30)


def release(name, eol_from, eol=False, lts=False, latest=None, maintained=None, codename=None):
    return {"name": name, "codename": codename, "isLts": lts, "isEol": eol, "eolFrom": eol_from,
            "isMaintained": (not eol) if maintained is None else maintained,
            "latest": {"name": latest or f"{name}.0"}}


NODE = {"result": {"releases": [
    release("26", "2029-04-30"),
    release("24", "2028-04-30", lts=True, latest="24.21.0", codename="Krypton"),
    release("22", "2027-01-15", lts=True, codename="Jod"),
    release("20", "2026-04-30", eol=True, lts=True, codename="Iron"),
]}}
REDIS = {"result": {"releases": [release("7.4", None), release("7.2", "2026-12-01")]}}
PURLS = {"result": [
    {"identifier": "pkg:docker/library/node", "product": {"name": "nodejs"}},
    {"identifier": "pkg:docker/library/redis", "product": {"name": "redis"}},
]}


def listing(name, versions, default, deprecated=()):
    return {"versions": [{"versionKey": {"version": v}, "publishedAt": date_,
                          "isDefault": v == default, "isDeprecated": v in deprecated,
                          "deprecatedReason": "use x instead" if v in deprecated else ""}
                         for v, date_ in versions]}


class FakeFetch:
    def __init__(self, routes):
        self.routes = routes
        self.log = {}

    def get(self, url, body=None):
        for key, value in self.routes.items():
            if url.endswith(key):
                return value(body) if callable(value) else value
        return {"_error": "HTTP 404"}


class EolTest(unittest.TestCase):
    def test_version_matches_the_most_precise_cycle(self):
        out = collect.eol_status("redis", "7.2.4", FakeFetch({"/redis/": REDIS}), TODAY)
        self.assertEqual(out["cycle"], "7.2")

    def test_eol_release_is_eol_and_target_is_newest_lts(self):
        out = collect.eol_status("nodejs", "20.11.1", FakeFetch({"/nodejs/": NODE}), TODAY)
        self.assertEqual(out["status"], "eol")
        self.assertEqual(out["target"]["cycle"], "24")

    def test_end_of_active_support_is_reported(self):
        releases = {"result": {"releases": [dict(release("24", "2028-04-30", lts=True),
                                                 eoasFrom="2026-10-20")]}}
        out = collect.eol_status("nodejs", "24", FakeFetch({"/nodejs/": releases}), TODAY)
        self.assertEqual((out["eoasFrom"], out["target"]["eoasFrom"]), ("2026-10-20",) * 2)

    def test_release_ending_within_six_months_is_eol_soon(self):
        out = collect.eol_status("nodejs", "22", FakeFetch({"/nodejs/": NODE}), TODAY)
        self.assertEqual(out["status"], "eol-soon")

    def test_codename_matches_a_cycle(self):
        out = collect.eol_status("nodejs", "krypton", FakeFetch({"/nodejs/": NODE}), TODAY)
        self.assertEqual((out["cycle"], out["status"]), ("24", "supported"))

    def test_missing_eol_date_is_supported_with_a_reason(self):
        out = collect.eol_status("redis", "7.4", FakeFetch({"/redis/": REDIS}), TODAY)
        self.assertEqual(out["status"], "supported")
        self.assertIn("non publiée", out["reason"])

    def test_unknown_version_is_unknown_not_supported(self):
        out = collect.eol_status("nodejs", "99", FakeFetch({"/nodejs/": NODE}), TODAY)
        self.assertEqual(out["status"], "unknown")

    def test_api_failure_is_unknown(self):
        out = collect.eol_status("nodejs", "20", FakeFetch({}), TODAY)
        self.assertEqual(out["status"], "unknown")


class ImageTest(unittest.TestCase):
    fetch = FakeFetch({"/identifiers/purl/": PURLS, "/nodejs/": NODE, "/redis/": REDIS,
                       "/alpine-linux/": {"result": {"releases": [
                           release("3.18", "2025-05-09", eol=True)]}}})

    def test_tag_gives_version_and_alpine_base(self):
        out = collect.image_status("node:20.11-alpine3.18", self.fetch, TODAY)
        self.assertEqual((out["product"], out["cycle"], out["status"]), ("nodejs", "20", "eol"))
        self.assertEqual(out["base"]["status"], "eol")

    def test_floating_tags_are_flagged(self):
        for ref in ("redis", "redis:latest", "node:lts-alpine", "docker.io/library/node:alpine"):
            with self.subTest(ref=ref):
                self.assertEqual(collect.image_status(ref, self.fetch, TODAY)["status"], "floating")

    def test_debian_codename_gives_base(self):
        self.assertEqual(collect.parse_image("node:22-bookworm-slim")["base"], ("debian", "12"))

    def test_private_image_is_unknown(self):
        out = collect.image_status("ghcr.io/acme/api:1.2", self.fetch, TODAY)
        self.assertEqual(out["status"], "unknown")

    def test_registry_port_is_not_a_tag(self):
        self.assertEqual(collect.parse_image("localhost:5000/app")["tag"], "latest")


class BumpTest(unittest.TestCase):
    def test_kinds(self):
        cases = [("1.2.3", "1.2.4", "patch"), ("1.2.3", "1.3.0", "minor"),
                 ("1.2.3", "2.0.0", "major"), ("0.3.1", "0.4.0", "major"),
                 ("2.0.0", "2.0.0", "none"), ("latest", "2.0.0", "unknown")]
        for current, latest, kind in cases:
            with self.subTest(current=current, latest=latest):
                self.assertEqual(collect.bump_kind(current, latest), kind)


class PackageTest(unittest.TestCase):
    def status(self, routes):
        return collect.package_status({"name": "@acme/lib", "version": "1.0.0"},
                                      FakeFetch(routes), TODAY, use_github=False)

    def test_deprecated_latest_means_abandoned(self):
        out = self.status({"%40acme%2Flib": listing(
            "@acme/lib", [("1.0.0", "2020-01-01T00:00:00Z")], "1.0.0", deprecated={"1.0.0"})})
        self.assertEqual(out["maintenance"], "abandoned")
        self.assertEqual(out["deprecated"], "use x instead")

    def test_no_release_for_two_years_is_stale(self):
        out = self.status({"%40acme%2Flib": listing(
            "@acme/lib", [("1.0.0", "2023-06-01T00:00:00Z")], "1.0.0")})
        self.assertEqual(out["maintenance"], "stale")

    def test_one_year_without_release_is_still_active(self):
        out = self.status({"%40acme%2Flib": listing(
            "@acme/lib", [("1.0.0", "2025-10-01T00:00:00Z"), ("2.0.0", "2025-10-02T00:00:00Z")],
            "2.0.0")})
        self.assertEqual((out["maintenance"], out["bump"]), ("active", "major"))

    def test_private_package_is_unknown(self):
        self.assertEqual(self.status({})["maintenance"], "unknown")


class PackageManagerOutputTest(unittest.TestCase):
    PNPM_LIST = [{"name": "app", "path": "/repo", "dependencies": {
        "kit": {"version": "2.0.0", "dependencies": {"devalue": {"version": "5.8.1"}}},
        "shared": {"version": "link:../shared"}},
        "devDependencies": {"vitest": {"version": "4.1.8", "dependencies": {
            "devalue": {"version": "5.8.1"}}}}},
        {"name": "web", "path": "/repo/web", "dependencies": {"kit": {"version": "2.0.0"}}}]

    def by_name(self, packages):
        return {p["name"]: p for p in packages}

    def test_direct_and_transitive_packages_are_deduplicated(self):
        pkgs = self.by_name(collect.packages_from_list(self.PNPM_LIST))
        self.assertEqual(set(pkgs), {"kit", "devalue", "vitest"})
        self.assertTrue(pkgs["kit"]["direct"])
        self.assertEqual(pkgs["kit"]["source"], "app, web")
        self.assertFalse(pkgs["devalue"]["direct"])

    def test_npm_ls_object_is_read_too(self):
        pkgs = collect.packages_from_list({"name": "app", "dependencies": {
            "lodash": {"version": "4.17.15"}}})
        self.assertEqual(pkgs[0]["name"], "lodash")

    def test_outdated_sets_latest_on_direct_packages_only(self):
        pkgs = collect.apply_outdated(collect.packages_from_list(self.PNPM_LIST), {
            "kit": {"current": "2.0.0", "latest": "2.5.0"},
            "devalue": {"current": "5.8.1", "latest": "5.9.0"}})
        pkgs = self.by_name(pkgs)
        self.assertEqual(pkgs["kit"]["latest"], "2.5.0")
        self.assertNotIn("latest", pkgs["devalue"])

    def test_inventory_packages_are_merged_as_direct(self):
        merged = self.by_name(collect.merge_packages(
            [{"name": "a", "version": "1.0.0", "direct": False}],
            [{"name": "a", "version": "1.0.0"}]))
        self.assertTrue(merged["a"]["direct"])


class OsvTest(unittest.TestCase):
    def fetch(self):
        return FakeFetch({
            "/querybatch": lambda body: {"results": [
                {"vulns": [{"id": "GHSA-a"}, {"id": "GHSA-b"}]} for _ in body["queries"]]},
            "/vulns/GHSA-a": {"aliases": ["CVE-1", "GHSA-b"], "database_specific": {
                "severity": "HIGH"}, "affected": [{"package": {"name": "lodash"}, "ranges": [
                    {"events": [{"introduced": "0"}, {"fixed": "4.17.21"}]}]}]},
            "/vulns/GHSA-b": {"aliases": ["CVE-1", "GHSA-a"]},
            "/packages/lodash": listing("lodash", [("4.17.21", "2021-02-20T00:00:00Z")],
                                        "4.17.21"),
        })

    def test_aliases_are_merged_and_fix_is_checked(self):
        vulns = collect.osv_scan([{"name": "lodash", "version": "4.17.15"}], self.fetch())
        self.assertEqual([v["id"] for v in vulns], ["GHSA-a"])
        self.assertEqual((vulns[0]["fixed"], vulns[0]["fixPublished"]), (["4.17.21"], True))

    def test_unpublished_fix_is_reported(self):
        fetch = self.fetch()
        fetch.routes["/packages/lodash"] = listing("lodash", [("4.17.15", "2019-07-19")], "4.17.15")
        self.assertFalse(collect.osv_scan([{"name": "lodash", "version": "4.17.15"}],
                                          fetch)[0]["fixPublished"])


if __name__ == "__main__":
    unittest.main()
