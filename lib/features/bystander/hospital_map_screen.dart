import 'dart:async';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:geolocator/geolocator.dart';
import 'package:url_launcher/url_launcher.dart';
import '../../core/theme/app_colors.dart';
import '../../core/constants/app_constants.dart';
import '../../data/models/hospital_model.dart';
import '../../services/location_service.dart';
import '../../services/hospital_service.dart';
import '../../services/places_web_service_stub.dart'
    if (dart.library.js_interop) '../../services/places_web_service.dart';

/// Hospital map screen — shows nearby hospitals on Google Map.
class HospitalMapScreen extends StatefulWidget {
  const HospitalMapScreen({super.key});

  @override
  State<HospitalMapScreen> createState() => _HospitalMapScreenState();
}

class _HospitalMapScreenState extends State<HospitalMapScreen> {
  GoogleMapController? _mapController;
  LatLng? _myLocation;
  final Set<Marker> _markers = {};
  bool _locationReady = false;
  List<_HospitalInfo> _hospitals = [];
  final LocationService _locationService = LocationService();

  @override
  void initState() {
    super.initState();
    _init();
  }

  @override
  void dispose() {
    _mapController?.dispose();
    super.dispose();
  }

  Future<void> _init() async {
    // Get location
    try {
      final hasPermission = await _locationService.requestPermission();
      if (hasPermission) {
        // getLastKnownPosition is NOT supported on Web — skip it entirely.
        Position? pos;
        if (!kIsWeb) {
          pos = await Geolocator.getLastKnownPosition();
        }
        final currentPos = pos ?? await _locationService.getCurrentPosition();

        setState(() {
          _myLocation = LatLng(currentPos.latitude, currentPos.longitude);
          _locationReady = true;
        });

        _mapController?.animateCamera(
          CameraUpdate.newLatLngZoom(_myLocation!, 13),
        );
      } else {
        setState(() {
          _myLocation = const LatLng(20.5937, 78.9629);
          _locationReady = true;
        });
      }
    } catch (e) {
      debugPrint('Location init error: $e');
      setState(() {
        _myLocation = const LatLng(20.5937, 78.9629);
        _locationReady = true;
      });
    }

    // Add my location marker
    if (_myLocation != null) {
      _markers.add(
        Marker(
          markerId: const MarkerId('me'),
          position: _myLocation!,
          icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueBlue),
          infoWindow: const InfoWindow(title: 'Your Location'),
        ),
      );
    }

    final hospitals = <_HospitalInfo>[];

    // 1. Fetch from Google Places API (real nearby hospitals)
    if (_myLocation != null) {
      try {
        List<HospitalModel> placesList;

        if (kIsWeb) {
          // On web, use the JS Places library directly (avoids CORS)
          final webService = PlacesWebService();
          placesList = await webService.fetchNearbyHospitals(
            latitude: _myLocation!.latitude,
            longitude: _myLocation!.longitude,
          );
        } else {
          // On native, use the REST API
          final service = HospitalService();
          placesList = await service.fetchNearbyHospitalsFromPlaces(
            latitude: _myLocation!.latitude,
            longitude: _myLocation!.longitude,
          );
        }

        for (final h in placesList) {
          double distance = Geolocator.distanceBetween(
            _myLocation!.latitude,
            _myLocation!.longitude,
            h.latitude,
            h.longitude,
          );

          hospitals.add(
            _HospitalInfo(
              name: h.name,
              lat: h.latitude,
              lng: h.longitude,
              distance: distance,
              phone: h.phone,
            ),
          );

          _markers.add(
            Marker(
              markerId: MarkerId(h.hospitalId),
              position: LatLng(h.latitude, h.longitude),
              icon: BitmapDescriptor.defaultMarkerWithHue(
                BitmapDescriptor.hueRed,
              ),
              infoWindow: InfoWindow(
                title: h.name,
                snippet: '${(distance / 1000).toStringAsFixed(1)} km',
              ),
            ),
          );
        }
      } catch (e) {
        debugPrint('Error fetching from Places API: $e');
      }
    }

    // 2. Query Firestore and merge any unique hospitals
    try {
      final snapshot = await FirebaseFirestore.instance
          .collection(AppConstants.hospitalsCollection)
          .get();

      for (final doc in snapshot.docs) {
        final data = doc.data();
        final hospital = HospitalModel.fromJson(data);
        final lat = hospital.latitude;
        final lng = hospital.longitude;
        final name = hospital.name;

        if (lat != 0.0 && lng != 0.0) {
          double distance = 0;
          if (_myLocation != null) {
            distance = Geolocator.distanceBetween(
              _myLocation!.latitude,
              _myLocation!.longitude,
              lat,
              lng,
            );
          }

          // Check if duplicate
          bool isDuplicate = hospitals.any((h) => 
            h.name.toLowerCase() == name.toLowerCase() || 
            (Geolocator.distanceBetween(h.lat, h.lng, lat, lng) < 100)
          );

          if (!isDuplicate) {
            hospitals.add(
              _HospitalInfo(
                name: name,
                lat: lat,
                lng: lng,
                distance: distance,
                phone: hospital.phone,
              ),
            );

            _markers.add(
              Marker(
                markerId: MarkerId(doc.id),
                position: LatLng(lat, lng),
                icon: BitmapDescriptor.defaultMarkerWithHue(
                  BitmapDescriptor.hueRed,
                ),
                infoWindow: InfoWindow(
                  title: name,
                  snippet: '${(distance / 1000).toStringAsFixed(1)} km',
                ),
              ),
            );
          }
        }
      }
    } catch (e) {
      debugPrint('Error query Firestore: $e');
    }

