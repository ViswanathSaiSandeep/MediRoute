"""
Test data constants for MediRoute Selenium automation.
Provides test users, form data, validation data, and boundary values.
"""


# ── Test User Credentials ─────────────────────────────────────────────────
class TestUsers:
    BYSTANDER = {
        "phone": "+919876543210",
        "name": "Test Bystander",
        "otp": "123456",
    }
    VOLUNTEER = {
        "phone": "+919876543211",
        "name": "Test Volunteer",
        "email": "volunteer@test.com",
        "skills": ["CPR Certified", "First Aid"],
    }
    HOSPITAL = {
        "name": "Test Hospital",
        "email": "hospital@test.com",
        "phone": "+919876543212",
        "address": "123 Medical Lane, Test City",
        "license": "HOSP-TEST-001",
    }
    INVALID_USER = {
        "phone": "invalid",
        "name": "",
        "email": "not-an-email",
    }
    ADMIN = {
        "email": "admin@mediroute.test",
        "password": "Admin@123",
    }


# ── Hospital Registration Data ────────────────────────────────────────────
class HospitalData:
    VALID = {
        "name": "City General Hospital",
        "registration_number": "REG-2024-001",
        "phone": "+914412345678",
        "email": "info@citygeneral.com",
        "address": "100 Hospital Road, Chennai",
        "beds_available": "250",
        "specialties": ["Cardiology", "Emergency", "Trauma"],
        "latitude": "13.0827",
        "longitude": "80.2707",
    }
    INVALID_NAME = {"name": ""}
    INVALID_PHONE = {"phone": "abc123"}
    INVALID_EMAIL = {"email": "not-valid"}
    DUPLICATE = {
        "name": "City General Hospital",
        "registration_number": "REG-2024-001",
    }


# ── Volunteer Registration Data ───────────────────────────────────────────
class VolunteerData:
    VALID = {
        "name": "John Responder",
        "phone": "+919876543213",
        "skills": ["CPR Certified", "First Aid"],
        "availability": "24/7",
    }
    MISSING_SKILLS = {
        "name": "Jane Doe",
        "phone": "+919876543214",
        "skills": [],
    }
    INVALID_PHONE = {
        "name": "Bad Phone User",
        "phone": "1234",
    }


# ── Emergency Data ────────────────────────────────────────────────────────
class EmergencyData:
    CARDIAC = {
        "type": "Cardiac Arrest",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "description": "Person collapsed, not breathing",
    }
    ACCIDENT = {
        "type": "Accident",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "description": "Road accident, multiple injuries",
    }
    CHOKING = {
        "type": "Choking",
        "latitude": 17.3850,
        "longitude": 78.4867,
        "description": "Child choking on food",
    }


# ── Form Validation Data ─────────────────────────────────────────────────
class ValidationData:
    EMPTY_STRING = ""
    WHITESPACE_ONLY = "   "
    SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
    SQL_INJECTION = "'; DROP TABLE users; --"
    XSS_PAYLOAD = "<script>alert('xss')</script>"
    LONG_STRING = "A" * 5000
    UNICODE_STRING = "测试用户 テストユーザー тест"
    EMOJI_STRING = "🚑🏥👨‍⚕️🩺"
    HTML_TAGS = "<b>Bold</b> <i>Italic</i>"
    VALID_EMAIL = "test@example.com"
    INVALID_EMAILS = [
        "plaintext",
        "@missing.com",
        "missing@",
        "missing@.com",
        "double@@domain.com",
        "spaces in@email.com",
    ]
    VALID_PHONES = [
        "+919876543210",
        "+14155552671",
        "+442071234567",
    ]
    INVALID_PHONES = [
        "abc",
        "123",
        "+1",
        "++919876543210",
        "+91 987 654 3210 000 000",
    ]
    BOUNDARY_NUMBERS = [0, -1, 1, 999999999, -999999999, 2147483647]


# ── Performance Thresholds ────────────────────────────────────────────────
class PerformanceThresholds:
    PAGE_LOAD_MAX_MS = 10000
    FIRST_PAINT_MAX_MS = 3000
    DOM_READY_MAX_MS = 5000
    JS_BUNDLE_MAX_KB = 5000
    TOTAL_REQUESTS_MAX = 50
    TOTAL_SIZE_MAX_KB = 10000


# ── Accessibility Standards ───────────────────────────────────────────────
class AccessibilityData:
    REQUIRED_ARIA_ROLES = ["button", "navigation", "main", "heading"]
    MIN_CONTRAST_RATIO = 4.5
    MIN_TOUCH_TARGET_PX = 44
    FOCUS_VISIBLE_ELEMENTS = ["button", "a", "input", "select", "textarea"]
