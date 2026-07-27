"""
Centralized configuration for the MediRoute Selenium Automation Framework.
All tests, page objects, and utilities read from this module.
BASE_URL is loaded from the environment variable BASE_URL.
"""

import os
import logging

# ── Deployment URL ──────────────────────────────────────────────────────────
BASE_URL = os.environ.get(
    "BASE_URL",
    "https://viswanathsaisandeep.github.io/MediRoute/"
)

# Ensure trailing slash for consistent path joining
if not BASE_URL.endswith("/"):
    BASE_URL += "/"

# ── Browser Configuration ──────────────────────────────────────────────────
BROWSER = os.environ.get("BROWSER", "chrome")
HEADLESS = os.environ.get("HEADLESS", "true").lower() == "true"
WINDOW_WIDTH = int(os.environ.get("WINDOW_WIDTH", "1920"))
WINDOW_HEIGHT = int(os.environ.get("WINDOW_HEIGHT", "1080"))

# ── Timeouts (seconds) ─────────────────────────────────────────────────────
IMPLICIT_WAIT = int(os.environ.get("IMPLICIT_WAIT", "10"))
EXPLICIT_WAIT = int(os.environ.get("EXPLICIT_WAIT", "20"))
PAGE_LOAD_TIMEOUT = int(os.environ.get("PAGE_LOAD_TIMEOUT", "60"))
FLUTTER_LOAD_TIMEOUT = int(os.environ.get("FLUTTER_LOAD_TIMEOUT", "30"))
DEPLOYMENT_WAIT = int(os.environ.get("DEPLOYMENT_WAIT", "60"))

# ── Retry Configuration ───────────────────────────────────────────────────
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", "2"))
RETRY_DELAY = int(os.environ.get("RETRY_DELAY", "3"))

# ── Paths ──────────────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "screenshots")
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# Ensure directories exist
for d in [REPORTS_DIR, SCREENSHOTS_DIR, LOGS_DIR, DATA_DIR]:
    os.makedirs(d, exist_ok=True)

# ── Logging Configuration ─────────────────────────────────────────────────
LOG_LEVEL = getattr(logging, os.environ.get("LOG_LEVEL", "INFO").upper(), logging.INFO)
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ── Parallel Execution ────────────────────────────────────────────────────
PARALLEL_WORKERS = int(os.environ.get("PARALLEL_WORKERS", "4"))

# ── Application Routes (from GoRouter) ────────────────────────────────────
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

# ── Emergency Types (from app_constants.dart) ─────────────────────────────
EMERGENCY_TYPES = [
    "Cardiac Arrest",
    "Choking",
    "Severe Bleeding",
    "Accident",
    "Drowning",
    "Seizure",
    "Allergic Reaction",
    "Other",
]

# ── Medical Skills ────────────────────────────────────────────────────────
MEDICAL_SKILLS = [
    "CPR Certified",
    "First Aid",
    "Nursing (RN/LPN)",
    "Doctor (MD/DO)",
    "EMT / Paramedic",
]

# ── Viewport Presets ──────────────────────────────────────────────────────
VIEWPORTS = {
    "mobile_s": (320, 568),
    "mobile_m": (375, 667),
    "mobile_l": (414, 896),
    "tablet": (768, 1024),
    "laptop": (1366, 768),
    "desktop": (1920, 1080),
    "wide": (2560, 1440),
}

# ── Pass/Fail Thresholds ─────────────────────────────────────────────────
PASS_THRESHOLD_PERCENT = 95
CRITICAL_FAIL_THRESHOLD_PERCENT = 5
