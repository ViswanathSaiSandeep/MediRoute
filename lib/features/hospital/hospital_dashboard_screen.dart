import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:intl/intl.dart';
import '../../core/theme/app_colors.dart';
import '../../core/constants/app_constants.dart';
import '../../data/models/hospital_model.dart';

/// Hospital dashboard — real-time emergency intake coordination.
class HospitalDashboardScreen extends StatefulWidget {
  const HospitalDashboardScreen({super.key});

  @override
  State<HospitalDashboardScreen> createState() =>
      _HospitalDashboardScreenState();
}

class _HospitalDashboardScreenState extends State<HospitalDashboardScreen> {
  bool _isLoading = true;
  HospitalModel? _hospital;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadHospitalDetails();
  }

  Future<void> _loadHospitalDetails() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) {
      if (mounted) context.go('/role-selection');
      return;
    }

    try {
      final doc = await FirebaseFirestore.instance
          .collection(AppConstants.hospitalsCollection)
          .doc(user.uid)
          .get();

      if (doc.exists && mounted) {
        setState(() {
          _hospital = HospitalModel.fromJson(doc.data()!);
          _isLoading = false;
        });
      } else {
        if (mounted) {
          setState(() {
            _errorMessage = 'Hospital profile not found.';
            _isLoading = false;
          });
        }
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _errorMessage = 'Failed to load hospital details.';
          _isLoading = false;
        });
      }
    }
  }

  Future<void> _toggleAvailability(bool value) async {
    if (_hospital == null) return;
    final uid = FirebaseAuth.instance.currentUser?.uid;
    if (uid == null) return;

    try {
      await FirebaseFirestore.instance
          .collection(AppConstants.hospitalsCollection)
          .doc(uid)
          .update({'active': value});

      setState(() {
        _hospital = HospitalModel(
          hospitalId: _hospital!.hospitalId,
          name: _hospital!.name,
          latitude: _hospital!.latitude,
          longitude: _hospital!.longitude,
          phone: _hospital!.phone,
          address: _hospital!.address,
          emergencyTypes: _hospital!.emergencyTypes,
          proofType: _hospital!.proofType,
          proofNumber: _hospital!.proofNumber,
          active: value,
        );
      });
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to update availability.')),
        );
      }
    }
  }

  Future<void> _updateAlertStatus(String emergencyId, String status) async {
    final uid = FirebaseAuth.instance.currentUser?.uid;
    if (uid == null) return;

    try {
      await FirebaseFirestore.instance
          .collection(AppConstants.hospitalsCollection)
          .doc(uid)
          .collection(AppConstants.hospitalAlertsSubcollection)
          .doc(emergencyId)
          .update({'status': status});
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to update status to $status.')),
        );
      }
    }
  }

  Future<void> _logout() async {
    await FirebaseAuth.instance.signOut();
    if (mounted) context.go('/role-selection');
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Scaffold(
        backgroundColor: AppColors.background,
        body: Center(
          child: CircularProgressIndicator(color: AppColors.primaryRed),
        ),
      );
    }

    if (_errorMessage != null || _hospital == null) {
      return Scaffold(
        backgroundColor: AppColors.background,
        appBar: AppBar(
          backgroundColor: Colors.transparent,
          title: const Text('Error'),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                _errorMessage ?? 'An error occurred.',
                style: const TextStyle(color: AppColors.primaryRed, fontSize: 16),
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: _logout,
                style: ElevatedButton.styleFrom(backgroundColor: AppColors.primaryRed),
                child: const Text('Log Out'),
              ),
            ],
          ),
        ),
      );
    }

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: AppColors.backgroundDark,
        title: const Text('Hospital Dashboard'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout, color: AppColors.textSecondary),
            onPressed: _logout,
          ),
        ],
      ),
      body: SafeArea(
        child: RefreshIndicator(
          onRefresh: _loadHospitalDetails,
          color: AppColors.primaryRed,
          child: LayoutBuilder(
            builder: (context, constraints) {
              final isWide = constraints.maxWidth > 800;

              return Padding(
                padding: const EdgeInsets.all(20.0),
                child: isWide
                    ? Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Expanded(
                            flex: 2,
                            child: SingleChildScrollView(
                              child: _buildHospitalInfoCard(true),
                            ),
                          ),
                          const SizedBox(width: 24),
                          Expanded(
                            flex: 3,
                            child: _buildAlertsSection(),
                          ),
                        ],
                      )
                    : Column(
                        children: [
                          _buildHospitalInfoCard(false),
                          const SizedBox(height: 20),
                          Expanded(
                            child: _buildAlertsSection(),
                          ),
                        ],
                      ),
              );
            },
          ),
        ),
      ),
    );
  }

  Widget _buildHospitalInfoCard(bool isWide) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.cardBackground,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: AppColors.cardBorder, width: 1.5),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.3),
            blurRadius: 16,
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: AppColors.primaryRed.withValues(alpha: 0.15),
                  shape: BoxShape.circle,
                ),
                child: const Icon(
                  Icons.local_hospital,
                  color: AppColors.primaryRed,
                  size: 28,
                ),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      _hospital!.name,
                      style: const TextStyle(
                        color: AppColors.textPrimary,
                        fontSize: 20,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      _hospital!.address,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
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
          const Divider(height: 32, color: AppColors.divider),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'Intake Status',
                style: TextStyle(
                  color: AppColors.textPrimary,
                  fontSize: 16,
                  fontWeight: FontWeight.w700,
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: _hospital!.active
                      ? Colors.green.withValues(alpha: 0.15)
                      : AppColors.primaryRed.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(
                    color: _hospital!.active ? Colors.green : AppColors.primaryRed,
                    width: 0.8,
                  ),
                ),
                child: Text(
                  _hospital!.active ? 'Accepting Patients' : 'Offline',
                  style: TextStyle(
                    color: _hospital!.active ? Colors.green : AppColors.primaryRed,
                    fontWeight: FontWeight.w700,
                    fontSize: 12,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          SwitchListTile(
            title: const Text(
              'Accept Active Emergencies',
              style: TextStyle(color: AppColors.textSecondary, fontSize: 14),
            ),
            subtitle: const Text(
              'Toggle availability to display in Bystander Maps and receive routing alerts.',
              style: TextStyle(color: AppColors.textSubdued, fontSize: 11),
            ),
            value: _hospital!.active,
            onChanged: _toggleAvailability,
            activeThumbColor: Colors.green,
            activeTrackColor: Colors.green.withValues(alpha: 0.3),
            inactiveThumbColor: AppColors.textSubdued,
            inactiveTrackColor: AppColors.cardBorder,
            contentPadding: EdgeInsets.zero,
          ),
          const Divider(height: 32, color: AppColors.divider),
          const Text(
            'Verified Accreditation Details',
            style: TextStyle(
              color: AppColors.textPrimary,
              fontSize: 14,
              fontWeight: FontWeight.w700,
            ),
          ),
          const SizedBox(height: 8),
          _buildDetailRow(Icons.description, 'Proof Type', _hospital!.proofType),
          const SizedBox(height: 6),
          _buildDetailRow(Icons.verified, 'Certificate ID', _hospital!.proofNumber),
          const SizedBox(height: 6),
          _buildDetailRow(Icons.phone, 'Contact Phone', _hospital!.phone),
          const SizedBox(height: 6),
          _buildDetailRow(
            Icons.pin_drop,
            'Coordinates',
            '${_hospital!.latitude.toStringAsFixed(5)}, ${_hospital!.longitude.toStringAsFixed(5)}',
          ),
          const Divider(height: 32, color: AppColors.divider),
          const Text(
            'Handled Emergency Types',
            style: TextStyle(
              color: AppColors.textPrimary,
              fontSize: 14,
              fontWeight: FontWeight.w700,
            ),
          ),
          const SizedBox(height: 8),
          Wrap(
            spacing: 6,
            runSpacing: 6,
            children: _hospital!.emergencyTypes.map((type) {
              return Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: AppColors.backgroundDark,
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: AppColors.cardBorder, width: 0.5),
                ),
                child: Text(
                  type,
                  style: const TextStyle(color: AppColors.textSecondary, fontSize: 12),
                ),
              );
            }).toList(),
          ),
        ],
      ),
    );
  }

  Widget _buildDetailRow(IconData icon, String label, String value) {
    return Row(
      children: [
        Icon(icon, color: AppColors.textSubdued, size: 16),
        const SizedBox(width: 8),
        Text(
          '$label: ',
          style: const TextStyle(color: AppColors.textSubdued, fontSize: 13),
        ),
        Expanded(
          child: Text(
            value,
            style: const TextStyle(color: AppColors.textPrimary, fontSize: 13, fontWeight: FontWeight.w600),
            overflow: TextOverflow.ellipsis,
          ),
        ),
      ],
    );
  }

  Widget _buildAlertsSection() {
    final uid = FirebaseAuth.instance.currentUser?.uid;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Active Emergency Alerts',
          style: TextStyle(
            color: AppColors.textPrimary,
            fontSize: 18,
            fontWeight: FontWeight.w800,
          ),
        ),
        const SizedBox(height: 12),
        Expanded(
          child: StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
            stream: FirebaseFirestore.instance
                .collection(AppConstants.hospitalsCollection)
                .doc(uid)
                .collection(AppConstants.hospitalAlertsSubcollection)
                .orderBy('timestamp', descending: true)
                .snapshots(),
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Center(
                  child: CircularProgressIndicator(color: AppColors.primaryRed),
                );
              }

              if (!snapshot.hasData || snapshot.data!.docs.isEmpty) {
                return Center(
                  child: Container(
                    padding: const EdgeInsets.all(32),
                    decoration: BoxDecoration(
                      color: AppColors.cardBackground,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: AppColors.cardBorder, width: 0.5),
                    ),
                    child: const Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(Icons.notifications_off, size: 48, color: AppColors.textSubdued),
                        SizedBox(height: 12),
                        Text(
                          'No incoming alerts received.',
                          style: TextStyle(color: AppColors.textSecondary, fontSize: 14),
                        ),
                      ],
                    ),
                  ),
                );
              }

              final docs = snapshot.data!.docs;
              return ListView.builder(
                itemCount: docs.length,
                itemBuilder: (context, index) {
                  final alertData = docs[index].data();
                  final alertId = docs[index].id;
                  final type = alertData['emergencyType'] as String? ?? 'General Emergency';
                  final address = alertData['address'] as String? ?? 'GPS Coordinates Provided';
                  final status = alertData['status'] as String? ?? 'notified';
                  final timestamp = alertData['timestamp'] as Timestamp?;
                  final timeText = timestamp != null
                      ? DateFormat('hh:mm a').format(timestamp.toDate())
                      : 'Just now';

                  return _buildAlertCard(alertId, type, address, status, timeText);
                },
              );
            },
          ),
        ),
      ],
    );
  }

  Widget _buildAlertCard(
    String alertId,
    String type,
    String address,
    String status,
    String timeText,
  ) {
    Color statusColor;
    String statusLabel;
    switch (status) {
      case 'notified':
        statusColor = AppColors.primaryRed;
        statusLabel = 'Incoming';
        break;
      case 'acknowledged':
        statusColor = Colors.orange;
        statusLabel = 'Preparing Intake';
        break;
      case 'dispatched':
        statusColor = const Color(0xFF42A5F5);
        statusLabel = 'Ambulance Sent';
        break;
      case 'resolved':
        statusColor = Colors.green;
        statusLabel = 'Resolved / Checked In';
        break;
      default:
        statusColor = AppColors.textSecondary;
        statusLabel = status;
    }

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.cardBackground,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: status == 'notified' ? AppColors.primaryRed : AppColors.cardBorder,
          width: status == 'notified' ? 1.2 : 0.8,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: AppColors.primaryRed.withValues(alpha: 0.12),
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(
                      Icons.emergency,
                      color: AppColors.primaryRed,
                      size: 20,
                    ),
                  ),
                  const SizedBox(width: 10),
                  Text(
                    type,
                    style: const TextStyle(
                      color: AppColors.textPrimary,
                      fontWeight: FontWeight.w700,
                      fontSize: 15,
                    ),
                  ),
                ],
              ),
              Text(
                timeText,
                style: const TextStyle(
                  color: AppColors.textSubdued,
                  fontSize: 12,
                ),
              ),
            ],
          ),
          const SizedBox(height: 10),
          Row(
            children: [
              const Icon(Icons.location_on, size: 14, color: AppColors.textSubdued),
              const SizedBox(width: 6),
              Expanded(
                child: Text(
                  address,
                  style: const TextStyle(color: AppColors.textSecondary, fontSize: 13),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Container(
                    width: 8,
                    height: 8,
                    decoration: BoxDecoration(
                      color: statusColor,
                      shape: BoxShape.circle,
                    ),
                  ),
                  const SizedBox(width: 6),
                  Text(
                    statusLabel,
                    style: TextStyle(
                      color: statusColor,
                      fontWeight: FontWeight.w700,
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
              Row(
                children: [
                  if (status == 'notified') ...[
                    TextButton(
                      onPressed: () => _updateAlertStatus(alertId, 'acknowledged'),
                      style: TextButton.styleFrom(
                        foregroundColor: Colors.orange,
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      ),
                      child: const Text('Prepare Intake'),
                    ),
                  ] else if (status == 'acknowledged') ...[
                    TextButton(
                      onPressed: () => _updateAlertStatus(alertId, 'dispatched'),
                      style: TextButton.styleFrom(
                        foregroundColor: const Color(0xFF42A5F5),
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      ),
                      child: const Text('Send Ambulance'),
                    ),
                    const SizedBox(width: 6),
                    TextButton(
                      onPressed: () => _updateAlertStatus(alertId, 'resolved'),
                      style: TextButton.styleFrom(
                        foregroundColor: Colors.green,
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      ),
                      child: const Text('Mark Checked In'),
                    ),
                  ] else if (status == 'dispatched') ...[
                    TextButton(
                      onPressed: () => _updateAlertStatus(alertId, 'resolved'),
                      style: TextButton.styleFrom(
                        foregroundColor: Colors.green,
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      ),
                      child: const Text('Mark Checked In'),
                    ),
                  ],
                ],
              ),
            ],
          ),
        ],
      ),
    );
  }
}
