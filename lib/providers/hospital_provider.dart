import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/hospital_service.dart';
import '../data/models/hospital_model.dart';

/// Provides the HospitalService singleton.
final hospitalServiceProvider = Provider<HospitalService>(
  (ref) => HospitalService(),
);

/// Find the nearest hospital given coordinates.
final nearestHospitalProvider =
    FutureProvider.family<HospitalModel?, ({double lat, double lng})>((
      ref,
      coords,
    ) async {
      final service = ref.watch(hospitalServiceProvider);
      return await service.findNearestHospital(
        latitude: coords.lat,
        longitude: coords.lng,
      );
    });
