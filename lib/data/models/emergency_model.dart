import 'package:cloud_firestore/cloud_firestore.dart';

/// Represents an active emergency SOS request.
class EmergencyModel {
  final String emergencyId;
  final String bystanderUid;
  final String type; // 'Cardiac Arrest', 'Choking', etc.
  final double latitude;
  final double longitude;
  final String geohash;
  final DateTime timestamp;
  final String status; // 'active' | 'assigned' | 'resolved' | 'cancelled'
  final String? volunteerAssigned;
  final String? volunteerName;
  final double? volunteerLat;
  final double? volunteerLng;
  final String? nearestHospitalId;
  final String? address;

  const EmergencyModel({
    required this.emergencyId,
    required this.bystanderUid,
    required this.type,
    required this.latitude,
    required this.longitude,
    this.geohash = '',
    required this.timestamp,
    this.status = 'active',
    this.volunteerAssigned,
    this.volunteerName,
    this.volunteerLat,
    this.volunteerLng,
    this.nearestHospitalId,
    this.address,
  });

  factory EmergencyModel.fromJson(Map<String, dynamic> json) {
    return EmergencyModel(
      emergencyId: json['emergencyId'] as String? ?? '',
      bystanderUid: json['bystanderUid'] as String? ?? '',
      type: json['type'] as String? ?? 'Other',
      latitude: (json['latitude'] as num?)?.toDouble() ?? 0.0,
      longitude: (json['longitude'] as num?)?.toDouble() ?? 0.0,
      geohash: json['geohash'] as String? ?? '',
      timestamp: (json['timestamp'] as Timestamp?)?.toDate() ?? DateTime.now(),
      status: json['status'] as String? ?? 'active',
      volunteerAssigned: json['volunteerAssigned'] as String?,
      volunteerName: json['volunteerName'] as String?,
      volunteerLat: (json['volunteerLat'] as num?)?.toDouble(),
      volunteerLng: (json['volunteerLng'] as num?)?.toDouble(),
      nearestHospitalId: json['nearestHospitalId'] as String?,
      address: json['address'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'emergencyId': emergencyId,
      'bystanderUid': bystanderUid,
      'type': type,
      'latitude': latitude,
      'longitude': longitude,
      'geohash': geohash,
      'timestamp': Timestamp.fromDate(timestamp),
      'status': status,
      'volunteerAssigned': volunteerAssigned,
      'volunteerName': volunteerName,
      'volunteerLat': volunteerLat,
      'volunteerLng': volunteerLng,
      'nearestHospitalId': nearestHospitalId,
      'address': address,
    };
  }

  EmergencyModel copyWith({
    String? emergencyId,
    String? bystanderUid,
    String? type,
    double? latitude,
    double? longitude,
    String? geohash,
    DateTime? timestamp,
    String? status,
    String? volunteerAssigned,
    String? volunteerName,
    double? volunteerLat,
    double? volunteerLng,
    String? nearestHospitalId,
    String? address,
  }) {
    return EmergencyModel(
      emergencyId: emergencyId ?? this.emergencyId,
      bystanderUid: bystanderUid ?? this.bystanderUid,
      type: type ?? this.type,
      latitude: latitude ?? this.latitude,
      longitude: longitude ?? this.longitude,
      geohash: geohash ?? this.geohash,
      timestamp: timestamp ?? this.timestamp,
      status: status ?? this.status,
      volunteerAssigned: volunteerAssigned ?? this.volunteerAssigned,
      volunteerName: volunteerName ?? this.volunteerName,
      volunteerLat: volunteerLat ?? this.volunteerLat,
      volunteerLng: volunteerLng ?? this.volunteerLng,
      nearestHospitalId: nearestHospitalId ?? this.nearestHospitalId,
      address: address ?? this.address,
    );
  }

  /// Whether this emergency is still active and needs response.
  bool get isActive => status == 'active' || status == 'assigned';
}
