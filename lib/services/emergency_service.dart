import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:geolocator/geolocator.dart';
import 'package:uuid/uuid.dart';
import '../data/models/emergency_model.dart';
import '../core/constants/app_constants.dart';
import 'location_service.dart';
import 'hospital_service.dart';

/// Handles the full emergency lifecycle — create, accept, resolve, cancel.
class EmergencyService {
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;
  final LocationService _locationService = LocationService();
  final HospitalService _hospitalService = HospitalService();
  static const _uuid = Uuid();

  /// Create a new emergency SOS request.
  /// 1. Gets current GPS position
  /// 2. Writes emergency doc to Firestore
  /// 3. Finds nearest hospital and sends alert
  /// 4. Notifies nearby volunteers (stores their UIDs but does NOT auto-assign)
  /// Returns the created EmergencyModel.
  Future<EmergencyModel> createEmergency({
    required String bystanderUid,
    required String emergencyType,
  }) async {
    // Get current location
    final position = await _locationService.getCurrentPosition();
    final emergencyId = _uuid.v4();

    final emergency = EmergencyModel(
      emergencyId: emergencyId,
      bystanderUid: bystanderUid,
      type: emergencyType,
      latitude: position.latitude,
      longitude: position.longitude,
      geohash: '',
      timestamp: DateTime.now(),
      status: 'active',
    );

    // Write to Firestore
    await _firestore
        .collection(AppConstants.emergenciesCollection)
        .doc(emergencyId)
        .set(emergency.toJson());

    // Find nearest hospital and alert (best-effort)
    try {
      final hospital = await _hospitalService.findNearestHospital(
        latitude: position.latitude,
        longitude: position.longitude,
      );
      if (hospital != null) {
        await _hospitalService.sendHospitalAlert(
          emergencyId: emergencyId,
          hospitalId: hospital.id,
          emergencyType: emergencyType,
          latitude: position.latitude,
          longitude: position.longitude,
        );
        await _firestore
            .collection(AppConstants.emergenciesCollection)
            .doc(emergencyId)
            .update({'nearestHospitalId': hospital.id});
      }
    } catch (_) {}

    // Notify nearby volunteers (best-effort) — does NOT auto-assign
    try {
      await _notifyNearbyVolunteers(
        emergencyId: emergencyId,
        latitude: position.latitude,
        longitude: position.longitude,
      );
    } catch (_) {}

    return emergency;
  }

  /// Find all available volunteers within the search radius and store their
  /// UIDs in the emergency doc so they can be notified. The emergency status
  /// stays 'active' until a volunteer explicitly accepts.
  Future<void> _notifyNearbyVolunteers({
    required String emergencyId,
    required double latitude,
    required double longitude,
  }) async {
    // Query available volunteers
    final snapshot = await _firestore
        .collection(AppConstants.usersCollection)
        .where('role', isEqualTo: 'volunteer')
        .where('availability', isEqualTo: true)
        .get();

    if (snapshot.docs.isEmpty) return;

    final radiusMeters = AppConstants.volunteerSearchRadiusKm * 1000;
    final notifiedUids = <String>[];

    for (final doc in snapshot.docs) {
      final data = doc.data();
      // Get volunteer location
      final location = data['location'] as Map<String, dynamic>?;
      final geopoint = location?['geopoint'] as GeoPoint?;
      double? vLat = geopoint?.latitude;
      double? vLng = geopoint?.longitude;

      // Fallback to flat fields
      vLat ??= data['latitude'] as double?;
      vLng ??= data['longitude'] as double?;

      if (vLat == null || vLng == null) continue;

      final distance = Geolocator.distanceBetween(
        latitude,
        longitude,
        vLat,
        vLng,
      );

      // Within search radius
      if (distance <= radiusMeters) {
        final uid = data['uid'] as String?;
        if (uid != null) {
          notifiedUids.add(uid);
        }
      }
    }

    // Store list of notified volunteer UIDs in the emergency doc
    if (notifiedUids.isNotEmpty) {
      await _firestore
          .collection(AppConstants.emergenciesCollection)
          .doc(emergencyId)
          .update({'notifiedVolunteers': notifiedUids});
    }
  }

