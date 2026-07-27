"""
Test data constants for MediRoute Appium Android automation.
"""


class TestUsers:
    BYSTANDER = {
        "phone": "+919876543210",
        "name": "Test Bystander",
        "email": "bystander@test.com",
        "password": "TestPass@123",
    }
    VOLUNTEER = {
        "phone": "+919876543211",
        "name": "Test Volunteer",
        "email": "volunteer@test.com",
        "password": "VolPass@123",
        "skills": ["CPR Certified", "First Aid"],
    }
    HOSPITAL = {
        "name": "Test Hospital",
        "email": "hospital@test.com",
        "phone": "+919876543212",
        "password": "HospPass@123",
        "address": "123 Medical Lane, Test City",
        "license": "HOSP-TEST-001",
    }
    INVALID_USER = {
        "phone": "invalid",
        "name": "",
        "email": "not-an-email",
        "password": "short",
    }


class ValidationData:
    EMPTY_STRING = ""
    WHITESPACE_ONLY = "   "
    SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
    SQL_INJECTION = "'; DROP TABLE users; --"
    XSS_PAYLOAD = "<script>alert('xss')</script>"
    LONG_STRING = "A" * 5000
    UNICODE_STRING = "测试用户 テスト тест"
    EMOJI_STRING = "🚑🏥👨‍⚕️🩺"
    VALID_EMAIL = "test@example.com"
    INVALID_EMAILS = [
        "plaintext", "@missing.com", "missing@",
        "missing@.com", "double@@domain.com",
    ]
    VALID_PHONES = ["+919876543210", "+14155552671", "+442071234567"]
    INVALID_PHONES = ["abc", "123", "+1", "++919876543210"]
    BOUNDARY_NUMBERS = [0, -1, 1, 999999999, -999999999]


class EmergencyData:
    CARDIAC = {"type": "Cardiac Arrest", "lat": 13.0827, "lng": 80.2707, "desc": "Person collapsed"}
    ACCIDENT = {"type": "Accident", "lat": 12.9716, "lng": 77.5946, "desc": "Road accident"}
    CHOKING = {"type": "Choking", "lat": 17.3850, "lng": 78.4867, "desc": "Child choking"}


class PerformanceThresholds:
    APP_LAUNCH_MAX_MS = 10000
    SCREEN_TRANSITION_MAX_MS = 3000
    INPUT_RESPONSE_MAX_MS = 1000
    API_RESPONSE_MAX_MS = 5000
    SCROLL_FPS_MIN = 30
