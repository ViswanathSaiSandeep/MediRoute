import 'dart:async';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:geolocator/geolocator.dart';
import 'package:url_launcher/url_launcher.dart';
import '../../core/theme/app_colors.dart';
import '../../core/constants/app_constants.dart';
import '../../core/widgets/mediroute_card.dart';
import '../../data/models/hospital_model.dart';

/// Hospital alert screen — shows nearest hospital notification status dynamically.
/// Also listens for volunteer assignment and auto-navigates to tracking.
class HospitalAlertScreen extends StatefulWidget {
  final String? emergencyId;

  const HospitalAlertScreen({super.key, this.emergencyId});

  @override
  State<HospitalAlertScreen> createState() => _HospitalAlertScreenState();
}

class _HospitalAlertScreenState extends State<HospitalAlertScreen> {
  bool _isLoading = true;
  String? _hospitalName;
  String? _hospitalPhone;
  String? _hospitalAddress;
  double? _distance;
  String? _emergencyType;
  String _volunteerStatus = 'searching'; // 'searching' | 'found' | 'en_route'
  String? _volunteerName;
  StreamSubscription? _emergencySub;
  bool _hasNavigatedToTracking = false;

  @override
  void initState() {
    super.initState();
    _loadHospitalDetails();
    _listenForVolunteerAssignment();
  }

  @override
  void dispose() {
    _emergencySub?.cancel();
    super.dispose();
  }

  /// Listen for changes to the emergency document.
  /// When a volunteer accepts (status changes to 'assigned'), auto-navigate to tracking.
  void _listenForVolunteerAssignment() {
    if (widget.emergencyId == null) return;

    _emergencySub = FirebaseFirestore.instance
        .collection(AppConstants.emergenciesCollection)
        .doc(widget.emergencyId)
        .snapshots()
        .listen((doc) {
          if (!doc.exists || !mounted || _hasNavigatedToTracking) return;
          final data = doc.data()!;
          final status = data['status'] as String?;
          final vName = data['volunteerName'] as String?;

          if (status == 'assigned') {
            setState(() {
              _volunteerStatus = 'found';
              _volunteerName = vName ?? 'Volunteer';
            });

            // Auto-navigate to tracking screen after a brief delay
            // so the user sees the "Volunteer found" message
            Future.delayed(const Duration(seconds: 2), () {
              if (mounted && !_hasNavigatedToTracking) {
                _hasNavigatedToTracking = true;
                context.go(
                  '/bystander/tracking',
                  extra: {'emergencyId': widget.emergencyId},
                );
              }
            });
          } else if (status == 'resolved') {
            if (mounted) context.go('/bystander/home');
          } else if (status == 'cancelled') {
            if (mounted) context.go('/bystander/home');
          }
        });
  }

  Future<void> _loadHospitalDetails() async {
    if (widget.emergencyId == null) {
      setState(() => _isLoading = false);
      return;
    }

    try {
      // 1. Fetch the emergency document to get nearestHospitalId
      final emergencyDoc = await FirebaseFirestore.instance
          .collection(AppConstants.emergenciesCollection)
          .doc(widget.emergencyId)
          .get();

      if (emergencyDoc.exists) {
        final data = emergencyDoc.data()!;
        final nearestHospitalId = data['nearestHospitalId'] as String?;
        _emergencyType = data['type'] as String?;
        final victimLat = data['latitude'] as double?;
        final victimLng = data['longitude'] as double?;

        if (nearestHospitalId != null) {
          // 2. Fetch hospital details
          final hospitalDoc = await FirebaseFirestore.instance
              .collection(AppConstants.hospitalsCollection)
              .doc(nearestHospitalId)
              .get();

          if (hospitalDoc.exists) {
            final hData = hospitalDoc.data()!;
            final hospital = HospitalModel.fromJson(hData);
            _hospitalName = hospital.name;
            _hospitalPhone = hospital.phone;
            _hospitalAddress = hospital.address;

            // Calculate distance
            if (victimLat != null && victimLng != null) {
              _distance = Geolocator.distanceBetween(
                victimLat,
                victimLng,
                hospital.latitude,
                hospital.longitude,
              );
            }
          }
        }
      }
    } catch (e) {
      debugPrint('Error loading hospital alert details: $e');
    }

    if (mounted) {
      setState(() => _isLoading = false);
    }
  }

