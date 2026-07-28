"""
Shared pytest hooks for HTTP-based test categories.
Supports parallel pytest-xdist worker process aggregation.
"""

import json
import os
import sys
import time
import traceback

_test_results = []


def get_category_results():
    return _test_results


def register_category_hooks(category_name: str, reports_dir: str):
    """Register pytest hooks for a test category.
    Returns (makereport_hook, terminal_summary_hook) for the caller to install.
    """

    def makereport_hook(item, call):
        """Hook wrapper for pytest_runtest_makereport."""
        outcome = yield
        report = outcome.get_result()

        if report.when == "call":
            case = getattr(item, "callspec", None)
            case_params = case.params.get("case", {}) if case else {}

            result = {
                "test_id": case_params.get("id", item.nodeid.split("::")[-1]),
                "module": case_params.get("module", category_name),
                "test_name": case_params.get("name", item.name),
                "priority": case_params.get("priority", "Medium"),
                "precondition": case_params.get("precondition", "Deployment live"),
                "expected": case_params.get("expected", "Test passes"),
                "actual": "",
                "status": "",
                "duration": report.duration,
                "error": "",
                "stack_trace": "",
                "category": category_name,
            }

            if report.passed:
                result["status"] = "PASSED"
                result["actual"] = result["expected"]
            elif report.failed:
                result["status"] = "FAILED"
                result["error"] = str(report.longrepr)[:500] if report.longrepr else "Unknown"
                result["stack_trace"] = str(report.longrepr)[:2000] if report.longrepr else ""
                result["actual"] = f"FAILED: {result['error'][:200]}"
            elif report.skipped:
                result["status"] = "SKIPPED"
                result["actual"] = "SKIPPED"

            _test_results.append(result)

            # Persist to disk for xdist worker aggregation
            raw_dir = os.path.join(reports_dir, ".raw_results")
            os.makedirs(raw_dir, exist_ok=True)
            safe_id = result["test_id"].replace("/", "_").replace("\\", "_").replace(":", "_")
            worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
            filepath = os.path.join(raw_dir, f"{worker_id}_{safe_id}_{int(time.time()*1000)}.json")
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(result, f)
            except Exception:
                pass

    def terminal_summary_hook(terminalreporter, exitstatus, config):
        """Hook for pytest_terminal_summary — aggregates raw results and generates category reports."""
        raw_dir = os.path.join(reports_dir, ".raw_results")
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
            results = list(_test_results)

        if not results:
            return

        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
            from shared.category_report import generate_category_reports
            os.makedirs(reports_dir, exist_ok=True)
            generate_category_reports(results, category_name, reports_dir)
            terminalreporter.write_sep("=", f"{category_name.upper()} REPORTS GENERATED ({len(results)} tests)")
            terminalreporter.write_line(f"  Reports directory: {reports_dir}")
        except Exception as e:
            print(f"[{category_name}] Report generation failed: {e}")
            traceback.print_exc()

    return makereport_hook, terminal_summary_hook