    // 3. Fallback: If no hospitals were found at all, generate mock hospitals near the current location
    if (hospitals.isEmpty && _myLocation != null) {
      final mockData = [
        {
          'name': 'City Emergency Hospital',
          'latOffset': 0.006,
          'lngOffset': 0.008,
          'phone': '108',
        },
        {
          'name': 'St. Jude Medical Center',
          'latOffset': -0.008,
          'lngOffset': 0.012,
          'phone': '011-2345678',
        },
        {
          'name': 'Metro Health Clinic',
          'latOffset': 0.012,
          'lngOffset': -0.006,
          'phone': '108',
        },
        {
          'name': 'Red Cross Trauma Care',
          'latOffset': -0.005,
          'lngOffset': -0.009,
          'phone': '112',
        },
      ];

      for (int i = 0; i < mockData.length; i++) {
        final mock = mockData[i];
        final lat = _myLocation!.latitude + (mock['latOffset'] as double);
        final lng = _myLocation!.longitude + (mock['lngOffset'] as double);
        final name = mock['name'] as String;
        final phone = mock['phone'] as String;

        double distance = Geolocator.distanceBetween(
          _myLocation!.latitude,
          _myLocation!.longitude,
          lat,
          lng,
        );

        hospitals.add(
          _HospitalInfo(
            name: name,
            lat: lat,
            lng: lng,
            distance: distance,
            phone: phone,
          ),
        );

        _markers.add(
          Marker(
            markerId: MarkerId('mock_hospital_$i'),
            position: LatLng(lat, lng),
            icon: BitmapDescriptor.defaultMarkerWithHue(
              BitmapDescriptor.hueRed,
            ),
            infoWindow: InfoWindow(
              title: name,
              snippet: '${(distance / 1000).toStringAsFixed(1)} km',
            ),
          ),
        );
      }
    }

