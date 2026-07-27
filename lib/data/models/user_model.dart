import 'package:cloud_firestore/cloud_firestore.dart';

/// Represents a registered user in MediRoute — either a bystander or volunteer.
class UserModel {
  final String uid;
  final String role; // 'bystander' | 'volunteer'
  final String name;
  final String email;
  final String phone;
  final List<String> skills;
  final double? latitude;
  final double? longitude;
  final String? geohash;
  final bool availability;
  final DateTime createdAt;
  final String? fcmToken;

  const UserModel({
    required this.uid,
    required this.role,
    required this.name,
    this.email = '',
    this.phone = '',
    this.skills = const [],
    this.latitude,
    this.longitude,
    this.geohash,
    this.availability = true,
    required this.createdAt,
    this.fcmToken,
  });

  /// Create from Firestore document snapshot.
  factory UserModel.fromJson(Map<String, dynamic> json) {
    // Extract location data from GeoFirePoint format
    final locationData = json['location'] as Map<String, dynamic>?;
    final geopoint = locationData?['geopoint'] as GeoPoint?;

    return UserModel(
      uid: json['uid'] as String? ?? '',
      role: json['role'] as String? ?? 'bystander',
      name: json['name'] as String? ?? '',
      email: json['email'] as String? ?? '',
      phone: json['phone'] as String? ?? '',
      skills: List<String>.from(json['skills'] ?? []),
      latitude: geopoint?.latitude ?? json['latitude'] as double?,
      longitude: geopoint?.longitude ?? json['longitude'] as double?,
      geohash:
          locationData?['geohash'] as String? ?? json['geohash'] as String?,
      availability: json['availability'] as bool? ?? true,
      createdAt: (json['createdAt'] as Timestamp?)?.toDate() ?? DateTime.now(),
      fcmToken: json['fcmToken'] as String?,
    );
  }

  /// Convert to Firestore-compatible map.
  Map<String, dynamic> toJson() {
    final map = <String, dynamic>{
      'uid': uid,
      'role': role,
      'name': name,
      'email': email,
      'phone': phone,
      'skills': skills,
      'availability': availability,
      'createdAt': Timestamp.fromDate(createdAt),
      'fcmToken': fcmToken,
    };

    // Store location as GeoFirePoint-compatible format
    if (latitude != null && longitude != null) {
      map['location'] = {
        'geopoint': GeoPoint(latitude!, longitude!),
        'geohash': geohash ?? '',
      };
    }

    return map;
  }

  /// Create a copy with modified fields.
  UserModel copyWith({
    String? uid,
    String? role,
    String? name,
    String? email,
    String? phone,
    List<String>? skills,
    double? latitude,
    double? longitude,
    String? geohash,
    bool? availability,
    DateTime? createdAt,
    String? fcmToken,
  }) {
    return UserModel(
      uid: uid ?? this.uid,
      role: role ?? this.role,
      name: name ?? this.name,
      email: email ?? this.email,
      phone: phone ?? this.phone,
      skills: skills ?? this.skills,
      latitude: latitude ?? this.latitude,
      longitude: longitude ?? this.longitude,
      geohash: geohash ?? this.geohash,
      availability: availability ?? this.availability,
      createdAt: createdAt ?? this.createdAt,
      fcmToken: fcmToken ?? this.fcmToken,
    );
  }
}
