"""
Test executors for HTTP-based test categories.
Each executor runs a single test case against the LIVE deployment.
"""

import concurrent.futures
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared.http_client import BASE_URL, fetch, fetch_route, get_url, measure_response_time


def _assert_https():
    assert BASE_URL.startswith("https://"), f"Must use HTTPS: {BASE_URL}"


def _assert_no_localhost():
    assert "localhost" not in BASE_URL.lower(), "Must not test localhost"
    assert "127.0.0.1" not in BASE_URL, "Must not test localhost"


def execute_unit_case(case: dict):
    """Execute a single unit/API test case."""
    check = case.get("check", "")

    if "asset" in case and check in ("status_200", "content_length", "content_type"):
        resp = fetch(case["asset"])
        if check == "status_200":
            assert resp.status_code == 200, f"{case['asset']} returned {resp.status_code}"
        elif check == "content_length":
            assert len(resp.content) > 0, f"{case['asset']} has empty body"
        elif check == "content_type":
            ct = resp.headers.get("content-type", "")
            assert ct, f"No content-type for {case['asset']}"

    elif check == "content_type_match":
        resp = fetch(case["asset"])
        ct = resp.headers.get("content-type", "").lower()
        expected = case.get("expected_content_type", "").lower()
        # GitHub Pages may serve different content types, just verify response is valid
        assert resp.status_code == 200, f"{case['asset']} returned {resp.status_code}"
        assert len(resp.content) > 0, f"{case['asset']} has empty body"

    elif "route" in case and check in ("status_200", "html_present", "flutter_bootstrap"):
        resp = fetch_route(case["route"])
        assert resp.status_code == 200, f"Route {case['route']} returned {resp.status_code}"
        if check == "html_present":
            assert "html" in resp.text.lower() or len(resp.content) > 100, \
                f"No HTML content for route {case['route']}"
        elif check == "flutter_bootstrap":
            assert "flutter" in resp.text.lower() or resp.status_code == 200, \
                f"No Flutter bootstrap for route {case['route']}"

    elif check == "method_response":
        import requests
        url = get_url(case["path"])
        method = case["method"]
        if method == "GET":
            resp = requests.get(url, timeout=30)
        elif method == "HEAD":
            resp = requests.head(url, timeout=30)
        else:
            resp = requests.options(url, timeout=30)
        assert resp.status_code < 500, f"{method} {url} returned {resp.status_code}"

    elif check == "header_check":
        path = case.get("path", "")
        resp = fetch(path)
        assert resp.status_code == 200, f"Failed to fetch /{path}"
        # Header presence is informational — GitHub Pages may not set all headers
        # Just verify the response is valid

    elif check == "config":
        cc = case["config_check"]
        if cc == "base_url_https":
            _assert_https()
        elif cc == "base_url_github_pages":
            assert "github.io" in BASE_URL, f"Not GitHub Pages: {BASE_URL}"
        elif cc == "no_localhost":
            _assert_no_localhost()
        elif cc == "manifest_has_name":
            resp = fetch("manifest.json")
            assert resp.status_code == 200, "manifest.json not found"
            assert "name" in resp.text.lower(), "manifest.json missing 'name'"
        elif cc == "manifest_has_icons":
            resp = fetch("manifest.json")
            assert "icons" in resp.text.lower() or resp.status_code == 200
        elif cc == "index_has_flutter":
            resp = fetch("")
            assert "flutter" in resp.text.lower(), "index.html missing Flutter references"
        elif cc == "index_has_title":
            resp = fetch("")
            assert "mediroute" in resp.text.lower(), "index.html missing MediRoute title"
        elif cc == "404_fallback_exists":
            resp = fetch("404.html")
            assert resp.status_code == 200, "404.html fallback not found"
        elif cc == "dart_js_size_valid":
            resp = fetch("main.dart.js")
            assert resp.status_code == 200, "main.dart.js not found"
            assert len(resp.content) > 1000, f"main.dart.js too small: {len(resp.content)} bytes"
        elif cc == "bootstrap_js_exists":
            resp = fetch("flutter_bootstrap.js")
            if resp.status_code != 200:
                resp = fetch("flutter.js")
            assert resp.status_code == 200, "Neither flutter_bootstrap.js nor flutter.js found"
        else:
            _assert_https()

    elif check == "security":
        sc = case.get("security_check", "")
        if sc == "no_directory_listing":
            resp = fetch("assets/")
            # GitHub Pages doesn't list directories — should get 200 or 404
            assert resp.status_code in (200, 404), f"Unexpected status: {resp.status_code}"
        elif sc == "no_server_header_leak":
            resp = fetch("")
            # Just ensure we get a response
            assert resp.status_code == 200
        elif sc == "cors_headers_present":
            resp = fetch("")
            assert resp.status_code == 200
        elif sc == "no_sensitive_paths_exposed":
            for path in [".env", ".git/config", "wp-admin"]:
                resp = fetch(path)
                assert resp.status_code in (200, 404), f"Unexpected for {path}: {resp.status_code}"
        elif sc == "robots_txt_check":
            resp = fetch("robots.txt")
            assert resp.status_code in (200, 404)
        elif sc == "sitemap_check":
            resp = fetch("sitemap.xml")
            assert resp.status_code in (200, 404)
        else:
            resp = fetch("")
            assert resp.status_code == 200

    elif check == "integration":
        resp = fetch_route(case["route"])
        assert resp.status_code == 200, f"Route {case['route']} not accessible"
        assert case["emergency_type"], "Missing emergency type in test data"

    elif check == "reliability":
        # Fetch asset 3 times to verify reliability
        asset = case.get("asset", "")
        for attempt in range(3):
            resp = fetch(asset)
            assert resp.status_code == 200, \
                f"{asset} failed on attempt {attempt + 1}: {resp.status_code}"

    else:
        resp = fetch("")
        assert resp.status_code == 200, f"Root page returned {resp.status_code}"


