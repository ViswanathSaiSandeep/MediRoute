"""
Centralized configuration for the MediRoute Appium Android Automation Framework.
All settings are driven by environment variables for CI/CD compatibility.
"""

import os
import logging

# ── Appium Server ──────────────────────────────────────────────────────────
APPIUM_HOST = os.environ.get("APPIUM_HOST", "127.0.0.1")
APPIUM_PORT = int(os.environ.get("APPIUM_PORT", "4723"))
APPIUM_URL = f"http://{APPIUM_HOST}:{APPIUM_PORT}"

# ── Android Capabilities ──────────────────────────────────────────────────
PLATFORM_NAME = "Android"
AUTOMATION_NAME = "UiAutomator2"
DEVICE_NAME = os.environ.get("DEVICE_NAME", "emulator-5554")
APP_PACKAGE = os.environ.get("APP_PACKAGE", "com.mediroute.app")
APP_ACTIVITY = os.environ.get("APP_ACTIVITY", ".MainActivity")
PLATFORM_VERSION = os.environ.get("PLATFORM_VERSION", "14")
APK_PATH = os.environ.get("APK_PATH", "")

# ── Deployment URL (for WebView testing) ──────────────────────────────────
BASE_URL = os.environ.get(
    "BASE_URL",
    "https://viswanathsaisandeep.github.io/MediRoute/"
)
if not BASE_URL.endswith("/"):
    BASE_URL += "/"

# ── Timeouts (seconds) ────────────────────────────────────────────────────
IMPLICIT_WAIT = int(os.environ.get("IMPLICIT_WAIT", "15"))
EXPLICIT_WAIT = int(os.environ.get("EXPLICIT_WAIT", "30"))
APP_LAUNCH_TIMEOUT = int(os.environ.get("APP_LAUNCH_TIMEOUT", "60000"))
NEW_COMMAND_TIMEOUT = int(os.environ.get("NEW_COMMAND_TIMEOUT", "300"))

# ── Retry Configuration ──────────────────────────────────────────────────
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", "2"))
RETRY_DELAY = int(os.environ.get("RETRY_DELAY", "3"))

# ── Paths ─────────────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "screenshots")
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")

for d in [REPORTS_DIR, SCREENSHOTS_DIR, LOGS_DIR]:
    os.makedirs(d, exist_ok=True)

# ── Logging ───────────────────────────────────────────────────────────────
LOG_LEVEL = getattr(logging, os.environ.get("LOG_LEVEL", "INFO").upper(), logging.INFO)
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s"

# ── Application Routes (Flutter hash-based routing) ───────────────────────
ROUTES = {
    "splash": "/",
    "role_selection": "/role-selection",
    "bystander_auth": "/bystander/auth",
    "bystander_home": "/bystander/home",
    "bystander_confirm": "/bystander/confirm",
    "bystander_first_aid": "/bystander/first-aid",
    "bystander_tracking": "/bystander/tracking",
    "bystander_hospital_alert": "/bystander/hospital-alert",
    "bystander_hospitals": "/bystander/hospitals",
    "hospital_register": "/hospital/register",
    "hospital_dashboard": "/hospital/dashboard",
    "volunteer_register": "/volunteer/register",
    "volunteer_dashboard": "/volunteer/dashboard",
    "volunteer_alert": "/volunteer/alert",
    "volunteer_navigation": "/volunteer/navigation",
    "volunteer_complete": "/volunteer/complete",
    "history": "/history",
    "profile": "/profile",
}

# ── Emergency Types ───────────────────────────────────────────────────────
EMERGENCY_TYPES = [
    "Cardiac Arrest", "Choking", "Severe Bleeding", "Accident",
    "Drowning", "Seizure", "Allergic Reaction", "Other",
]

# ── Medical Skills ────────────────────────────────────────────────────────
MEDICAL_SKILLS = [
    "CPR Certified", "First Aid", "Nursing (RN/LPN)",
    "Doctor (MD/DO)", "EMT / Paramedic",
]

# ── Pass/Fail Thresholds ─────────────────────────────────────────────────
PASS_THRESHOLD_PERCENT = 95
CRITICAL_FAIL_THRESHOLD_PERCENT = 5
