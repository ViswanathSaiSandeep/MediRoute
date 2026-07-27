# MediRoute Appium Android Automation Framework

## Overview

Enterprise-grade Appium E2E testing framework for the MediRoute Android application.
Uses UiAutomator2 automation with the Page Object Model pattern.

## Test Suite Summary

| Module | Test File | Test Cases |
|--------|-----------|------------|
| Authentication | `test_auth_appium.py` | 50 |
| Navigation | `test_navigation_appium.py` | 50 |
| UI Validation | `test_ui_appium.py` | 50 |
| Forms & Input | `test_forms_appium.py` | 50 |
| Performance | `test_performance_appium.py` | 50 |
| Validation | `test_validation_appium.py` | 50 |
| Regression | `test_regression_appium.py` | 50 |
| **Total** | | **350** |

## Architecture

```
appium/
├── config/
│   ├── appium_settings.py     # Centralized env-driven settings
│   └── test_data.py           # Test data constants
├── pages/
│   ├── base_screen.py         # Base page object (all interactions)
│   └── all_screens.py         # Screen-specific page objects
├── tests/
│   ├── conftest.py            # Shared fixtures & report hooks
│   ├── test_auth_appium.py    # Authentication (50 TCs)
│   ├── test_navigation_appium.py   # Navigation (50 TCs)
│   ├── test_ui_appium.py      # UI Validation (50 TCs)
│   ├── test_forms_appium.py   # Forms (50 TCs)
│   ├── test_performance_appium.py  # Performance (50 TCs)
│   ├── test_validation_appium.py   # Validation (50 TCs)
│   └── test_regression_appium.py   # Regression (50 TCs)
├── utils/
│   ├── appium_driver_factory.py    # Driver creation
│   └── appium_report_generator.py  # Excel/Markdown/JSON reports
├── requirements.txt
├── pytest.ini
└── README.md
```

## Prerequisites

- Python 3.10+
- Node.js 16+
- Android SDK (API 34+)
- Appium 2.x (`npm install -g appium`)
- UiAutomator2 driver (`appium driver install uiautomator2`)

## Running Tests

### CI/CD (GitHub Actions)
Tests run automatically on every push via `.github/workflows/deploy-and-test.yml`.
The workflow sets up an Android emulator and Appium server automatically.

### Locally
```bash
cd automation/appium
pip install -r requirements.txt
appium &     # Start Appium server
python -m pytest tests/ -v --tb=short
```

## Reports Generated

- `Appium_Test_Report.xlsx` — Full report (6 sheets)
- `Appium_Failed_Test_Cases.xlsx` — Failed tests detail
- `Appium_Passed_Test_Cases.xlsx` — Passed tests detail
- `Appium_Summary_Report.xlsx` — Executive summary
- `summary.md` — GitHub Actions summary
- `execution-results.json` — Machine-readable results

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APPIUM_HOST` | `127.0.0.1` | Appium server host |
| `APPIUM_PORT` | `4723` | Appium server port |
| `DEVICE_NAME` | `emulator-5554` | Android device name |
| `APP_PACKAGE` | `com.mediroute.app` | Application package |
| `PLATFORM_VERSION` | `14` | Android API level |
| `APK_PATH` | `` | Path to APK (optional) |
| `BASE_URL` | GitHub Pages URL | For WebView testing |
