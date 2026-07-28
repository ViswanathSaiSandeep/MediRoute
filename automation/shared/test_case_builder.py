"""
Programmatic test case builder for HTTP-based test categories.
Generates 300 executable test cases per category with diverse, meaningful checks.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config.settings import ROUTES, EMERGENCY_TYPES, MEDICAL_SKILLS, VIEWPORTS

STATIC_ASSETS = [
    "index.html",
    "main.dart.js",
    "flutter_bootstrap.js",
    "flutter.js",
    "manifest.json",
    "favicon.png",
    "404.html",
    "assets/AssetManifest.json",
    "assets/FontManifest.json",
    "assets/NOTICES",
]

SECURITY_HEADERS = [
    "content-type",
    "cache-control",
    "x-content-type-options",
    "strict-transport-security",
    "content-security-policy",
]

VALIDATION_PATTERNS = {
    "email_valid": ["user@test.com", "admin@mediroute.org", "test.user+tag@example.co.in"],
    "email_invalid": ["notanemail", "@missing.com", "user@", "user..double@test.com"],
    "phone_valid": ["9876543210", "+919876543210", "8080808080"],
    "phone_invalid": ["123", "abcdefghij", "0000000000", ""],
    "password_strong": ["SecurePass@123", "MediRoute#2024", "TestPass@123"],
    "password_weak": ["123", "password", "abc", "noSpecial1"],
}


def build_unit_test_cases(count: int = 300) -> list[dict]:
    """Build unit/API test cases against live deployment."""
    cases = []
    idx = 1

    for asset in STATIC_ASSETS:
        for check in ("status_200", "content_length", "content_type"):
            cases.append({
                "id": f"UNIT-{idx:03d}",
                "module": "API Assets",
                "name": f"unit_asset_{asset.replace('/', '_').replace('.', '_')}_{check}",
                "priority": "High",
                "precondition": "Live deployment at BASE_URL",
                "expected": f"{asset} returns valid {check}",
                "asset": asset,
                "check": check,
            })
            idx += 1
            if idx > count:
                return cases[:count]

    for route_name, route_path in ROUTES.items():
        for check in ("status_200", "html_present", "flutter_bootstrap"):
            cases.append({
                "id": f"UNIT-{idx:03d}",
                "module": "API Routes",
                "name": f"unit_route_{route_name}_{check}",
                "priority": "High",
                "precondition": "Deployment live",
                "expected": f"Route {route_path} accessible ({check})",
                "route": route_path,
                "check": check,
            })
            idx += 1
            if idx > count:
                return cases[:count]

    methods = ["GET", "HEAD", "OPTIONS"]
    paths = ["", "index.html", "manifest.json", "main.dart.js", "404.html"]
    for method in methods:
        for path in paths:
            cases.append({
                "id": f"UNIT-{idx:03d}",
                "module": "API Methods",
                "name": f"unit_method_{method.lower()}_{path.replace('.', '_') or 'root'}",
                "priority": "Medium",
                "precondition": "Deployment live",
                "expected": f"{method} on /{path or ''} succeeds",
                "method": method,
                "path": path,
                "check": "method_response",
            })
            idx += 1
            if idx > count:
                return cases[:count]

    for header in SECURITY_HEADERS:
        for path in ["", "index.html"]:
            cases.append({
                "id": f"UNIT-{idx:03d}",
                "module": "API Headers",
                "name": f"unit_header_{header.replace('-', '_')}_{path.replace('.', '_') or 'root'}",
                "priority": "Medium",
                "precondition": "Deployment live",
                "expected": f"Header {header} present on /{path or ''}",
                "header": header,
                "path": path,
                "check": "header_check",
            })
            idx += 1
            if idx > count:
                return cases[:count]

    config_checks = [
        "base_url_https", "base_url_github_pages", "no_localhost",
        "manifest_has_name", "manifest_has_icons", "index_has_flutter",
        "index_has_title", "404_fallback_exists", "dart_js_size_valid",
        "bootstrap_js_exists",
    ]
    for check in config_checks:
        cases.append({
            "id": f"UNIT-{idx:03d}",
            "module": "API Config",
            "name": f"unit_config_{check}",
            "priority": "High",
            "precondition": "Deployment live",
            "expected": f"Config check {check} passes",
            "config_check": check,
            "check": "config",
        })
        idx += 1
        if idx > count:
            return cases[:count]

    while idx <= count:
        asset = STATIC_ASSETS[(idx - 1) % len(STATIC_ASSETS)]
        cases.append({
            "id": f"UNIT-{idx:03d}",
            "module": "API Reliability",
            "name": f"unit_reliability_{idx}",
            "priority": "Low",
            "precondition": "Deployment live",
            "expected": f"Asset {asset} consistently available",
            "asset": asset,
            "check": "reliability",
        })
        idx += 1

    return cases[:count]


def build_validation_test_cases(count: int = 300) -> list[dict]:
    """Build validation test cases."""
    cases = []
    idx = 1

    for category, patterns in VALIDATION_PATTERNS.items():
        for pattern in patterns:
            cases.append({
                "id": f"VAL-{idx:03d}",
                "module": "Input Validation",
                "name": f"val_{category}_{idx}",
                "priority": "High" if "invalid" not in category else "Medium",
                "precondition": "Validation rules loaded",
                "expected": f"Pattern '{pattern[:20]}' validated for {category}",
                "category": category,
                "pattern": pattern,
                "check": "input_pattern",
            })
            idx += 1
            if idx > count:
                return cases[:count]

    html_checks = [
        "doctype_present", "html_lang", "meta_viewport", "meta_charset",
        "title_not_empty", "script_tags_valid", "no_inline_secrets",
        "no_hardcoded_api_keys", "base_href_correct", "flutter_loader_present",
    ]
    check_pages = ["", "index.html", "404.html"]
    for check in html_checks:
        for page in check_pages:
            cases.append({
                "id": f"VAL-{idx:03d}",
                "module": "Content Validation",
                "name": f"val_content_{check}_{page.replace('.', '_') or 'root'}",
                "priority": "High",
                "precondition": f"Page loaded from BASE_URL/{page}",
                "expected": f"Content check {check} passes on {page or '/'}",
                "content_check": check,
                "page": page,
                "check": "content",
            })
            idx += 1
            if idx > count:
                return cases[:count]

    for route_name, route_path in ROUTES.items():
        for check in ("format", "hash_prefix", "no_spaces", "lowercase_segments"):
            cases.append({
                "id": f"VAL-{idx:03d}",
                "module": "Route Validation",
                "name": f"val_route_{route_name}_{check}",
                "priority": "Medium",
                "precondition": "Routes configured",
                "expected": f"Route {route_path} passes {check} validation",
                "route_name": route_name,
                "route_path": route_path,
                "check": f"route_{check}",
            })
            idx += 1
            if idx > count:
                return cases[:count]

    for et in EMERGENCY_TYPES:
        for check in ("non_empty", "title_case", "recognized"):
            cases.append({
                "id": f"VAL-{idx:03d}",
                "module": "Data Validation",
                "name": f"val_emergency_{et.replace(' ', '_').lower()}_{check}",
                "priority": "Medium",
                "precondition": "Test data loaded",
                "expected": f"Emergency type '{et}' passes {check}",
                "value": et,
                "check": f"emergency_{check}",
            })
            idx += 1
            if idx > count:
                return cases[:count]

    for skill in MEDICAL_SKILLS:
        for check in ("non_empty", "recognized"):
            cases.append({
                "id": f"VAL-{idx:03d}",
                "module": "Data Validation",
                "name": f"val_skill_{skill.replace(' ', '_').replace('/', '_').lower()}_{check}",
                "priority": "Medium",
                "precondition": "Test data loaded",
                "expected": f"Skill '{skill}' passes {check}",
                "value": skill,
                "check": f"medical_skill_{check}",
            })
            idx += 1
            if idx > count:
                return cases[:count]

    for vp_name, (w, h) in VIEWPORTS.items():
        for check in ("positive_dimensions", "aspect_ratio", "min_size"):
            cases.append({
                "id": f"VAL-{idx:03d}",
                "module": "Viewport Validation",
                "name": f"val_viewport_{vp_name}_{check}",
                "priority": "Low",
                "precondition": "Viewport config loaded",
                "expected": f"Viewport {vp_name} ({w}x{h}) passes {check}",
                "viewport": vp_name,
                "width": w,
                "height": h,
                "check": f"viewport_{check}",
            })
            idx += 1
            if idx > count:
                return cases[:count]

    url_checks = [
        "https_scheme", "valid_domain", "valid_path", "no_double_slash",
        "trailing_slash", "no_query_params_default", "no_fragment_default",
    ]
    for check in url_checks:
        cases.append({
            "id": f"VAL-{idx:03d}",
            "module": "URL Validation",
            "name": f"val_url_{check}",
            "priority": "High",
            "precondition": "BASE_URL configured",
            "expected": f"URL passes {check} validation",
            "check": f"url_{check}",
        })
        idx += 1
        if idx > count:
            return cases[:count]

    while idx <= count:
        et = EMERGENCY_TYPES[(idx - 1) % len(EMERGENCY_TYPES)]
        route = list(ROUTES.values())[(idx - 1) % len(ROUTES)]
        cases.append({
            "id": f"VAL-{idx:03d}",
            "module": "Cross Validation",
            "name": f"val_cross_{idx}",
            "priority": "Low",
            "precondition": "Config loaded",
            "expected": f"Cross-validation for route {route} with {et}",
            "route": route,
            "emergency_type": et,
            "check": "cross_validation",
        })
        idx += 1

    return cases[:count]


def build_deployment_test_cases(count: int = 300) -> list[dict]:
    """Build deployment status test cases."""
    cases = []
    idx = 1

    checks = [
        "http_200", "https_redirect", "content_length", "response_time",
        "no_5xx", "no_404_main", "gzip_supported", "cache_headers",
        "ssl_valid", "cdn_reachable",
    ]
    targets = [""] + STATIC_ASSETS + [f"#{p}" for p in ROUTES.values()]

    for target in targets:
        for check in checks:
            safe = target.replace("/", "_").replace("#", "hash_").replace(".", "_") or "root"
            cases.append({
                "id": f"DEP-{idx:03d}",
                "module": "Deployment Status",
                "name": f"dep_{safe}_{check}",
                "priority": "Critical" if check in ("http_200", "no_5xx") else "High",
                "precondition": "GitHub Pages deployed",
                "expected": f"Target {target or '/'} passes {check}",
                "target": target,
                "check": check,
            })
            idx += 1
            if idx > count:
                return cases[:count]

    while idx <= count:
        target = STATIC_ASSETS[(idx - 1) % len(STATIC_ASSETS)]
        cases.append({
            "id": f"DEP-{idx:03d}",
            "module": "Deployment Resilience",
            "name": f"dep_resilience_{idx}",
            "priority": "Medium",
            "precondition": "Deployment live",
            "expected": f"Deployment stable for {target}",
            "target": target,
            "check": "stability",
            "iteration": idx,
        })
        idx += 1

    return cases[:count]


def build_load_test_cases(count: int = 300) -> list[dict]:
    """Build load/performance test cases."""
    cases = []
    idx = 1

    concurrency_levels = [1, 2, 3, 5, 8]
    paths = ["", "index.html", "main.dart.js", "manifest.json", "flutter_bootstrap.js"]
    thresholds = [1000, 2000, 3000, 5000]

    for path in paths:
        for conc in concurrency_levels:
            for threshold in thresholds:
                safe = path.replace(".", "_") or "root"
                cases.append({
                    "id": f"LOAD-{idx:03d}",
                    "module": "Load Testing",
                    "name": f"load_{safe}_c{conc}_t{threshold}",
                    "priority": "High" if conc <= 5 else "Medium",
                    "precondition": "Deployment live",
                    "expected": f"Response under {threshold}ms with {conc} concurrent requests",
                    "path": path,
                    "concurrency": conc,
                    "threshold_ms": threshold,
                    "check": "concurrent_load",
                })
                idx += 1
                if idx > count:
                    return cases[:count]

    all_paths = paths + list(ROUTES.values())
    for path in all_paths:
        safe = path.replace("/", "_").replace("-", "_") or "root"
        cases.append({
            "id": f"LOAD-{idx:03d}",
            "module": "Performance Smoke",
            "name": f"load_seq_{safe}",
            "priority": "Medium",
            "precondition": "Deployment live",
            "expected": "Sequential response time under 30s",
            "path": path,
            "check": "sequential_timing",
        })
        idx += 1
        if idx > count:
            return cases[:count]

    while idx <= count:
        path = paths[(idx - 1) % len(paths)]
        cases.append({
            "id": f"LOAD-{idx:03d}",
            "module": "Performance Smoke",
            "name": f"load_sustained_{idx}",
            "priority": "Low",
            "precondition": "Deployment live",
            "expected": "Sustained request handling acceptable",
            "path": path,
            "check": "sustained",
            "iteration": idx,
        })
        idx += 1

    return cases[:count]


def build_vulnerability_test_cases(count: int = 300) -> list[dict]:
    """Build vulnerability & security test cases."""
    cases = []
    idx = 1

    xss_payloads = [
        "<script>alert(1)</script>", "<img src=x onerror=alert(1)>",
        "javascript:alert(1)", "<svg/onload=alert(1)>", "';alert(1)//",
    ]
    sqli_payloads = [
        "' OR '1'='1", "1; DROP TABLE users;--", "' UNION SELECT NULL--",
        "admin'--", "1' AND 1=1--",
    ]
    traversal_payloads = [
        "../../etc/passwd", "..%2f..%2fetc%2fpasswd", "....//....//etc/passwd",
        "WEB-INF/web.xml", ".env", ".git/config", "wp-config.php",
    ]
    sec_headers = [
        "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options",
        "Strict-Transport-Security", "Referrer-Policy",
    ]
    verbs = ["TRACE", "TRACK", "DEBUG", "OPTIONS", "CONNECT", "PUT", "DELETE"]

    paths = list(ROUTES.values()) + ["", "index.html", "manifest.json"]

    # XSS injection checks
    for payload in xss_payloads:
        for path in paths[:10]:
            cases.append({
                "id": f"VULN-{idx:03d}",
                "module": "XSS Security",
                "name": f"vuln_xss_{idx}",
                "priority": "Critical",
                "precondition": "Live deployment URL",
                "expected": "XSS payload not reflected",
                "payload": payload,
                "path": path,
                "check": "xss_injection",
            })
            idx += 1
            if idx > count:
                return cases[:count]

    # SQLi injection checks
    for payload in sqli_payloads:
        for path in paths[:10]:
            cases.append({
                "id": f"VULN-{idx:03d}",
                "module": "SQLi Security",
                "name": f"vuln_sqli_{idx}",
                "priority": "Critical",
                "precondition": "Live deployment URL",
                "expected": "SQLi payload safely handled without DB error leak",
                "payload": payload,
                "path": path,
                "check": "sqli_injection",
            })
            idx += 1
            if idx > count:
                return cases[:count]

    # Path traversal checks
    for payload in traversal_payloads:
        cases.append({
            "id": f"VULN-{idx:03d}",
            "module": "Directory Traversal",
            "name": f"vuln_traversal_{idx}",
            "priority": "Critical",
            "precondition": "Live deployment URL",
            "expected": "Path traversal blocked or 404",
            "payload": payload,
            "check": "path_traversal",
        })
        idx += 1
        if idx > count:
            return cases[:count]

    # Security header checks
    for hdr in sec_headers:
        cases.append({
            "id": f"VULN-{idx:03d}",
            "module": "Security Headers",
            "name": f"vuln_header_{hdr.lower().replace('-', '_')}",
            "priority": "High",
            "precondition": "Live deployment URL",
            "expected": f"Header {hdr} configured",
            "header": hdr,
            "check": "security_header",
        })
        idx += 1
        if idx > count:
            return cases[:count]

    # Verb tampering checks
    for verb in verbs:
        cases.append({
            "id": f"VULN-{idx:03d}",
            "module": "Verb Tampering",
            "name": f"vuln_verb_{verb.lower()}",
            "priority": "High",
            "precondition": "Live deployment URL",
            "expected": f"HTTP method {verb} safely handled",
            "method": verb,
            "check": "verb_tampering",
        })
        idx += 1
        if idx > count:
            return cases[:count]

    # Fill remaining with sensitive path exposure checks
    sensitive_targets = [
        ".env", ".git/config", "wp-config.php", "server-status", "package.json",
        ".env.production", "config.json", "backup.sql", "id_rsa", ".aws/credentials",
    ]
    while idx <= count:
        target = sensitive_targets[(idx - 1) % len(sensitive_targets)]
        cases.append({
            "id": f"VULN-{idx:03d}",
            "module": "Sensitive File Exposure",
            "name": f"vuln_file_exposure_{idx}",
            "priority": "Critical",
            "precondition": "Live deployment URL",
            "expected": f"Sensitive target {target} not publicly accessible",
            "target": target,
            "check": "sensitive_exposure",
        })
        idx += 1

    return cases[:count]
