import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Volunteer availability toggle state.
final volunteerAvailabilityProvider = StateProvider<bool>((ref) => true);

/// Volunteer role selection state.
final userRoleProvider = StateProvider<String?>((ref) => null);
