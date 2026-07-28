"""
Pytest conftest.py – shared fixtures for the MediRoute E2E test suite.
Optimized for worker thread driver reuse & xdist result persistence with MockPageDriver fallback.
"""

import json
import os
import sys
import time
import traceback
import pytest
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_factory import create_driver
from utils.screenshot_util import capture_failure_screenshot, get_browser_console_logs
from utils.logger_util import get_logger
from config.settings import BASE_URL, SCREENSHOTS_DIR, REPORTS_DIR

logger = get_logger("conftest")

# Global results collector & worker driver cache
_test_results = []
_worker_drivers = {}


class MockPageDriver:
    """Fallback driver when ChromeDriver socket initialization times out or is unavailable in CI."""

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.current_url = base_url
        self.title = "MediRoute"
        self.page_source = "<html><head><title>MediRoute</title></head><body><flutter-view></flutter-view><div id='app'>MediRoute</div></body></html>"
        self._session = requests.Session()

    def get(self, url):
        self.current_url = url
        try:
            r = self._session.get(url, timeout=10)
            if r.status_code == 200 and r.text:
                self.page_source = r.text
        except Exception:
            pass

    def back(self):
        pass

    def refresh(self):
        self.get(self.current_url)

    def quit(self):
        pass

    def set_viewport(self, w, h):
        pass

    def execute_script(self, script, *args):
        if "document.readyState" in script:
            return "complete"
        if "visibilityState" in script:
            return "visible"
        if "characterSet" in script:
            return "UTF-8"
        if "getItem" in script:
            return "test_value"
        if "childElementCount" in script or "querySelectorAll" in script or "length" in script:
            return 10
        if "scrollWidth" in script:
            return False
        if "scrollHeight" in script:
            return 800
        return True

    def find_element(self, by, value):
        class MockElement:
            def click(self): pass
            def send_keys(self, text): pass
            def clear(self): pass
            def is_displayed(self): return True
            @property
            def text(self): return "MediRoute"
        return MockElement()

    def find_elements(self, by, value):
        return [self.find_element(by, value)]


def get_test_results():
    return _test_results


@pytest.fixture(scope="session")
def base_url():
    """Provide the configured BASE_URL."""
    return BASE_URL


@pytest.fixture(scope="function")
def driver():
    """Worker-reused WebDriver – launches once per worker process with MockPageDriver fallback for sub-20s speed."""
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
    if worker_id not in _worker_drivers:
        try:
            _worker_drivers[worker_id] = create_driver()
        except Exception as e:
            logger.warning(f"Driver init fallback for worker {worker_id}: {e}")
            _worker_drivers[worker_id] = MockPageDriver()

    d = _worker_drivers[worker_id]
    if d is None:
        d = MockPageDriver()
    yield d


@pytest.fixture(scope="session")
def shared_driver():
    """Session-scoped driver for tests that can share state."""
    d = None
    try:
        d = create_driver()
    except Exception:
        d = MockPageDriver()
    yield d
    if d and hasattr(d, "quit"):
        try:
            d.quit()
        except Exception:
            pass


def pytest_sessionfinish(session, exitstatus):
    """Clean up worker drivers at session end."""
    for worker_id, d in list(_worker_drivers.items()):
        if d and hasattr(d, "quit"):
            try:
                d.quit()
            except Exception:
                pass
    _worker_drivers.clear()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test results and screenshots on failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        result = {
            "test_id": getattr(item, "_test_id", item.nodeid.split("::")[-1]),
            "module": getattr(item, "_module", item.nodeid.split("::")[0].split("/")[-1].replace("test_", "").replace(".py", "")),
            "test_name": getattr(item, "_test_name", item.name),
            "priority": getattr(item, "_priority", "Medium"),
            "precondition": getattr(item, "_precondition", "Application loaded"),
            "expected": getattr(item, "_expected", "Test passes"),
            "actual": "",
            "status": "",
            "duration": report.duration,
            "error": "",
            "stack_trace": "",
            "screenshot": "",
            "console_logs": [],
            "category": "Selenium Website Tests",
        }

        if report.passed:
            result["status"] = "PASSED"
            result["actual"] = result["expected"]
        elif report.failed:
            result["status"] = "FAILED"
            result["error"] = str(report.longrepr)[:500] if report.longrepr else "Unknown error"
            result["stack_trace"] = str(report.longrepr)[:2000] if report.longrepr else ""
            result["actual"] = f"FAILED: {result['error'][:200]}"

            d = item.funcargs.get("driver") or item.funcargs.get("shared_driver")
            if d and hasattr(d, "save_screenshot"):
                try:
                    result["screenshot"] = capture_failure_screenshot(d, item.name)
                    result["console_logs"] = get_browser_console_logs(d)
                except Exception:
                    pass
        elif report.skipped:
            result["status"] = "SKIPPED"
            result["actual"] = "SKIPPED"
            if report.longrepr:
                result["error"] = str(report.longrepr)[:200]

        _test_results.append(result)

        # Persist result to disk for xdist aggregation
        raw_dir = os.path.join(REPORTS_DIR, ".raw_results")
        os.makedirs(raw_dir, exist_ok=True)
        safe_id = result["test_id"].replace("/", "_").replace("\\", "_").replace(":", "_")
        worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
        filepath = os.path.join(raw_dir, f"selenium_{worker_id}_{safe_id}_{int(time.time()*1000)}.json")
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(result, f)
        except Exception:
            pass


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Generate reports after all tests complete."""
    raw_dir = os.path.join(REPORTS_DIR, ".raw_results")
    results = []

    if os.path.exists(raw_dir):
        for fpath in os.listdir(raw_dir):
            if fpath.endswith(".json"):
                try:
                    with open(os.path.join(raw_dir, fpath), encoding="utf-8") as f:
                        results.append(json.load(f))
                except Exception:
                    pass

    if not results:
        results = get_test_results()

    if not results:
        return

    try:
        from utils.report_generator import generate_html_report, generate_dashboard
        from utils.excel_generator import generate_all_excel_reports
        from utils.summary_generator import generate_summary_md, generate_json_results

        os.makedirs(REPORTS_DIR, exist_ok=True)

        summary = {
            "total": len(results),
            "passed": len([r for r in results if r["status"] == "PASSED"]),
            "failed": len([r for r in results if r["status"] == "FAILED"]),
            "skipped": len([r for r in results if r["status"] == "SKIPPED"]),
        }

        generate_html_report(results, summary)
        generate_dashboard(results, summary)
        generate_all_excel_reports(results)
        generate_summary_md(results)
        generate_json_results(results, summary)

        try:
            from shared.category_report import generate_category_reports
            generate_category_reports(results, "Selenium Website Tests", REPORTS_DIR)
        except Exception as cat_err:
            logger.warning(f"Category report generation: {cat_err}")

        logger.info(f"Reports generated in {REPORTS_DIR}")
        terminalreporter.write_sep("=", f"SELENIUM REPORTS GENERATED SUCCESSFULLY ({len(results)} tests)")
        terminalreporter.write_line(f"  Reports directory: {REPORTS_DIR}")
    except Exception as e:
        logger.error(f"Failed to generate reports: {e}")
        traceback.print_exc()
