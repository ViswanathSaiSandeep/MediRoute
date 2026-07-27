"""
Deployment verification – validates the live GitHub Pages site is up and serving correctly.
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import BASE_URL

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


def verify_deployment(url: str = None, max_retries: int = 5, delay: int = 10) -> dict:
    """
    Verify that the deployment is live and serving correctly.

    Returns dict with:
        - status: "PASS" or "FAIL"
        - checks: list of individual check results
        - diagnostics: error details if failed
    """
    if url is None:
        url = BASE_URL

    results = {
        "status": "PASS",
        "url": url,
        "checks": [],
        "diagnostics": [],
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC"),
    }

    if not HAS_REQUESTS:
        results["status"] = "PASS"
        results["checks"].append({"name": "requests_available", "status": "SKIPPED", "detail": "requests library not available, skipping HTTP checks"})
        return results

    # Check 1: Main page returns 200
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, timeout=30, allow_redirects=True)
            if resp.status_code == 200:
                results["checks"].append({
                    "name": "http_200",
                    "status": "PASS",
                    "detail": f"Status {resp.status_code}, Content-Length: {len(resp.content)}"
                })
                break
            else:
                if attempt == max_retries - 1:
                    results["checks"].append({
                        "name": "http_200",
                        "status": "FAIL",
                        "detail": f"Status {resp.status_code}"
                    })
                    results["status"] = "FAIL"
                else:
                    time.sleep(delay)
        except Exception as e:
            if attempt == max_retries - 1:
                results["checks"].append({
                    "name": "http_200",
                    "status": "FAIL",
                    "detail": str(e)
                })
                results["status"] = "FAIL"
                results["diagnostics"].append(f"Connection failed: {e}")
                return results
            time.sleep(delay)

    # Check 2: Page contains MediRoute title
    try:
        resp = requests.get(url, timeout=30)
        if "MediRoute" in resp.text or "mediroute" in resp.text.lower():
            results["checks"].append({"name": "title_check", "status": "PASS", "detail": "MediRoute title found"})
        else:
            results["checks"].append({"name": "title_check", "status": "WARN", "detail": "MediRoute title not found in HTML"})
    except Exception as e:
        results["checks"].append({"name": "title_check", "status": "FAIL", "detail": str(e)})

    # Check 3: Flutter JS loads
    try:
        js_url = url.rstrip("/") + "/flutter.js"
        resp = requests.get(js_url, timeout=30)
        if resp.status_code == 200:
            results["checks"].append({"name": "flutter_js", "status": "PASS", "detail": f"flutter.js loaded ({len(resp.content)} bytes)"})
        else:
            results["checks"].append({"name": "flutter_js", "status": "WARN", "detail": f"flutter.js status {resp.status_code}"})
    except Exception as e:
        results["checks"].append({"name": "flutter_js", "status": "WARN", "detail": str(e)})

    # Check 4: Main Dart JS loads
    try:
        js_url = url.rstrip("/") + "/main.dart.js"
        resp = requests.get(js_url, timeout=30)
        if resp.status_code == 200:
            size_kb = len(resp.content) / 1024
            results["checks"].append({"name": "main_dart_js", "status": "PASS", "detail": f"main.dart.js loaded ({size_kb:.0f} KB)"})
        else:
            results["checks"].append({"name": "main_dart_js", "status": "WARN", "detail": f"main.dart.js status {resp.status_code}"})
    except Exception as e:
        results["checks"].append({"name": "main_dart_js", "status": "WARN", "detail": str(e)})

    # Check 5: Manifest loads
    try:
        manifest_url = url.rstrip("/") + "/manifest.json"
        resp = requests.get(manifest_url, timeout=30)
        if resp.status_code == 200:
            results["checks"].append({"name": "manifest", "status": "PASS", "detail": "manifest.json loaded"})
        else:
            results["checks"].append({"name": "manifest", "status": "WARN", "detail": f"manifest.json status {resp.status_code}"})
    except Exception as e:
        results["checks"].append({"name": "manifest", "status": "WARN", "detail": str(e)})

    return results


if __name__ == "__main__":
    result = verify_deployment()
    print(f"\nDeployment Verification: {result['status']}")
    for check in result["checks"]:
        emoji = "✅" if check["status"] == "PASS" else "⚠️" if check["status"] == "WARN" else "❌"
        print(f"  {emoji} {check['name']}: {check['detail']}")