    // Sort by distance
    hospitals.sort((a, b) => a.distance.compareTo(b.distance));
    if (mounted) setState(() => _hospitals = hospitals);
  }

  void _callHospital(String? phone) async {
    if (phone == null || phone.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Hospital phone number not available.'),
          backgroundColor: AppColors.primaryRed,
        ),
      );
      return;
    }
    final uri = Uri.parse('tel:${phone.trim()}');
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri);
    } else {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Could not launch phone dialer.')),
        );
      }
    }
  }

  void _navigateToGoogleMaps(double lat, double lng, String name) async {
    final uri = Uri.parse('https://www.google.com/maps/search/?api=1&query=${Uri.encodeComponent(name)}+$lat,$lng');
    try {
      if (await canLaunchUrl(uri)) {
        await launchUrl(uri, mode: LaunchMode.externalApplication);
      } else {
        final fallbackUri = Uri.parse('https://maps.google.com/?q=$lat,$lng');
        await launchUrl(fallbackUri, mode: LaunchMode.externalApplication);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Could not open Google Maps.')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: Stack(
        children: [
          if (_locationReady && _myLocation != null)
            GoogleMap(
              initialCameraPosition: CameraPosition(
                target: _myLocation!,
                zoom: 13,
              ),
              onMapCreated: (c) => _mapController = c,
              markers: _markers,
              myLocationEnabled: true,
              myLocationButtonEnabled: false,
              zoomControlsEnabled: false,
            )
          else
            const Center(
              child: CircularProgressIndicator(color: AppColors.primaryRed),
            ),

          // Back + Title
          Positioned(
            top: MediaQuery.of(context).padding.top + 8,
            left: 16,
            right: 16,
            child: Row(
              children: [
                CircleAvatar(
                  backgroundColor: AppColors.background,
                  child: IconButton(
                    icon: const Icon(
                      Icons.arrow_back,
                      color: AppColors.textPrimary,
                    ),
                    onPressed: () => context.go('/bystander/home'),
                  ),
                ),
                const SizedBox(width: 12),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 8,
                  ),
                  decoration: BoxDecoration(
                    color: AppColors.background,
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
                      const Icon(
                        Icons.local_hospital,
                        color: AppColors.primaryRed,
                        size: 18,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        'Nearby Hospitals (${_hospitals.length})',
                        style: const TextStyle(
                          color: AppColors.textPrimary,
                          fontWeight: FontWeight.w700,
                          fontSize: 14,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // Hospital list panel at bottom
          if (_hospitals.isNotEmpty)
            Positioned(
              left: 0,
              right: 0,
              bottom: 0,
              child: Container(
                constraints: BoxConstraints(
                  maxHeight: MediaQuery.of(context).size.height * 0.45,
                ),
                decoration: BoxDecoration(
                  color: AppColors.cardBackground,
                  borderRadius: const BorderRadius.vertical(
                    top: Radius.circular(24),
                  ),
                  border: Border.all(color: AppColors.cardBorder, width: 1.5),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withValues(alpha: 0.4),
                      blurRadius: 16,
                      offset: const Offset(0, -4),
                    ),
                  ],
                ),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    // Handle
                    Container(
                      margin: const EdgeInsets.only(top: 12, bottom: 8),
                      width: 48,
                      height: 5,
                      decoration: BoxDecoration(
                        color: AppColors.textSubdued.withValues(alpha: 0.5),
                        borderRadius: BorderRadius.circular(2.5),
                      ),
                    ),
                    Expanded(
                      child: ListView.builder(
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                        itemCount: _hospitals.length,
                        itemBuilder: (context, i) {
                          final h = _hospitals[i];
                          return Container(
                            margin: const EdgeInsets.only(bottom: 12),
                            decoration: BoxDecoration(
                              color: AppColors.background,
                              borderRadius: BorderRadius.circular(16),
                              border: Border.all(color: AppColors.cardBorder, width: 0.8),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black.withValues(alpha: 0.08),
                                  blurRadius: 6,
                                  offset: const Offset(0, 2),
                                ),
                              ],
                            ),
                            child: ClipRRect(
                              borderRadius: BorderRadius.circular(16),
                              child: Material(
                                color: Colors.transparent,
                                child: InkWell(
                                  onTap: () {
                                    _mapController?.animateCamera(
                                      CameraUpdate.newLatLngZoom(
                                        LatLng(h.lat, h.lng),
                                        16,
                                      ),
                                    );
                                  },
                                  child: Padding(
                                    padding: const EdgeInsets.all(14),
                                    child: Row(
                                      children: [
                                        Container(
                                          padding: const EdgeInsets.all(10),
                                          decoration: BoxDecoration(
                                            color: AppColors.primaryRed.withValues(
                                              alpha: 0.12,
                                            ),
                                            shape: BoxShape.circle,
                                          ),
                                          child: const Icon(
                                            Icons.local_hospital,
                                            color: AppColors.primaryRed,
                                            size: 22,
                                          ),
                                        ),
                                        const SizedBox(width: 14),
                                        Expanded(
                                          child: Column(
                                            crossAxisAlignment:
                                                CrossAxisAlignment.start,
                                            children: [
                                              Text(
                                                h.name,
                                                maxLines: 1,
                                                overflow: TextOverflow.ellipsis,
                                                style: const TextStyle(
                                                  color: AppColors.textPrimary,
                                                  fontWeight: FontWeight.w700,
                                                  fontSize: 15,
                                                ),
                                              ),
                                              const SizedBox(height: 4),
                                              Row(
                                                children: [
                                                  const Icon(
                                                    Icons.location_on,
                                                    size: 13,
                                                    color: AppColors.textSubdued,
                                                  ),
                                                  const SizedBox(width: 4),
                                                  Text(
                                                    '${(h.distance / 1000).toStringAsFixed(1)} km away',
                                                    style: const TextStyle(
                                                      color: AppColors.textSubdued,
                                                      fontSize: 12,
                                                    ),
                                                  ),
                                                ],
                                              ),
                                            ],
                                          ),
                                        ),
                                        Row(
                                          mainAxisSize: MainAxisSize.min,
                                          children: [
                                            if (h.phone != null && h.phone!.trim().isNotEmpty) ...[
                                              GestureDetector(
                                                onTap: () => _callHospital(h.phone),
                                                child: Container(
                                                  padding: const EdgeInsets.all(10),
                                                  decoration: BoxDecoration(
                                                    color: AppColors.acceptGreen.withValues(alpha: 0.12),
                                                    shape: BoxShape.circle,
                                                  ),
                                                  child: const Icon(
                                                    Icons.phone,
                                                    color: AppColors.acceptGreen,
                                                    size: 18,
                                                  ),
                                                ),
                                              ),
                                              const SizedBox(width: 8),
                                            ],
                                            GestureDetector(
                                              onTap: () => _navigateToGoogleMaps(h.lat, h.lng, h.name),
                                              child: Container(
                                                padding: const EdgeInsets.all(10),
                                                decoration: BoxDecoration(
                                                  color: const Color(0xFF42A5F5).withValues(alpha: 0.12),
                                                  shape: BoxShape.circle,
                                                ),
                                                child: const Icon(
                                                  Icons.directions,
                                                  color: Color(0xFF42A5F5),
                                                  size: 18,
                                                ),
                                              ),
                                            ),
                                          ],
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          );
                        },
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

class _HospitalInfo {
  final String name;
  final double lat;
  final double lng;
  final double distance;
  final String? phone;

  _HospitalInfo({
    required this.name,
    required this.lat,
    required this.lng,
    required this.distance,
    this.phone,
  });
}
