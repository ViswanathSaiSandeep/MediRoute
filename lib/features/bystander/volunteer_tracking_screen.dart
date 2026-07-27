import 'dart:async';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:geolocator/geolocator.dart';
import '../../core/theme/app_colors.dart';
import '../../core/constants/app_constants.dart';
import '../../services/location_service.dart';

/// Bystander view — tracks volunteer en route on a real map.
class VolunteerTrackingScreen extends StatefulWidget {
  final String? emergencyId;

  const VolunteerTrackingScreen({super.key, this.emergencyId});

  @override
  State<VolunteerTrackingScreen> createState() =>
      _VolunteerTrackingScreenState();
}

class _VolunteerTrackingScreenState extends State<VolunteerTrackingScreen> {
  GoogleMapController? _mapController;
  LatLng? _myLocation;
  LatLng? _volunteerLocation;
  String _volunteerName = 'Volunteer';
  String _status = 'Searching...';
  double _distance = 0;
  bool _locationReady = false;
  StreamSubscription? _emergencySub;
  final LocationService _locationService = LocationService();

  @override
  void initState() {
    super.initState();
    _init();
  }

  @override
  void dispose() {
    _emergencySub?.cancel();
    _mapController?.dispose();
    super.dispose();
  }

  Future<void> _init() async {
    // Request location permission
    try {
      final hasPermission = await _locationService.requestPermission();
      if (hasPermission) {
        final pos = await _locationService.getCurrentPosition();
        if (mounted) {
          setState(() {
            _myLocation = LatLng(pos.latitude, pos.longitude);
            _locationReady = true;
          });
          _mapController?.animateCamera(CameraUpdate.newLatLng(_myLocation!));
        }
      } else {
        // Fallback — try anyway
        try {
          final pos = await Geolocator.getCurrentPosition();
          if (mounted) {
            setState(() {
              _myLocation = LatLng(pos.latitude, pos.longitude);
              _locationReady = true;
            });
          }
        } catch (_) {
          // Use a default location in India
          if (mounted) {
            setState(() {
              _myLocation = const LatLng(20.5937, 78.9629);
              _locationReady = true;
            });
          }
        }
      }
    } catch (_) {
      if (mounted) {
        setState(() {
          _myLocation = const LatLng(20.5937, 78.9629);
          _locationReady = true;
        });
      }
    }

    // Listen to emergency for volunteer position updates
    if (widget.emergencyId != null) {
      _emergencySub = FirebaseFirestore.instance
          .collection(AppConstants.emergenciesCollection)
          .doc(widget.emergencyId)
          .snapshots()
          .listen((doc) {
            if (!doc.exists || !mounted) return;
            final data = doc.data()!;
            final vLat = data['volunteerLat'] as double?;
            final vLng = data['volunteerLng'] as double?;
            final vName = data['volunteerName'] as String?;
            final status = data['status'] as String?;

            setState(() {
              if (vName != null) _volunteerName = vName;
              if (status != null) {
                _status = status == 'assigned'
                    ? 'En Route'
                    : status == 'resolved'
                    ? 'Arrived'
                    : status;
              }
            });

            if (vLat != null && vLng != null) {
              setState(() {
                _volunteerLocation = LatLng(vLat, vLng);
                if (_myLocation != null) {
                  _distance = Geolocator.distanceBetween(
                    _myLocation!.latitude,
                    _myLocation!.longitude,
                    vLat,
                    vLng,
                  );
                }
              });
              // Fit both markers on screen
              if (_myLocation != null) {
                _mapController?.animateCamera(
                  CameraUpdate.newLatLngBounds(
                    LatLngBounds(
                      southwest: LatLng(
                        _myLocation!.latitude < vLat
                            ? _myLocation!.latitude
                            : vLat,
                        _myLocation!.longitude < vLng
                            ? _myLocation!.longitude
                            : vLng,
                      ),
                      northeast: LatLng(
                        _myLocation!.latitude > vLat
                            ? _myLocation!.latitude
                            : vLat,
                        _myLocation!.longitude > vLng
                            ? _myLocation!.longitude
                            : vLng,
                      ),
                    ),
                    80,
                  ),
                );
              }
            }

            if (status == 'resolved') {
              if (mounted) context.go('/bystander/home');
            }
          });
    }
  }