  /// Volunteer accepts an emergency.
  Future<void> acceptEmergency({
    required String emergencyId,
    required String volunteerUid,
  }) async {
    // Use a transaction to prevent race conditions (two volunteers accepting simultaneously)
    await _firestore.runTransaction((transaction) async {
      final docRef = _firestore
          .collection(AppConstants.emergenciesCollection)
          .doc(emergencyId);
      final snapshot = await transaction.get(docRef);

      if (!snapshot.exists) return;

      final currentStatus = snapshot.data()?['status'] as String?;

      // Only allow acceptance if still active (not already assigned)
      if (currentStatus != 'active') return;

      // Get volunteer name
      String volunteerName = 'Volunteer';
      try {
        final userDoc = await _firestore
            .collection(AppConstants.usersCollection)
            .doc(volunteerUid)
            .get();
        if (userDoc.exists) {
          volunteerName = userDoc.data()?['name'] as String? ?? 'Volunteer';
        }
      } catch (_) {}

      // Get volunteer's current location
      double? volunteerLat;
      double? volunteerLng;
      try {
        final userDoc = await _firestore
            .collection(AppConstants.usersCollection)
            .doc(volunteerUid)
            .get();
        if (userDoc.exists) {
          final data = userDoc.data()!;
          final location = data['location'] as Map<String, dynamic>?;
          final geopoint = location?['geopoint'] as GeoPoint?;
          volunteerLat = geopoint?.latitude ?? data['latitude'] as double?;
          volunteerLng = geopoint?.longitude ?? data['longitude'] as double?;
        }
      } catch (_) {}

      transaction.update(docRef, {
        'status': 'assigned',
        'volunteerAssigned': volunteerUid,
        'volunteerName': volunteerName,
        'volunteerLat': volunteerLat,
        'volunteerLng': volunteerLng,
      });
    });

    // Create a response document
    await _firestore.collection(AppConstants.responsesCollection).add({
      'emergencyId': emergencyId,
      'volunteerUid': volunteerUid,
      'acceptedAt': FieldValue.serverTimestamp(),
      'status': 'en_route',
    });

    // Mark volunteer as unavailable
    await _firestore
        .collection(AppConstants.usersCollection)
        .doc(volunteerUid)
        .update({'availability': false});
  }

  /// Mark emergency as resolved.
  Future<void> resolveEmergency({
    required String emergencyId,
    String? helpProvided,
    String? outcome,
  }) async {
    // Get volunteer UID to restore availability
    try {
      final doc = await _firestore
          .collection(AppConstants.emergenciesCollection)
          .doc(emergencyId)
          .get();
      final volunteerUid = doc.data()?['volunteerAssigned'] as String?;
      if (volunteerUid != null) {
        await _firestore
            .collection(AppConstants.usersCollection)
            .doc(volunteerUid)
            .update({'availability': true});
      }
    } catch (_) {}

    await _firestore
        .collection(AppConstants.emergenciesCollection)
        .doc(emergencyId)
        .update({
          'status': 'resolved',
          'resolvedAt': FieldValue.serverTimestamp(),
          'helpProvided': helpProvided,
          'outcome': outcome,
        });
  }

  /// Cancel an emergency.
  Future<void> cancelEmergency(String emergencyId) async {
    // Restore volunteer availability
    try {
      final doc = await _firestore
          .collection(AppConstants.emergenciesCollection)
          .doc(emergencyId)
          .get();
      final volunteerUid = doc.data()?['volunteerAssigned'] as String?;
      if (volunteerUid != null) {
        await _firestore
            .collection(AppConstants.usersCollection)
            .doc(volunteerUid)
            .update({'availability': true});
      }
    } catch (_) {}

    await _firestore
        .collection(AppConstants.emergenciesCollection)
        .doc(emergencyId)
        .update({'status': 'cancelled'});
  }

  /// Stream active emergencies (for volunteer dashboard).
  Stream<List<EmergencyModel>> streamActiveEmergencies() {
    return _firestore
        .collection(AppConstants.emergenciesCollection)
        .where('status', isEqualTo: 'active')
        .orderBy('timestamp', descending: true)
        .limit(10)
        .snapshots()
        .map(
          (snapshot) => snapshot.docs
              .map((doc) => EmergencyModel.fromJson(doc.data()))
              .toList(),
        );
  }

  /// Stream a specific emergency by ID (for bystander tracking).
  Stream<EmergencyModel?> streamEmergency(String emergencyId) {
    return _firestore
        .collection(AppConstants.emergenciesCollection)
        .doc(emergencyId)
        .snapshots()
        .map((doc) {
          if (!doc.exists) return null;
          return EmergencyModel.fromJson(doc.data()!);
        });
  }

  /// Update volunteer's live location during navigation.
  Future<void> updateVolunteerLocation({
    required String emergencyId,
    required double latitude,
    required double longitude,
  }) async {
    await _firestore
        .collection(AppConstants.emergenciesCollection)
        .doc(emergencyId)
        .update({
          'volunteerLat': latitude,
          'volunteerLng': longitude,
          'volunteerLocationUpdatedAt': FieldValue.serverTimestamp(),
        });
  }

  /// Get nearby active emergencies within radius (in km).
  Future<List<EmergencyModel>> getNearbyEmergencies({
    required double latitude,
    required double longitude,
    double radiusKm = 1.0,
  }) async {
    final snapshot = await _firestore
        .collection(AppConstants.emergenciesCollection)
        .where('status', isEqualTo: 'active')
        .get();

    final radiusMeters = radiusKm * 1000;
    return snapshot.docs
        .map((doc) => EmergencyModel.fromJson(doc.data()))
        .where((e) {
          final distance = Geolocator.distanceBetween(
            latitude,
            longitude,
            e.latitude,
            e.longitude,
          );
          return distance <= radiusMeters;
        })
        .toList();
  }
}