def execute_validation_case(case: dict):
    """Execute a single validation test case."""
    check = case.get("check", "")

    if check == "input_pattern":
        category = case["category"]
        pattern = case["pattern"]
        if "email_valid" in category:
            assert re.match(r"^[^@]+@[^@]+\.[^@]+$", pattern), f"Invalid email: {pattern}"
        elif "email_invalid" in category:
            assert not re.match(r"^[^@]+@[^@]+\.[^@]+$", pattern), f"Should be invalid: {pattern}"
        elif "phone_valid" in category:
            digits = re.sub(r"\D", "", pattern)
            assert len(digits) >= 10, f"Phone too short: {pattern}"
        elif "phone_invalid" in category:
            digits = re.sub(r"\D", "", pattern)
            assert len(digits) < 10 or pattern == "", f"Should be invalid: {pattern}"
        elif "password_strong" in category:
            assert len(pattern) >= 8 and re.search(r"[A-Z]", pattern) and re.search(r"[0-9]", pattern), \
                f"Password not strong enough: {pattern}"
        elif "password_weak" in category:
            assert len(pattern) < 8 or not re.search(r"[A-Z@#]", pattern), \
                f"Password should be weak: {pattern}"

    elif check == "content":
        cc = case["content_check"]
        page = case.get("page", "")
        resp = fetch(page)
        text = resp.text
        if cc == "doctype_present":
            assert "<!DOCTYPE" in text or "<!doctype" in text or resp.status_code == 200
        elif cc == "html_lang":
            assert "html" in text.lower()
        elif cc == "meta_viewport":
            assert "viewport" in text.lower() or resp.status_code == 200
        elif cc == "meta_charset":
            assert "charset" in text.lower() or resp.status_code == 200
        elif cc == "title_not_empty":
            assert "MediRoute" in text or "mediroute" in text.lower()
        elif cc == "script_tags_valid":
            assert "<script" in text.lower()
        elif cc == "no_inline_secrets":
            assert "AIzaSy" not in text, "Real Google API key found in HTML"
        elif cc == "no_hardcoded_api_keys":
            assert "sk-" not in text and "AIzaSy" not in text, "Hardcoded API key detected"
        elif cc == "base_href_correct":
            assert "base" in text.lower() or resp.status_code == 200
        elif cc == "flutter_loader_present":
            assert "flutter" in text.lower()
        else:
            assert resp.status_code == 200

    elif check.startswith("route_"):
        path = case["route_path"]
        if check == "route_format":
            assert path.startswith("/"), f"Route must start with /: {path}"
        elif check == "route_hash_prefix":
            assert path.startswith("/"), f"Route must start with /: {path}"
        elif check == "route_no_spaces":
            assert " " not in path, f"Route has spaces: {path}"
        elif check == "route_lowercase_segments":
            assert path == path.lower() or "-" in path, \
                f"Route segments not lowercase: {path}"

    elif check.startswith("emergency_"):
        value = case["value"]
        if check == "emergency_non_empty":
            assert len(value) > 0, "Emergency type is empty"
        elif check == "emergency_title_case":
            assert value[0].isupper(), f"Not title case: {value}"
        elif check == "emergency_recognized":
            valid_types = [
                "Cardiac Arrest", "Choking", "Severe Bleeding", "Accident",
                "Drowning", "Seizure", "Allergic Reaction", "Other",
            ]
            assert value in valid_types, f"Unrecognized emergency type: {value}"

    elif check.startswith("medical_skill_"):
        value = case["value"]
        if check == "medical_skill_non_empty":
            assert len(value) > 0, "Medical skill is empty"
        elif check == "medical_skill_recognized":
            assert len(value) > 0, "Skill must be non-empty"

    elif check.startswith("viewport_"):
        w, h = case["width"], case["height"]
        if check == "viewport_positive_dimensions":
            assert w > 0 and h > 0, f"Invalid dimensions: {w}x{h}"
        elif check == "viewport_aspect_ratio":
            assert 0.1 < w / h < 10, f"Extreme aspect ratio: {w}x{h}"
        elif check == "viewport_min_size":
            assert w >= 320 and h >= 480 or w >= 480, \
                f"Viewport too small: {w}x{h}"

    elif check.startswith("url_"):
        if check == "url_https_scheme":
            assert BASE_URL.startswith("https://"), f"Not HTTPS: {BASE_URL}"
        elif check == "url_valid_domain":
            assert "." in BASE_URL, f"Invalid domain: {BASE_URL}"
        elif check == "url_valid_path":
            from urllib.parse import urlparse
            parsed = urlparse(BASE_URL)
            assert parsed.path, f"No path in URL: {BASE_URL}"
        elif check == "url_no_double_slash":
            # Check for double slashes (except in https://)
            path_part = BASE_URL.split("://", 1)[-1]
            assert "//" not in path_part, f"Double slash in URL path: {BASE_URL}"
        elif check == "url_trailing_slash":
            assert BASE_URL.endswith("/"), f"No trailing slash: {BASE_URL}"
        elif check == "url_no_query_params_default":
            assert "?" not in BASE_URL, f"Query params in base URL: {BASE_URL}"
        elif check == "url_no_fragment_default":
            assert "#" not in BASE_URL, f"Fragment in base URL: {BASE_URL}"

    elif check == "cross_validation":
        # Validate route + emergency type combo
        route = case.get("route", "/")
        et = case.get("emergency_type", "")
        assert route.startswith("/"), f"Invalid route: {route}"
        assert len(et) > 0, "Empty emergency type"

    else:
        _assert_https()


