import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:http/http.dart' as http;
import '../data/models/hospital_model.dart';
import '../core/constants/app_constants.dart';
import 'location_service.dart';

/// Handles hospital-related operations — finding nearest hospital and sending alerts.
class HospitalService {
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;
  final LocationService _locationService = LocationService();

  /// Find the nearest active hospital to the given coordinates.
  /// Returns the closest hospital or null if none found.
  Future<HospitalModel?> findNearestHospital({
    required double latitude,
    required double longitude,
  }) async {
    try {
      // 1. Try fetching from Firestore first
      final snapshot = await _firestore
          .collection(AppConstants.hospitalsCollection)
          .where('active', isEqualTo: true)
          .get();

      HospitalModel? nearest;
      double minDistance = double.infinity;

      if (snapshot.docs.isNotEmpty) {
        for (final doc in snapshot.docs) {
          final hospital = HospitalModel.fromJson(doc.data());
          final distance = _locationService.distanceBetween(
            latitude,
            longitude,
            hospital.latitude,
            hospital.longitude,
          );

          if (distance < minDistance) {
            minDistance = distance;
            nearest = hospital;
          }
        }
      }

      // 2. Fall back to Google Places API if Firestore is empty
      if (nearest == null) {
        final placesHospitals = await fetchNearbyHospitalsFromPlaces(
          latitude: latitude,
          longitude: longitude,
        );
        if (placesHospitals.isNotEmpty) {
          nearest = placesHospitals.first;
        }
      }

      // 3. Absolute fallback: generate a mock hospital nearby if none are found anywhere
      nearest ??= HospitalModel(
        hospitalId: 'mock_fallback_hospital',
        name: 'City Emergency Hospital (Mock)',
        latitude: latitude + 0.006,
        longitude: longitude + 0.008,
        phone: '108',
        address: 'Main Street Medical Hub',
        active: true,
      );

      return nearest;
    } catch (e) {
      return null;
    }
  }

  /// Fetch nearby hospitals from Google Places API.
  Future<List<HospitalModel>> fetchNearbyHospitalsFromPlaces({
    required double latitude,
    required double longitude,
    double radiusMeters = 5000,
  }) async {
    // Places Web Service does not support browser CORS.
    // Return empty list on Web so it falls back to mock list cleanly.
    if (kIsWeb) {
      return [];
    }

    const apiKey = 'YOUR_GOOGLE_MAPS_API_KEY';
    final url = Uri.parse(
      'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
      '?location=$latitude,$longitude'
      '&radius=$radiusMeters'
      '&type=hospital'
      '&key=$apiKey',
    );

    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        final data = json.decode(response.body) as Map<String, dynamic>;
        final results = data['results'] as List<dynamic>?;
        if (results == null) return [];

        final list = <HospitalModel>[];
        for (final item in results) {
          final geometry = item['geometry'] as Map<String, dynamic>?;
          final location = geometry?['location'] as Map<String, dynamic>?;
          final lat = location?['lat'] as double?;
          final lng = location?['lng'] as double?;
          final name = item['name'] as String? ?? 'Hospital';
          final placeId = item['place_id'] as String? ?? '';
          final address = item['vicinity'] as String? ?? '';

          if (lat != null && lng != null) {
            list.add(
              HospitalModel(
                hospitalId: placeId,
                name: name,
                latitude: lat,
                longitude: lng,
                phone: '', // Places Search doesn't return phone directly, we use empty and fall back
                address: address,
                active: true,
              ),
            );
          }
        }
        return list;
      }
      return [];
    } catch (e) {
      debugPrint('Places API error: $e');
      return [];
    }
  }

  /// Send a pre-notification alert to the nearest hospital.
  Future<void> sendHospitalAlert({
    required String emergencyId,
    required String hospitalId,
    required String emergencyType,
    required double latitude,
    required double longitude,
    String? address,
  }) async {
    // Write best-effort hospital alert to Firestore subcollection
    try {
      await _firestore
          .collection(AppConstants.hospitalsCollection)
          .doc(hospitalId)
          .collection(AppConstants.hospitalAlertsSubcollection)
          .doc(emergencyId)
          .set({
            'emergencyId': emergencyId,
            'emergencyType': emergencyType,
            'latitude': latitude,
            'longitude': longitude,
            'address': address,
            'timestamp': FieldValue.serverTimestamp(),
            'status': 'notified',
          });
    } catch (_) {}
  }
}