  void _callHospital() async {
    if (_hospitalPhone == null || _hospitalPhone!.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Hospital phone number not available.'),
          backgroundColor: AppColors.primaryRed,
        ),
      );
      return;
    }
    final uri = Uri.parse('tel:$_hospitalPhone');
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

  String get _distanceText {
    if (_distance == null) return 'Calculating distance...';
    final d = _distance!;
    if (d < 1000) return '${d.toInt()} m away';
    return '${(d / 1000).toStringAsFixed(1)} km away';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        title: const Text('Hospital Alert'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/bystander/home'),
        ),
      ),
      body: SafeArea(
        child: _isLoading
            ? const Center(
                child: CircularProgressIndicator(color: AppColors.primaryRed),
              )
            : SingleChildScrollView(
                padding: const EdgeInsets.all(24),
                child: Column(
                  children: [
                    const SizedBox(height: 20),
 
                    // ── Hospital Icon ──
                    Container(
                      width: 100,
                      height: 100,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: AppColors.acceptGreen.withValues(alpha: 0.15),
                      ),
                      child: const Icon(
                        Icons.local_hospital,
                        size: 48,
                        color: AppColors.acceptGreen,
                      ),
                    ),
 
                    const SizedBox(height: 24),
 
                    const Text(
                      'Hospital Pre-Notified',
                      style: TextStyle(
                        color: AppColors.textPrimary,
                        fontSize: 24,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
 
                    const SizedBox(height: 8),
 
                    const Text(
                      'The nearest hospital has been alerted about the emergency and is preparing resources.',
                      textAlign: TextAlign.center,
                      style: TextStyle(color: AppColors.textSecondary, fontSize: 14),
                    ),
 
                    const SizedBox(height: 24),

                    // ── Volunteer Status Card ──
                    _buildVolunteerStatusCard(),

                    const SizedBox(height: 16),
 
                    // ── Hospital Info Card ──
                    if (_hospitalName != null)
                      MedirouteCard(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                Container(
                                  padding: const EdgeInsets.all(10),
                                  decoration: BoxDecoration(
                                    color: AppColors.primaryRed.withValues(alpha: 0.15),
                                    borderRadius: BorderRadius.circular(10),
                                  ),
                                  child: const Icon(
                                    Icons.local_hospital,
                                    color: AppColors.primaryRed,
                                  ),
                                ),
                                const SizedBox(width: 14),
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        _hospitalName!,
                                        style: const TextStyle(
                                          color: AppColors.textPrimary,
                                          fontSize: 16,
                                          fontWeight: FontWeight.w700,
                                        ),
                                      ),
                                      Text(
                                        _distanceText,
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
                            const Divider(height: 28, color: AppColors.divider),
                            _DetailRow(
                              icon: Icons.check_circle,
                              iconColor: AppColors.acceptGreen,
                              label: 'Notification Status',
                              value: 'Sent Successfully',
                            ),
                            const SizedBox(height: 12),
                            _DetailRow(
                              icon: Icons.phone,
                              iconColor: AppColors.textSecondary,
                              label: 'Emergency Line',
                              value: _hospitalPhone ?? 'Not set',
                            ),
                            const SizedBox(height: 12),
                            _DetailRow(
                              icon: Icons.location_on,
                              iconColor: AppColors.textSecondary,
                              label: 'Address',
                              value: _hospitalAddress ?? 'Not set',
                            ),
                          ],
                        ),
                      )
                    else
                      Container(
                        padding: const EdgeInsets.all(20),
                        decoration: BoxDecoration(
                          color: AppColors.cardBackground,
                          borderRadius: BorderRadius.circular(16),
                        ),
                        child: const Row(
                          children: [
                            Icon(Icons.info, color: AppColors.primaryRed),
                            SizedBox(width: 12),
                            Expanded(
                              child: Text(
                                'No hospital was notified for this event, or no hospital is within range.',
                                style: TextStyle(color: AppColors.textSecondary),
                              ),
                            ),
                          ],
                        ),
                      ),
 
                    const SizedBox(height: 32),
 
                    // ── Actions ──
                    if (_hospitalPhone != null && _hospitalPhone!.isNotEmpty) ...[
                      SizedBox(
                        width: double.infinity,
                        height: 52,
                        child: ElevatedButton.icon(
                          onPressed: _callHospital,
                          icon: const Icon(Icons.phone),
                          label: const Text(
                            'Call Hospital',
                            style: TextStyle(fontWeight: FontWeight.w700, fontSize: 16),
                          ),
                        ),
                      ),
                      const SizedBox(height: 12),
                    ],
 
                    SizedBox(
                      width: double.infinity,
                      height: 52,
                      child: OutlinedButton.icon(
                        onPressed: () => context.go(
                          '/bystander/first-aid',
                          extra: {
                            'emergencyType': _emergencyType ?? 'Other',
                            'emergencyId': widget.emergencyId,
                          },
                        ),
                        icon: const Icon(Icons.medical_services_outlined, color: AppColors.textPrimary),
                        style: OutlinedButton.styleFrom(
                          side: const BorderSide(color: AppColors.cardBorder),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(16),
                          ),
                        ),
                        label: const Text(
                          'AI First Aid Guidance',
                          style: TextStyle(
                            color: AppColors.textPrimary,
                            fontWeight: FontWeight.w600,
                            fontSize: 16,
                          ),
                        ),
                      ),
                    ),
 
                    const SizedBox(height: 12),
 
                    SizedBox(
                      width: double.infinity,
                      height: 52,
                      child: OutlinedButton.icon(
                        onPressed: () => context.go(
                          '/bystander/tracking',
                          extra: {'emergencyId': widget.emergencyId},
                        ),
                        icon: const Icon(Icons.map, color: AppColors.textPrimary),
                        style: OutlinedButton.styleFrom(
                          side: const BorderSide(color: AppColors.cardBorder),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(16),
                          ),
                        ),
                        label: const Text(
                          'Track Responders',
                          style: TextStyle(
                            color: AppColors.textPrimary,
                            fontWeight: FontWeight.w600,
                            fontSize: 16,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
        ),
    );
  }

  /// Build a real-time volunteer status card that shows searching/found states.
  Widget _buildVolunteerStatusCard() {
    final bool isFound = _volunteerStatus == 'found';

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isFound
            ? AppColors.acceptGreen.withValues(alpha: 0.1)
            : AppColors.cardBackground,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isFound
              ? AppColors.acceptGreen.withValues(alpha: 0.3)
              : AppColors.cardBorder,
        ),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: isFound
                  ? AppColors.acceptGreen.withValues(alpha: 0.15)
                  : const Color(0xFF42A5F5).withValues(alpha: 0.15),
              borderRadius: BorderRadius.circular(10),
            ),
            child: isFound
                ? const Icon(Icons.check_circle, color: AppColors.acceptGreen)
                : const SizedBox(
                    width: 24,
                    height: 24,
                    child: CircularProgressIndicator(
                      strokeWidth: 2.5,
                      color: Color(0xFF42A5F5),
                    ),
                  ),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  isFound
                      ? 'Volunteer Found!'
                      : 'Searching for Volunteers...',
                  style: TextStyle(
                    color: isFound ? AppColors.acceptGreen : AppColors.textPrimary,
                    fontSize: 16,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  isFound
                      ? '${_volunteerName ?? "Volunteer"} has accepted. Redirecting to tracking...'
                      : 'Notifying nearby volunteers within ${AppConstants.volunteerSearchRadiusKm.toStringAsFixed(0)}km',
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
    );
  }
}

class _DetailRow extends StatelessWidget {
  final IconData icon;
  final Color iconColor;
  final String label;
  final String value;

  const _DetailRow({
    required this.icon,
    required this.iconColor,
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(icon, size: 20, color: iconColor),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                label,
                style: const TextStyle(
                  color: AppColors.textSubdued,
                  fontSize: 12,
                ),
              ),
              Text(
                value,
                style: const TextStyle(
                  color: AppColors.textPrimary,
                  fontSize: 14,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
