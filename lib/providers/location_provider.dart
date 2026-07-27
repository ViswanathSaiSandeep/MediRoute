import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:geolocator/geolocator.dart';
import '../services/location_service.dart';

/// Provides the LocationService singleton.
final locationServiceProvider = Provider<LocationService>(
  (ref) => LocationService(),
);

/// Async provider for getting current position.
final currentPositionProvider = FutureProvider<Position?>((ref) async {
  final service = ref.watch(locationServiceProvider);
  final hasPermission = await service.requestPermission();
  if (!hasPermission) return null;
  return await service.getCurrentPosition();
});

/// Stream of real-time position updates.
final positionStreamProvider = StreamProvider<Position>((ref) {
  final service = ref.watch(locationServiceProvider);
  return service.getPositionStream();
});

/// Whether location permission is granted.
final locationPermissionProvider = FutureProvider<bool>((ref) async {
  final service = ref.watch(locationServiceProvider);
  return await service.requestPermission();
});
