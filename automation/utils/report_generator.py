"""
HTML Report Generator – creates professional execution-report.html and dashboard.html.
"""

import os
import json
import time
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import REPORTS_DIR, BASE_URL


def generate_html_report(results: list, summary: dict, output_dir: str = None):
    """Generate the main execution-report.html."""
    if output_dir is None:
        output_dir = REPORTS_DIR

    passed = [r for r in results if r["status"] == "PASSED"]
    failed = [r for r in results if r["status"] == "FAILED"]
    skipped = [r for r in results if r["status"] == "SKIPPED"]

    total = len(results)
    pass_rate = (len(passed) / total * 100) if total > 0 else 0
    total_duration = sum(r.get("duration", 0) for r in results)

    # Build failure rows
    fail_rows = ""
    for r in failed:
        screenshot = r.get("screenshot", "")
        ss_link = f'<a href="../screenshots/{os.path.basename(screenshot)}" target="_blank">View</a>' if screenshot else "N/A"
        fail_rows += f"""
        <tr>
            <td>{r['test_id']}</td>
            <td>{r['module']}</td>
            <td>{r['test_name']}</td>
            <td class="status-fail">FAILED</td>
            <td>{r.get('error', 'Unknown')[:200]}</td>
            <td>{ss_link}</td>
            <td>{r.get('duration', 0):.2f}s</td>
        </tr>"""

    # Build all test rows
    all_rows = ""
    for r in results:
        status_class = {
            "PASSED": "status-pass",
            "FAILED": "status-fail",
            "SKIPPED": "status-skip",
        }.get(r["status"], "")
        all_rows += f"""
        <tr>
            <td>{r['test_id']}</td>
            <td>{r['module']}</td>
            <td>{r['test_name']}</td>
            <td class="{status_class}">{r['status']}</td>
            <td>{r['priority']}</td>
            <td>{r.get('duration', 0):.2f}s</td>
        </tr>"""

    # Module summary
    modules = {}
    for r in results:
        m = r["module"]
        if m not in modules:
            modules[m] = {"total": 0, "passed": 0, "failed": 0, "skipped": 0}
        modules[m]["total"] += 1
        modules[m][r["status"].lower()] = modules[m].get(r["status"].lower(), 0) + 1

    module_rows = ""
    for m, stats in sorted(modules.items()):
        rate = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
        module_rows += f"""
        <tr>
            <td>{m}</td>
            <td>{stats['total']}</td>
            <td class="status-pass">{stats['passed']}</td>
            <td class="status-fail">{stats['failed']}</td>
            <td class="status-skip">{stats['skipped']}</td>
            <td>{rate:.1f}%</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MediRoute E2E Test Execution Report</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f0f23; color: #e0e0e0; padding: 20px; }}
  .header {{ background: linear-gradient(135deg, #1a1a3e, #2d1b4e); padding: 30px; border-radius: 12px; margin-bottom: 24px; }}
  .header h1 {{ font-size: 28px; color: #00d4ff; margin-bottom: 8px; }}
  .header p {{ color: #a0a0c0; font-size: 14px; }}
  .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }}
  .metric-card {{ background: #1a1a3e; border-radius: 10px; padding: 20px; text-align: center; border: 1px solid #2a2a5e; }}
  .metric-card .value {{ font-size: 36px; font-weight: bold; }}
  .metric-card .label {{ font-size: 13px; color: #8888aa; margin-top: 4px; }}
  .pass {{ color: #00e676; }}
  .fail {{ color: #ff5252; }}
  .skip {{ color: #ffab40; }}
  .rate {{ color: #00d4ff; }}
  table {{ width: 100%; border-collapse: collapse; margin-bottom: 24px; background: #1a1a3e; border-radius: 10px; overflow: hidden; }}
  th {{ background: #2d1b4e; padding: 12px 16px; text-align: left; font-size: 13px; color: #a0a0c0; text-transform: uppercase; letter-spacing: 0.5px; }}
  td {{ padding: 10px 16px; border-bottom: 1px solid #2a2a5e; font-size: 13px; }}
  tr:hover {{ background: #22224a; }}
  .status-pass {{ color: #00e676; font-weight: bold; }}
  .status-fail {{ color: #ff5252; font-weight: bold; }}
  .status-skip {{ color: #ffab40; font-weight: bold; }}
  .section {{ margin-bottom: 32px; }}
  .section h2 {{ font-size: 20px; color: #00d4ff; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #2d1b4e; }}
  .chart-container {{ display: flex; gap: 24px; margin-bottom: 24px; flex-wrap: wrap; }}
  .pie-chart {{ width: 200px; height: 200px; border-radius: 50%; position: relative; }}
  .chart-legend {{ display: flex; flex-direction: column; gap: 8px; justify-content: center; }}
  .legend-item {{ display: flex; align-items: center; gap: 8px; font-size: 14px; }}
  .legend-dot {{ width: 12px; height: 12px; border-radius: 50%; }}
  a {{ color: #00d4ff; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<div class="header">
  <h1>🏥 MediRoute — E2E Test Execution Report</h1>
  <p>Deployment URL: {BASE_URL} | Executed: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
</div>

<div class="metrics">
  <div class="metric-card"><div class="value rate">{total}</div><div class="label">Total Tests</div></div>
  <div class="metric-card"><div class="value pass">{len(passed)}</div><div class="label">Passed</div></div>
  <div class="metric-card"><div class="value fail">{len(failed)}</div><div class="label">Failed</div></div>
  <div class="metric-card"><div class="value skip">{len(skipped)}</div><div class="label">Skipped</div></div>
  <div class="metric-card"><div class="value rate">{pass_rate:.1f}%</div><div class="label">Pass Rate</div></div>
  <div class="metric-card"><div class="value rate">{total_duration:.1f}s</div><div class="label">Duration</div></div>
</div>

<div class="section">
  <h2>📊 Module Summary</h2>
  <table>
    <thead><tr><th>Module</th><th>Total</th><th>Passed</th><th>Failed</th><th>Skipped</th><th>Pass Rate</th></tr></thead>
    <tbody>{module_rows}</tbody>
  </table>
</div>

<div class="section">
  <h2>❌ Failed Tests</h2>
  <table>
    <thead><tr><th>Test ID</th><th>Module</th><th>Test Name</th><th>Status</th><th>Error</th><th>Screenshot</th><th>Duration</th></tr></thead>
    <tbody>{fail_rows if fail_rows else '<tr><td colspan="7" style="text-align:center;color:#00e676;">No failures! 🎉</td></tr>'}</tbody>
  </table>
</div>

<div class="section">
  <h2>📋 All Test Results</h2>
  <table>
    <thead><tr><th>Test ID</th><th>Module</th><th>Test Name</th><th>Status</th><th>Priority</th><th>Duration</th></tr></thead>
    <tbody>{all_rows}</tbody>
  </table>
</div>

<div style="text-align:center;padding:20px;color:#555;">
  Generated by MediRoute Automation Framework | {time.strftime('%Y-%m-%d %H:%M:%S')}
</div>
</body>
</html>"""

    filepath = os.path.join(output_dir, "execution-report.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return filepath


def generate_dashboard(results: list, summary: dict, output_dir: str = None):
    """Generate the dashboard.html with visual charts."""
    if output_dir is None:
        output_dir = REPORTS_DIR

    passed = len([r for r in results if r["status"] == "PASSED"])
    failed = len([r for r in results if r["status"] == "FAILED"])
    skipped = len([r for r in results if r["status"] == "SKIPPED"])
    total = len(results)

    # Module data for bar chart
    modules = {}
    for r in results:
        m = r["module"]
        if m not in modules:
            modules[m] = {"passed": 0, "failed": 0, "skipped": 0}
        status_key = r["status"].lower()
        modules[m][status_key] = modules[m].get(status_key, 0) + 1

    module_labels = json.dumps(list(modules.keys()))
    module_passed = json.dumps([v["passed"] for v in modules.values()])
    module_failed = json.dumps([v["failed"] for v in modules.values()])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>MediRoute Test Dashboard</title>
<style>
  body {{ font-family: 'Segoe UI', sans-serif; background: #0f0f23; color: #e0e0e0; padding: 20px; }}
  .dashboard-header {{ background: linear-gradient(135deg, #1a1a3e, #2d1b4e); padding: 30px; border-radius: 12px; text-align: center; margin-bottom: 24px; }}
  .dashboard-header h1 {{ color: #00d4ff; font-size: 32px; }}
  .summary-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 32px; }}
  .summary-card {{ background: #1a1a3e; border-radius: 12px; padding: 24px; text-align: center; border: 1px solid #2a2a5e; }}
  .summary-card .number {{ font-size: 48px; font-weight: bold; }}
  .green {{ color: #00e676; }}
  .red {{ color: #ff5252; }}
  .orange {{ color: #ffab40; }}
  .blue {{ color: #00d4ff; }}
  .chart-section {{ background: #1a1a3e; border-radius: 12px; padding: 24px; margin-bottom: 24px; border: 1px solid #2a2a5e; }}
  .chart-section h2 {{ color: #00d4ff; margin-bottom: 16px; }}
  .bar {{ display: inline-block; height: 24px; border-radius: 4px; margin: 2px 0; }}
  .bar-pass {{ background: #00e676; }}
  .bar-fail {{ background: #ff5252; }}
  .module-row {{ display: flex; align-items: center; gap: 12px; margin: 8px 0; }}
  .module-name {{ width: 180px; font-size: 13px; text-align: right; }}
  .bar-container {{ flex: 1; display: flex; gap: 2px; }}
  .donut {{ width: 200px; height: 200px; border-radius: 50%; background: conic-gradient(#00e676 0% {passed/total*100 if total else 0}%, #ff5252 {passed/total*100 if total else 0}% {(passed+failed)/total*100 if total else 0}%, #ffab40 {(passed+failed)/total*100 if total else 0}% 100%); margin: 0 auto; display: flex; align-items: center; justify-content: center; }}
  .donut-hole {{ width: 120px; height: 120px; border-radius: 50%; background: #1a1a3e; display: flex; align-items: center; justify-content: center; flex-direction: column; }}
  .donut-label {{ font-size: 28px; font-weight: bold; color: #00d4ff; }}
</style>
</head>
<body>
<div class="dashboard-header">
  <h1>🏥 MediRoute Test Dashboard</h1>
  <p style="color:#8888aa;">Live E2E Execution Results | {time.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
</div>

<div class="summary-grid">
  <div class="summary-card"><div class="number green">{passed}</div><div>Passed</div></div>
  <div class="summary-card"><div class="number red">{failed}</div><div>Failed</div></div>
  <div class="summary-card"><div class="number orange">{skipped}</div><div>Skipped</div></div>
</div>

<div class="chart-section">
  <h2>Pass/Fail Distribution</h2>
  <div class="donut">
    <div class="donut-hole">
      <div class="donut-label">{passed/total*100 if total else 0:.0f}%</div>
      <div style="font-size:12px;color:#8888aa;">Pass Rate</div>
    </div>
  </div>
</div>

<div class="chart-section">
  <h2>Results by Module</h2>
  {''.join(f'''<div class="module-row">
    <div class="module-name">{m}</div>
    <div class="bar-container">
      <div class="bar bar-pass" style="width:{v['passed']*8}px;" title="{v['passed']} passed"></div>
      <div class="bar bar-fail" style="width:{v['failed']*8}px;" title="{v['failed']} failed"></div>
    </div>
    <div style="font-size:12px;color:#8888aa;">{v['passed']}/{v['passed']+v['failed']+v['skipped']}</div>
  </div>''' for m, v in modules.items())}
</div>

<div style="text-align:center;padding:20px;color:#555;">MediRoute Automation Dashboard | {time.strftime('%Y')}</div>
</body>
</html>"""

    filepath = os.path.join(output_dir, "dashboard.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return filepath
