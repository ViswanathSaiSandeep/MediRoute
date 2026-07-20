import 'dart:async';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:geolocator/geolocator.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../../core/theme/app_colors.dart';
import '../../core/constants/app_constants.dart';
import '../../data/models/emergency_model.dart';
import '../../services/location_service.dart';

/// Volunteer dashboard — real map, availability toggle, listens for emergencies.
class VolunteerDashboardScreen extends StatefulWidget {
  const VolunteerDashboardScreen({super.key});

  @override
  State<VolunteerDashboardScreen> createState() =>
      _VolunteerDashboardScreenState();
}

class _VolunteerDashboardScreenState extends State<VolunteerDashboardScreen> {
  GoogleMapController? _mapController;
  LatLng _myLocation = const LatLng(20.5937, 78.9629); // Default India center
  bool _isAvailable = true;
  StreamSubscription? _emergencySub;
  StreamSubscription<Position>? _posSub;
  final LocationService _locationService = LocationService();
  int _currentNavIndex = 0;

  /// Track emergency IDs that have already been shown/navigated to,
  /// so we don't repeatedly navigate for the same emergency.
  final Set<String> _seenEmergencyIds = {};

  /// Whether we are currently showing an emergency alert (to prevent double-navigation)
  bool _isShowingAlert = false;

  @override
  void initState() {
    super.initState();
    _init();
  }

  @override
  void dispose() {
    _emergencySub?.cancel();
    _posSub?.cancel();
    _mapController?.dispose();
    super.dispose();
  }

  Future<void> _init() async {
    // Get location
    final hasPermission = await _locationService.requestPermission();
    if (hasPermission) {
      final pos = await _locationService.getCurrentPosition();
      setState(() => _myLocation = LatLng(pos.latitude, pos.longitude));
      _mapController?.animateCamera(CameraUpdate.newLatLng(_myLocation));

      // Update position in Firestore
      final uid = FirebaseAuth.instance.currentUser?.uid;
      if (uid != null) {
        await FirebaseFirestore.instance
            .collection(AppConstants.usersCollection)
            .doc(uid)
            .update({
              'location': {
                'geopoint': GeoPoint(pos.latitude, pos.longitude),
                'geohash': '',
              },
              'availability': _isAvailable,
            });
      }
    }

    // Listen for active emergencies
    _emergencySub = FirebaseFirestore.instance
        .collection(AppConstants.emergenciesCollection)
        .where('status', isEqualTo: 'active')
        .orderBy('timestamp', descending: true)
        .limit(10)
        .snapshots()
        .listen((snapshot) {
          if (!_isAvailable || !mounted || _isShowingAlert) return;

          final uid = FirebaseAuth.instance.currentUser?.uid;

          for (final doc in snapshot.docs) {
            final emergency = EmergencyModel.fromJson(doc.data());

            // Skip if we've already navigated to this emergency
            if (_seenEmergencyIds.contains(emergency.emergencyId)) continue;

            // Skip if this volunteer is the bystander who created it
            if (uid != null && emergency.bystanderUid == uid) continue;

            final distance = Geolocator.distanceBetween(
              _myLocation.latitude,
              _myLocation.longitude,
              emergency.latitude,
              emergency.longitude,
            );

            // Alert if within search radius (1km)
            if (distance <= AppConstants.volunteerSearchRadiusKm * 1000) {
              _seenEmergencyIds.add(emergency.emergencyId);
              _isShowingAlert = true;
              context.go(
                '/volunteer/alert',
                extra: {
                  'emergencyId': emergency.emergencyId,
                  'emergencyType': emergency.type,
                  'distance': distance,
                  'latitude': emergency.latitude,
                  'longitude': emergency.longitude,
                },
              );
              break;
            }
          }
        });
  }

  void _toggleAvailability(bool value) {
    setState(() => _isAvailable = value);
    final uid = FirebaseAuth.instance.currentUser?.uid;
    if (uid != null) {
      FirebaseFirestore.instance
          .collection(AppConstants.usersCollection)
          .doc(uid)
          .update({'availability': value});
    }
  }

