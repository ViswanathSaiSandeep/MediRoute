import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../data/models/emergency_model.dart';
import '../core/constants/app_constants.dart';

/// Provides the Firestore instance.
final firestoreProvider = Provider<FirebaseFirestore>((ref) {
  return FirebaseFirestore.instance;
});

/// Stream of the currently active emergency for the current user.
final activeEmergencyProvider = StreamProvider.family<EmergencyModel?, String>((
  ref,
  bystanderUid,
) {
  final firestore = ref.watch(firestoreProvider);
  return firestore
      .collection(AppConstants.emergenciesCollection)
      .where('bystanderUid', isEqualTo: bystanderUid)
      .where('status', whereIn: ['active', 'assigned'])
      .orderBy('timestamp', descending: true)
      .limit(1)
      .snapshots()
      .map((snapshot) {
        if (snapshot.docs.isEmpty) return null;
        return EmergencyModel.fromJson(snapshot.docs.first.data());
      });
});

/// Stream of emergencies for volunteer alerts (active emergencies nearby).
final emergencyAlertsProvider = StreamProvider<List<EmergencyModel>>((ref) {
  final firestore = ref.watch(firestoreProvider);
  return firestore
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
});

/// Provider to track the selected emergency type.
final selectedEmergencyTypeProvider = StateProvider<String?>((ref) => null);