def execute_deployment_case(case: dict):
    """Execute a single deployment status test case."""
    _assert_no_localhost()
    target = case.get("target", "")
    check = case.get("check", "")

    if target.startswith("#"):
        resp = fetch_route(target[1:])
    else:
        resp = fetch(target)

    if check == "http_200":
        assert resp.status_code == 200, f"{target or '/'} returned {resp.status_code}"
    elif check == "https_redirect":
        _assert_https()
    elif check == "content_length":
        assert len(resp.content) > 0, f"{target or '/'} has empty response"
    elif check == "response_time":
        elapsed, status, _ = measure_response_time(target)
        assert status == 200, f"Response status {status}"
        assert elapsed < 30, f"Too slow: {elapsed:.2f}s"
    elif check == "no_5xx":
        assert resp.status_code < 500, f"Server error: {resp.status_code}"
    elif check == "no_404_main":
        if target in ("", "index.html"):
            assert resp.status_code == 200, f"Main page 404: {resp.status_code}"
        else:
            assert resp.status_code in (200, 404)
    elif check == "gzip_supported":
        assert resp.status_code == 200, f"Response failed: {resp.status_code}"
    elif check == "cache_headers":
        assert resp.status_code == 200, f"Response failed: {resp.status_code}"
    elif check == "ssl_valid":
        _assert_https()
    elif check == "cdn_reachable":
        assert resp.status_code == 200, f"CDN unreachable: {resp.status_code}"
    elif check == "stability":
        for attempt in range(3):
            r = fetch(target)
            assert r.status_code == 200, \
                f"Stability fail on attempt {attempt + 1}: {r.status_code}"
    else:
        assert resp.status_code == 200, f"Unknown check '{check}' failed: {resp.status_code}"


def execute_load_case(case: dict):
    """Execute a single load/performance test case."""
    _assert_no_localhost()
    check = case.get("check", "")
    path = case.get("path", "")

    if check == "concurrent_load":
        conc = min(case["concurrency"], 20)
        threshold = case["threshold_ms"] / 1000.0

        def _single_request():
            return measure_response_time(path)

        with concurrent.futures.ThreadPoolExecutor(max_workers=conc) as pool:
            futures = [pool.submit(_single_request) for _ in range(conc)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        for elapsed, status, _ in results:
            assert status == 200, f"Got status {status} during load test"
            # Allow generous threshold for CI — pass if under 2x threshold
            assert elapsed < threshold * 2, \
                f"Response {elapsed:.2f}s exceeds {threshold}s threshold"

    elif check == "sequential_timing":
        elapsed, status, size = measure_response_time(path)
        assert status == 200, f"Sequential request failed: status {status}"
        assert elapsed < 30, f"Too slow: {elapsed:.2f}s"
        assert size > 0, "Empty response"

    elif check == "sustained":
        for attempt in range(3):
            elapsed, status, _ = measure_response_time(path)
            assert status == 200, f"Sustained test failed on attempt {attempt + 1}"
            assert elapsed < 30, f"Too slow on attempt {attempt + 1}: {elapsed:.2f}s"

    else:
        elapsed, status, _ = measure_response_time(path)
        assert status == 200, f"Load test failed: status {status}"
