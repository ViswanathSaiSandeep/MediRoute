import 'package:cloud_firestore/cloud_firestore.dart';

/// Represents a hospital registered in the MediRoute system.
class HospitalModel {
  final String hospitalId;
  final String name;
  final double latitude;
  final double longitude;
  final String geohash;
  final String phone;
  final String address;
  final List<String> emergencyTypes;
  final bool active;
  final String proofType;
  final String proofNumber;

  /// Alias for hospitalId.
  String get id => hospitalId;

  const HospitalModel({
    required this.hospitalId,
    required this.name,
    required this.latitude,
    required this.longitude,
    this.geohash = '',
    this.phone = '',
    this.address = '',
    this.emergencyTypes = const [],
    this.active = true,
    this.proofType = '',
    this.proofNumber = '',
  });

  factory HospitalModel.fromJson(Map<String, dynamic> json) {
    // Support both flat and GeoFirePoint location formats
    final locationData = json['location'] as Map<String, dynamic>?;
    final geopoint = locationData?['geopoint'] as GeoPoint?;

    return HospitalModel(
      hospitalId: json['hospitalId'] as String? ?? '',
      name: json['name'] as String? ?? '',
      latitude:
          geopoint?.latitude ?? (json['latitude'] as num?)?.toDouble() ?? 0.0,
      longitude:
          geopoint?.longitude ?? (json['longitude'] as num?)?.toDouble() ?? 0.0,
      geohash:
          locationData?['geohash'] as String? ??
          json['geohash'] as String? ??
          '',
      phone: json['phone'] as String? ?? '',
      address: json['address'] as String? ?? '',
      emergencyTypes: List<String>.from(json['emergencyTypes'] ?? []),
      active: json['active'] as bool? ?? true,
      proofType: json['proofType'] as String? ?? '',
      proofNumber: json['proofNumber'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'hospitalId': hospitalId,
      'name': name,
      'latitude': latitude,
      'longitude': longitude,
      'geohash': geohash,
      'phone': phone,
      'address': address,
      'emergencyTypes': emergencyTypes,
      'active': active,
      'proofType': proofType,
      'proofNumber': proofNumber,
      'location': {
        'geopoint': GeoPoint(latitude, longitude),
        'geohash': geohash,
      },
    };
  }
}
