import 'package:cloud_firestore/cloud_firestore.dart';

/// Represents a volunteer's response to an emergency.
class ResponseModel {
  final String responseId;
  final String emergencyId;
  final String volunteerId;
  final DateTime acceptedAt;
  final DateTime? arrivedAt;
  final String? helpProvided;
  final String? outcome; // 'stabilized' | 'transported' | 'cancelled'
  final String? notes;

  const ResponseModel({
    required this.responseId,
    required this.emergencyId,
    required this.volunteerId,
    required this.acceptedAt,
    this.arrivedAt,
    this.helpProvided,
    this.outcome,
    this.notes,
  });

  factory ResponseModel.fromJson(Map<String, dynamic> json) {
    return ResponseModel(
      responseId: json['responseId'] as String? ?? '',
      emergencyId: json['emergencyId'] as String? ?? '',
      volunteerId: json['volunteerId'] as String? ?? '',
      acceptedAt:
          (json['acceptedAt'] as Timestamp?)?.toDate() ?? DateTime.now(),
      arrivedAt: (json['arrivedAt'] as Timestamp?)?.toDate(),
      helpProvided: json['helpProvided'] as String?,
      outcome: json['outcome'] as String?,
      notes: json['notes'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'responseId': responseId,
      'emergencyId': emergencyId,
      'volunteerId': volunteerId,
      'acceptedAt': Timestamp.fromDate(acceptedAt),
      'arrivedAt': arrivedAt != null ? Timestamp.fromDate(arrivedAt!) : null,
      'helpProvided': helpProvided,
      'outcome': outcome,
      'notes': notes,
    };
  }
}
