#!/usr/bin/env python3
"""
Main test runner for MediRoute Selenium Automation.
Executes all tests, generates reports, and outputs summary.
"""

import os
import sys
import time
import subprocess
import json

# Ensure automation directory is in path
AUTOMATION_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AUTOMATION_DIR)

from config.settings import BASE_URL, REPORTS_DIR, SCREENSHOTS_DIR, LOGS_DIR


def main():
    """Run the complete test suite."""
    print("=" * 70)
    print("  MediRoute Selenium Automation Framework")
    print("=" * 70)
    print(f"  BASE_URL:     {BASE_URL}")
    print(f"  Reports:      {REPORTS_DIR}")
    print(f"  Screenshots:  {SCREENSHOTS_DIR}")
    print(f"  Logs:         {LOGS_DIR}")
    print("=" * 70)

    # Ensure output directories exist
    for d in [REPORTS_DIR, SCREENSHOTS_DIR, LOGS_DIR]:
        os.makedirs(d, exist_ok=True)

    # Step 1: Verify deployment
    print("\n[1/3] Verifying deployment...")
    try:
        from utils.verify_deployment import verify_deployment
        result = verify_deployment()
        print(f"  Deployment Status: {result['status']}")
        for check in result.get("checks", []):
            emoji = "✅" if check["status"] == "PASS" else "⚠️" if check["status"] == "WARN" else "❌"
            print(f"  {emoji} {check['name']}: {check['detail']}")

        if result["status"] == "FAIL":
            print("\n❌ Deployment verification FAILED. Aborting tests.")
            sys.exit(1)
    except Exception as e:
        print(f"  ⚠️ Deployment verification skipped: {e}")

    # Step 2: Run tests
    print("\n[2/3] Running Selenium E2E tests...")
    start_time = time.time()

    pytest_args = [
        sys.executable, "-m", "pytest",
        os.path.join(AUTOMATION_DIR, "tests"),
        "-v",
        "--tb=short",
        "--no-header",
        f"--rootdir={AUTOMATION_DIR}",
    ]

    result = subprocess.run(
        pytest_args,
        cwd=AUTOMATION_DIR,
        capture_output=False,
        env={**os.environ, "PYTHONPATH": AUTOMATION_DIR},
    )

    elapsed = time.time() - start_time
    print(f"\n  Tests completed in {elapsed:.1f}s")
    print(f"  Exit code: {result.returncode}")

    # Step 3: Summary
    print("\n[3/3] Checking reports...")
    reports_exist = []
    for f in ["execution-report.html", "dashboard.html", "Automation_Test_Report.xlsx",
              "Failed_Test_Cases.xlsx", "Passed_Test_Cases.xlsx", "Summary_Report.xlsx",
              "summary.md", "execution-results.json"]:
        path = os.path.join(REPORTS_DIR, f)
        if os.path.exists(path):
            reports_exist.append(f)
            print(f"  ✅ {f}")
        else:
            print(f"  ❌ {f} (not generated)")

    screenshots = os.listdir(SCREENSHOTS_DIR) if os.path.exists(SCREENSHOTS_DIR) else []
    print(f"\n  📸 Screenshots captured: {len(screenshots)}")
    print(f"  📊 Reports generated: {len(reports_exist)}/8")

    print("\n" + "=" * 70)
    print("  Execution Complete")
    print("=" * 70)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
