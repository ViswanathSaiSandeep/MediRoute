/// Application-wide constants for MediRoute.
class AppConstants {
  AppConstants._();

  // ── App Meta ──
  static const String appName = 'MediRoute';
  static const String tagline = 'Help arrives faster.';
  static const String version = '1.0.0';

  // ── Emergency Config ──
  /// Radius in kilometers to search for nearby volunteers.
  static const double volunteerSearchRadiusKm = 1.0;

  /// Duration in seconds the SOS button must be held to trigger.
  static const int sosHoldDurationSeconds = 3;

  /// Timeout in seconds for volunteer to accept an alert.
  static const int alertTimeoutSeconds = 10;

  // ── Emergency Types ──
  static const List<String> emergencyTypes = [
    'Cardiac Arrest',
    'Choking',
    'Severe Bleeding',
    'Accident',
    'Drowning',
    'Seizure',
    'Allergic Reaction',
    'Other',
  ];

  // ── Medical Skills ──
  static const List<String> medicalSkills = [
    'CPR Certified',
    'First Aid',
    'Nursing (RN/LPN)',
    'Doctor (MD/DO)',
    'EMT / Paramedic',
  ];

  // ── Firestore Collections ──
  static const String usersCollection = 'users';
  static const String emergenciesCollection = 'emergencies';
  static const String responsesCollection = 'responses';
  static const String hospitalsCollection = 'hospitals';
  static const String hospitalAlertsSubcollection = 'hospital_alerts';

  // ── Emergency Number (India) ──
  static const String emergencyNumber = '108';
}
