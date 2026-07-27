import '../data/models/hospital_model.dart';

/// Stub implementation for non-web platforms.
/// Returns empty list — the REST API is used instead on native.
class PlacesWebService {
  Future<List<HospitalModel>> fetchNearbyHospitals({
    required double latitude,
    required double longitude,
    double radiusMeters = 5000,
  }) async {
    return [];
  }
}
