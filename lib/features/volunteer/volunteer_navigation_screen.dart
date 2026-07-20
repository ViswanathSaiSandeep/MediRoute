import 'dart:async';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:geolocator/geolocator.dart';
import '../../core/theme/app_colors.dart';
import '../../services/emergency_service.dart';

/// Volunteer navigation — real map with live position tracking to victim.
class VolunteerNavigationScreen extends StatefulWidget {
  final String? emergencyId;
  final double? victimLat;
  final double? victimLng;

  const VolunteerNavigationScreen({
    super.key,
    this.emergencyId,
    this.victimLat,
    this.victimLng,
  });

  @override
  State<VolunteerNavigationScreen> createState() =>
      _VolunteerNavigationScreenState();
}

class _VolunteerNavigationScreenState extends State<VolunteerNavigationScreen> {
  GoogleMapController? _mapController;
  LatLng _myLocation = const LatLng(0, 0);
  double _distance = 0;
  StreamSubscription<Position>? _positionSub;
  final EmergencyService _emergencyService = EmergencyService();

  @override
  void initState() {
    super.initState();
    _init();
  }

  @override
  void dispose() {
    _positionSub?.cancel();
    _mapController?.dispose();
    super.dispose();
  }

  Future<void> _init() async {
    // Note: acceptEmergency() is already called in EmergencyAlertScreen
    // before navigating here. We just start position tracking.

    // Start tracking
    _positionSub =
        Geolocator.getPositionStream(
          locationSettings: const LocationSettings(
            accuracy: LocationAccuracy.high,
            distanceFilter: 5,
          ),
        ).listen((pos) {
          setState(() {
            _myLocation = LatLng(pos.latitude, pos.longitude);
            if (widget.victimLat != null && widget.victimLng != null) {
              _distance = Geolocator.distanceBetween(
                pos.latitude,
                pos.longitude,
                widget.victimLat!,
                widget.victimLng!,
              );
            }
          });

          // Update volunteer location in Firestore
          if (widget.emergencyId != null) {
            _emergencyService.updateVolunteerLocation(
              emergencyId: widget.emergencyId!,
              latitude: pos.latitude,
              longitude: pos.longitude,
            );
          }
        });
  }

  int get _etaMinutes => (_distance / 80).ceil().clamp(1, 60);

  void _markArrived() {
    context.go(
      '/volunteer/complete',
      extra: {'emergencyId': widget.emergencyId},
    );
  }

  @override
  Widget build(BuildContext context) {
    final victimPos = (widget.victimLat != null && widget.victimLng != null)
        ? LatLng(widget.victimLat!, widget.victimLng!)
        : null;

    final markers = <Marker>{
      Marker(
        markerId: const MarkerId('me'),
        position: _myLocation,
        icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueBlue),
        infoWindow: const InfoWindow(title: 'You'),
      ),
    };
    if (victimPos != null) {
      markers.add(
        Marker(
          markerId: const MarkerId('victim'),
          position: victimPos,
          icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueRed),
          infoWindow: const InfoWindow(title: 'Victim'),
        ),
      );
    }

    return Scaffold(
      backgroundColor: AppColors.background,
      body: Stack(
        children: [
          // Map
          GoogleMap(
            initialCameraPosition: CameraPosition(
              target: victimPos ?? _myLocation,
              zoom: 15,
            ),
            onMapCreated: (c) => _mapController = c,
            markers: markers,
            myLocationEnabled: true,
            myLocationButtonEnabled: false,
            zoomControlsEnabled: false,
          ),

          // Top bar
          Positioned(
            top: 0,
            left: 0,
            right: 0,
            child: Container(
              padding: EdgeInsets.fromLTRB(
                16,
                MediaQuery.of(context).padding.top + 8,
                16,
                12,
              ),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    AppColors.background,
                    AppColors.background.withValues(alpha: 0),
                  ],
                ),
              ),
              child: Row(
                children: [
                  CircleAvatar(
                    backgroundColor: AppColors.cardBackground,
                    child: IconButton(
                      icon: const Icon(
                        Icons.arrow_back,
                        color: AppColors.textPrimary,
                      ),
                      onPressed: () => context.go('/volunteer/dashboard'),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 14,
                      vertical: 8,
                    ),
                    decoration: BoxDecoration(
                      color: AppColors.primaryRed,
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: const Row(
                      children: [
                        Icon(Icons.navigation, color: Colors.white, size: 16),
                        SizedBox(width: 6),
                        Text(
                          'EN ROUTE',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.w800,
                            fontSize: 13,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),

          // Bottom info + actions
          Positioned(
            left: 16,
            right: 16,
            bottom: 24,
            child: Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AppColors.cardBackground,
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: AppColors.cardBorder),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withValues(alpha: 0.3),
                    blurRadius: 20,
                  ),
                ],
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  // ETA + Distance
                  Row(
                    children: [
                      Expanded(
                        child: _StatBox(
                          icon: Icons.timer,
                          value: '$_etaMinutes min',
                          label: 'ETA',
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: _StatBox(
                          icon: Icons.straighten,
                          value: _distance < 1000
                              ? '${_distance.toInt()} m'
                              : '${(_distance / 1000).toStringAsFixed(1)} km',
                          label: 'Distance',
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  // Mark Arrived
                  SizedBox(
                    width: double.infinity,
                    height: 52,
                    child: ElevatedButton.icon(
                      onPressed: _markArrived,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.green,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(14),
                        ),
                      ),
                      icon: const Icon(Icons.check_circle, color: Colors.white),
                      label: const Text(
                        'Mark Arrived',
                        style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.w700,
                          fontSize: 16,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _StatBox extends StatelessWidget {
  final IconData icon;
  final String value;
  final String label;
  const _StatBox({
    required this.icon,
    required this.value,
    required this.label,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 14),
      decoration: BoxDecoration(
        color: AppColors.background,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        children: [
          Icon(icon, color: AppColors.primaryRed, size: 20),
          const SizedBox(width: 10),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                label,
                style: const TextStyle(
                  color: AppColors.textSubdued,
                  fontSize: 11,
                ),
              ),
              Text(
                value,
                style: const TextStyle(
                  color: AppColors.textPrimary,
                  fontSize: 18,
                  fontWeight: FontWeight.w800,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