  int get _etaMinutes => (_distance / 80).ceil().clamp(1, 60);

  @override
  Widget build(BuildContext context) {
    final markers = <Marker>{};
    if (_myLocation != null) {
      markers.add(
        Marker(
          markerId: const MarkerId('me'),
          position: _myLocation!,
          icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueRed),
          infoWindow: const InfoWindow(title: 'Your Location'),
        ),
      );
    }
    if (_volunteerLocation != null) {
      markers.add(
        Marker(
          markerId: const MarkerId('volunteer'),
          position: _volunteerLocation!,
          icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueBlue),
          infoWindow: InfoWindow(title: _volunteerName),
        ),
      );
    }

    return Scaffold(
      backgroundColor: AppColors.background,
      body: Stack(
        children: [
          // Map — only show when location is ready
          if (_locationReady && _myLocation != null)
            GoogleMap(
              initialCameraPosition: CameraPosition(
                target: _myLocation!,
                zoom: 15,
              ),
              onMapCreated: (c) => _mapController = c,
              markers: markers,
              myLocationEnabled: true,
              myLocationButtonEnabled: false,
              zoomControlsEnabled: false,
              mapType: MapType.normal,
            )
          else
            const Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  CircularProgressIndicator(color: AppColors.primaryRed),
                  SizedBox(height: 16),
                  Text(
                    'Getting your location...',
                    style: TextStyle(color: AppColors.textSecondary),
                  ),
                ],
              ),
            ),

          // Back button
          Positioned(
            top: MediaQuery.of(context).padding.top + 8,
            left: 16,
            child: CircleAvatar(
              backgroundColor: AppColors.background,
              child: IconButton(
                icon: const Icon(
                  Icons.arrow_back,
                  color: AppColors.textPrimary,
                ),
                onPressed: () => context.go('/bystander/home'),
              ),
            ),
          ),

          // Volunteer info card
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
                  Row(
                    children: [
                      CircleAvatar(
                        radius: 24,
                        backgroundColor: const Color(
                          0xFF42A5F5,
                        ).withValues(alpha: 0.2),
                        child: const Icon(
                          Icons.person,
                          color: Color(0xFF42A5F5),
                          size: 26,
                        ),
                      ),
                      const SizedBox(width: 14),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              _volunteerName,
                              style: const TextStyle(
                                color: AppColors.textPrimary,
                                fontSize: 18,
                                fontWeight: FontWeight.w700,
                              ),
                            ),
                            Text(
                              _volunteerLocation != null
                                  ? 'Volunteer is $_status'
                                  : 'Searching for nearby volunteers...',
                              style: const TextStyle(
                                color: AppColors.textSecondary,
                                fontSize: 13,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      _InfoChip(
                        icon: Icons.timer,
                        label: 'ETA',
                        value: _volunteerLocation != null
                            ? '$_etaMinutes min'
                            : '--',
                      ),
                      const SizedBox(width: 12),
                      _InfoChip(
                        icon: Icons.straighten,
                        label: 'Distance',
                        value: _volunteerLocation != null
                            ? _distance < 1000
                                  ? '${_distance.toInt()} m'
                                  : '${(_distance / 1000).toStringAsFixed(1)} km'
                            : '--',
                      ),
                    ],
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

class _InfoChip extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  const _InfoChip({
    required this.icon,
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 12),
        decoration: BoxDecoration(
          color: AppColors.background,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Row(
          children: [
            Icon(icon, color: AppColors.primaryRed, size: 18),
            const SizedBox(width: 8),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  label,
                  style: const TextStyle(
                    color: AppColors.textSubdued,
                    fontSize: 10,
                  ),
                ),
                Text(
                  value,
                  style: const TextStyle(
                    color: AppColors.textPrimary,
                    fontSize: 16,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
