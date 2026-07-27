# MediRoute Selenium E2E Automation Framework

Enterprise-grade Selenium automation framework for testing MediRoute against the **live GitHub Pages deployment**.

## 🏗️ Architecture

```
automation/
├── config/          # Configuration & test data
│   ├── settings.py  # BASE_URL, timeouts, routes
│   └── test_data.py # Users, hospitals, validation data
├── pages/           # Page Object Model
│   ├── base_page.py # Base POM with Flutter-aware helpers
│   └── all_pages.py # All screen page objects
├── tests/           # Test suites (470+ test cases)
│   ├── conftest.py  # Fixtures, hooks, auto-report generation
│   ├── test_authentication.py      # 40 tests
│   ├── test_authorization.py       # 40 tests
│   ├── test_navigation.py          # 30 tests
│   ├── test_ui_validation.py       # 50 tests
│   ├── test_forms.py               # 50 tests
│   ├── test_crud_operations.py     # 50 tests
│   ├── test_input_validation.py    # 40 tests
│   ├── test_error_handling.py      # 20 tests
│   ├── test_session_management.py  # 20 tests
│   ├── test_file_upload.py         # 20 tests
│   ├── test_accessibility.py       # 20 tests
│   ├── test_responsive_design.py   # 20 tests
│   ├── test_performance_smoke.py   # 20 tests
│   └── test_regression.py          # 50 tests
├── utils/           # Utilities
│   ├── driver_factory.py     # WebDriver setup
│   ├── screenshot_util.py    # Screenshot capture
│   ├── logger_util.py        # Structured logging
│   ├── retry_util.py         # Test retry decorator
│   ├── wait_util.py          # Explicit waits
│   ├── report_generator.py   # HTML reports
│   ├── excel_generator.py    # Excel reports
│   ├── summary_generator.py  # MD + JSON reports
│   └── verify_deployment.py  # Deployment checks
├── reports/         # Generated reports (runtime)
├── screenshots/     # Captured screenshots (runtime)
├── logs/            # Execution logs (runtime)
├── requirements.txt # Python dependencies
├── pytest.ini       # Pytest configuration
└── run_tests.py     # Main entry point
```

## 🚀 Local Execution

### Prerequisites
- Python 3.9+
- Google Chrome (latest)
- ChromeDriver (matching Chrome version)

### Setup
```bash
cd automation
pip install -r requirements.txt
```

### Run All Tests
```bash
# Against live deployment (default)
python run_tests.py

# Against custom URL
BASE_URL=https://your-site.github.io/MediRoute/ python run_tests.py

# Run specific test suite
python -m pytest tests/test_authentication.py -v

# Run with parallel execution
python -m pytest tests/ -n 4 -v
```

## 🔄 CI/CD Execution

The GitHub Actions workflow (`.github/workflows/deploy-and-test.yml`) runs automatically on:
- **Push** to main/master
- **Pull request** to main/master
- **Manual trigger** (workflow_dispatch)

### Pipeline Stages
1. Checkout → 2. Dependencies → 3. Build → 4. Analyze → 5. Deploy → 6. Wait → 7. Verify → 8. Test → 9. HTML Reports → 10. Excel Reports → 11. Upload → 12. Summary → 13. History

### GitHub Pages Setup
1. Go to **Settings → Pages**
2. Set Source: **Deploy from a branch**
3. Set Branch: **gh-pages** / **(root)**
4. The workflow creates `gh-pages` branch automatically on first push

### Required Permissions
The workflow needs `contents: write` and `pages: write` permissions (configured in YAML).

## 📊 Reports

| Report | Format | Description |
|--------|--------|-------------|
| Automation_Test_Report.xlsx | Excel | 6 sheets: All, Passed, Failed, Skipped, Metrics, Defects |
| Failed_Test_Cases.xlsx | Excel | Detailed failure analysis |
| Passed_Test_Cases.xlsx | Excel | Passed test evidence |
| Summary_Report.xlsx | Excel | Executive summary with module breakdown |
| execution-report.html | HTML | Full test results with screenshots |
| dashboard.html | HTML | Visual dashboard with charts |
| execution-results.json | JSON | Machine-readable results |
| summary.md | Markdown | GitHub Actions summary |

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `WebDriverException` | Ensure Chrome and ChromeDriver versions match |
| Tests timing out | Increase `EXPLICIT_WAIT` in settings.py |
| Deployment not found | Check BASE_URL; wait for GitHub Pages CDN propagation |
| All tests skipped | Verify the live URL is accessible |
| Import errors | Run from `automation/` directory; check PYTHONPATH |

## ⚙️ Configuration

All settings are in `config/settings.py`. Key environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `https://viswanathsaisandeep.github.io/MediRoute/` | Live deployment URL |
| `HEADLESS` | `true` | Run Chrome headless |
| `EXPLICIT_WAIT` | `20` | Element wait timeout (seconds) |
| `PARALLEL_WORKERS` | `4` | Parallel test workers |