  Future<void> _showNearbyAlerts() async {
    showModalBottomSheet(
      context: context,
      backgroundColor: AppColors.cardBackground,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) {
        return StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
          stream: FirebaseFirestore.instance
              .collection(AppConstants.emergenciesCollection)
              .where('status', isEqualTo: 'active')
              .orderBy('timestamp', descending: true)
              .snapshots(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator(color: Color(0xFF42A5F5)));
            }

            if (!snapshot.hasData || snapshot.data!.docs.isEmpty) {
              return const Padding(
                padding: EdgeInsets.all(32.0),
                child: Center(
                  child: Text(
                    'No active emergencies nearby.',
                    style: TextStyle(color: AppColors.textSecondary),
                  ),
                ),
              );
            }

            final docs = snapshot.data!.docs;
            final nearbyEmergencies = <Map<String, dynamic>>[];
            final uid = FirebaseAuth.instance.currentUser?.uid;

            for (final doc in docs) {
              final data = doc.data();
              final eLat = data['latitude'] as double?;
              final eLng = data['longitude'] as double?;
              if (eLat == null || eLng == null) continue;

              // Skip if this volunteer created the emergency
              final bystanderUid = data['bystanderUid'] as String?;
              if (uid != null && bystanderUid == uid) continue;

              final distance = Geolocator.distanceBetween(
                _myLocation.latitude,
                _myLocation.longitude,
                eLat,
                eLng,
              );

              // Show active emergencies within search radius (1km)
              if (distance <= AppConstants.volunteerSearchRadiusKm * 1000) {
                nearbyEmergencies.add({
                  ...data,
                  'distance': distance,
                });
              }
            }

            if (nearbyEmergencies.isEmpty) {
              return Padding(
                padding: const EdgeInsets.all(32.0),
                child: Center(
                  child: Text(
                    'No active emergencies within ${AppConstants.volunteerSearchRadiusKm.toStringAsFixed(0)}km.',
                    style: const TextStyle(color: AppColors.textSecondary),
                  ),
                ),
              );
            }

            return Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Active Nearby Emergencies',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w700,
                      color: AppColors.textPrimary,
                    ),
                  ),
                  const SizedBox(height: 16),
                  Flexible(
                    child: ListView.builder(
                      shrinkWrap: true,
                      itemCount: nearbyEmergencies.length,
                      itemBuilder: (context, i) {
                        final e = nearbyEmergencies[i];
                        final dist = e['distance'] as double;
                        final distText = dist < 1000
                            ? '${dist.toInt()} m'
                            : '${(dist / 1000).toStringAsFixed(1)} km';

                        return Container(
                          margin: const EdgeInsets.only(bottom: 10),
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: AppColors.background,
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(color: AppColors.cardBorder, width: 0.5),
                          ),
                          child: Row(
                            children: [
                              Container(
                                padding: const EdgeInsets.all(8),
                                decoration: BoxDecoration(
                                  color: AppColors.primaryRed.withValues(alpha: 0.15),
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: const Icon(
                                  Icons.emergency,
                                  color: AppColors.primaryRed,
                                  size: 20,
                                ),
                              ),
                              const SizedBox(width: 12),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      e['type'] as String? ?? 'Emergency',
                                      style: const TextStyle(
                                        color: AppColors.textPrimary,
                                        fontWeight: FontWeight.w600,
                                        fontSize: 14,
                                      ),
                                    ),
                                    Text(
                                      '$distText away',
                                      style: const TextStyle(
                                        color: AppColors.textSecondary,
                                        fontSize: 12,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                              ElevatedButton(
                                onPressed: () {
                                  Navigator.pop(context);
                                  final emergencyId = e['emergencyId'] as String?;
                                  if (emergencyId != null) {
                                    _seenEmergencyIds.add(emergencyId);
                                  }
                                  this.context.go(
                                    '/volunteer/alert',
                                    extra: {
                                      'emergencyId': emergencyId,
                                      'emergencyType': e['type'],
                                      'distance': dist,
                                      'latitude': e['latitude'],
                                      'longitude': e['longitude'],
                                    },
                                  );
                                },
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: AppColors.primaryRed,
                                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                ),
                                child: const Text(
                                  'Respond',
                                  style: TextStyle(
                                    fontSize: 12,
                                    fontWeight: FontWeight.w700,
                                    color: Colors.white,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: Stack(
        children: [
          // Real Google Map
          GoogleMap(
            initialCameraPosition: CameraPosition(
              target: _myLocation,
              zoom: 15,
            ),
            onMapCreated: (c) => _mapController = c,
            myLocationEnabled: true,
            myLocationButtonEnabled: false,
            zoomControlsEnabled: false,
            mapType: MapType.normal,
          ),

          // Top bar
          Positioned(
            top: MediaQuery.of(context).padding.top + 8,
            left: 16,
            right: 16,
            child: Row(
              children: [
                // Logo
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: AppColors.background,
                    borderRadius: BorderRadius.circular(12),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withValues(alpha: 0.3),
                        blurRadius: 8,
                      ),
                    ],
                  ),
                  child: const Row(
                    children: [
                      Icon(
                        Icons.volunteer_activism,
                        color: Color(0xFF42A5F5),
                        size: 20,
                      ),
                      SizedBox(width: 8),
                      Text(
                        'MediRoute',
                        style: TextStyle(
                          color: AppColors.textPrimary,
                          fontWeight: FontWeight.w700,
                          fontSize: 16,
                        ),
                      ),
                    ],
                  ),
                ),
                const Spacer(),
                // Availability toggle
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 6,
                  ),
                  decoration: BoxDecoration(
                    color: _isAvailable
                        ? Colors.green
                        : AppColors.cardBackground,
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withValues(alpha: 0.3),
                        blurRadius: 8,
                      ),
                    ],
                  ),
                  child: Row(
                    children: [
                      Text(
                        _isAvailable ? 'Available' : 'Offline',
                        style: const TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.w700,
                          fontSize: 13,
                        ),
                      ),
                      const SizedBox(width: 6),
                      SizedBox(
                        height: 24,
                        child: Switch(
                          value: _isAvailable,
                          onChanged: _toggleAvailability,
                          activeThumbColor: Colors.white,
                          activeTrackColor: Colors.green.shade700,
                          materialTapTargetSize:
                              MaterialTapTargetSize.shrinkWrap,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // Status card at bottom
          Positioned(
            left: 16,
            right: 16,
            bottom: 80,
            child: Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AppColors.cardBackground,
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: AppColors.cardBorder),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withValues(alpha: 0.3),
                    blurRadius: 16,
                  ),
                ],
              ),
              child: Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: _isAvailable
                          ? Colors.green.withValues(alpha: 0.2)
                          : AppColors.primaryRed.withValues(alpha: 0.2),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Icon(
                      _isAvailable ? Icons.wifi_tethering : Icons.wifi_off,
                      color: _isAvailable ? Colors.green : AppColors.primaryRed,
                    ),
                  ),
                  const SizedBox(width: 14),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          _isAvailable
                              ? 'Waiting for alerts...'
                              : 'You are offline',
                          style: const TextStyle(
                            color: AppColors.textPrimary,
                            fontSize: 16,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                        Text(
                          _isAvailable
                              ? 'Listening for emergencies within ${AppConstants.volunteerSearchRadiusKm.toStringAsFixed(0)}km'
                              : 'Toggle availability to receive alerts',
                          style: const TextStyle(
                            color: AppColors.textSecondary,
                            fontSize: 12,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
      bottomNavigationBar: Container(
        decoration: const BoxDecoration(
          color: AppColors.backgroundDark,
          border: Border(top: BorderSide(color: AppColors.divider)),
        ),
        child: BottomNavigationBar(
          currentIndex: _currentNavIndex,
          onTap: (i) {
            if (i == 0) {
              setState(() => _currentNavIndex = 0);
              // Reset alert flag when returning to dashboard
              _isShowingAlert = false;
            } else if (i == 1) {
              _showNearbyAlerts();
            } else if (i == 2) {
              context.go('/history');
            } else if (i == 3) {
              context.go('/profile');
            }
          },
          backgroundColor: AppColors.backgroundDark,
          selectedItemColor: const Color(0xFF42A5F5),
          unselectedItemColor: AppColors.textSubdued,
          type: BottomNavigationBarType.fixed,
          elevation: 0,
          items: const [
            BottomNavigationBarItem(icon: Icon(Icons.map), label: 'Dashboard'),
            BottomNavigationBarItem(
              icon: Icon(Icons.notifications),
              label: 'Alerts',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.history),
              label: 'History',
            ),
            BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
          ],
        ),
      ),
    );
  }
}
