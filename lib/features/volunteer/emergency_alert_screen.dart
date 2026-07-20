import 'dart:async';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../../core/theme/app_colors.dart';
import '../../services/emergency_service.dart';

/// Emergency alert screen — volunteer sees incoming emergency with countdown.
class EmergencyAlertScreen extends StatefulWidget {
  final String? emergencyId;
  final String? emergencyType;
  final double? distance;
  final double? latitude;
  final double? longitude;

  const EmergencyAlertScreen({
    super.key,
    this.emergencyId,
    this.emergencyType,
    this.distance,
    this.latitude,
    this.longitude,
  });

  @override
  State<EmergencyAlertScreen> createState() => _EmergencyAlertScreenState();
}

class _EmergencyAlertScreenState extends State<EmergencyAlertScreen>
    with SingleTickerProviderStateMixin {
  int _countdown = 10;
  Timer? _timer;
  late AnimationController _pulseController;
  bool _isAccepting = false;
  final EmergencyService _emergencyService = EmergencyService();

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    )..repeat(reverse: true);
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      setState(() => _countdown--);
      if (_countdown <= 0) {
        _timer?.cancel();
        if (mounted) context.go('/volunteer/dashboard');
      }
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    _pulseController.dispose();
    super.dispose();
  }

  String get _distanceText {
    final d = widget.distance ?? 0;
    if (d < 1000) return '${d.toInt()} m';
    return '${(d / 1000).toStringAsFixed(1)} km';
  }

  /// Accept the emergency: call service first, then navigate to navigation screen.
  Future<void> _acceptEmergency() async {
    if (_isAccepting) return;
    setState(() => _isAccepting = true);
    _timer?.cancel();

    try {
      final uid = FirebaseAuth.instance.currentUser?.uid;
      if (uid != null && widget.emergencyId != null) {
        await _emergencyService.acceptEmergency(
          emergencyId: widget.emergencyId!,
          volunteerUid: uid,
        );
      }

      if (mounted) {
        context.go(
          '/volunteer/navigation',
          extra: {
            'emergencyId': widget.emergencyId,
            'victimLat': widget.latitude,
            'victimLng': widget.longitude,
          },
        );
      }
    } catch (e) {
      // If acceptance failed (e.g. already assigned to another volunteer),
      // show error and go back to dashboard
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('This emergency was already accepted by another volunteer.'),
            backgroundColor: AppColors.primaryRed,
          ),
        );
        context.go('/volunteer/dashboard');
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            children: [
              const Spacer(),

              // Countdown ring
              AnimatedBuilder(
                animation: _pulseController,
                builder: (context, child) {
                  return Stack(
                    alignment: Alignment.center,
                    children: [
                      // Outer pulse
                      Container(
                        width: 180 + (_pulseController.value * 20),
                        height: 180 + (_pulseController.value * 20),
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          border: Border.all(
                            color: AppColors.primaryRed.withValues(alpha: 0.2),
                            width: 2,
                          ),
                        ),
                      ),
                      // Countdown ring
                      SizedBox(
                        width: 160,
                        height: 160,
                        child: CircularProgressIndicator(
                          value: _countdown / 10,
                          strokeWidth: 5,
                          backgroundColor: AppColors.primaryRed.withValues(
                            alpha: 0.15,
                          ),
                          valueColor: const AlwaysStoppedAnimation<Color>(
                            AppColors.primaryRed,
                          ),
                        ),
                      ),
                      // Center content
                      Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(
                            Icons.warning_amber_rounded,
                            color: AppColors.primaryRed,
                            size: 36,
                          ),
                          const SizedBox(height: 4),
                          Text(
                            '$_countdown',
                            style: const TextStyle(
                              color: AppColors.textPrimary,
                              fontSize: 40,
                              fontWeight: FontWeight.w900,
                            ),
                          ),
                          const Text(
                            'seconds',
                            style: TextStyle(
                              color: AppColors.textSubdued,
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ),
                    ],
                  );
                },
              ),

              const SizedBox(height: 32),

              const Text(
                'EMERGENCY NEARBY',
                style: TextStyle(
                  color: AppColors.primaryRed,
                  fontSize: 22,
                  fontWeight: FontWeight.w900,
                  letterSpacing: 2,
                ),
              ),

              const SizedBox(height: 24),

              // Info chips
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  _Chip(
                    icon: Icons.emergency,
                    label: widget.emergencyType ?? 'Unknown',
                  ),
                  const SizedBox(width: 12),
                  _Chip(icon: Icons.straighten, label: _distanceText),
                ],
              ),

              const Spacer(),

              // Accept
              SizedBox(
                width: double.infinity,
                height: 56,
                child: ElevatedButton.icon(
                  onPressed: _isAccepting ? null : _acceptEmergency,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primaryRed,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                  ),
                  icon: _isAccepting
                      ? const SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            color: Colors.white,
                          ),
                        )
                      : const Icon(Icons.check_circle, color: Colors.white),
                  label: Text(
                    _isAccepting ? 'Accepting...' : 'Accept Emergency',
                    style: const TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.w700,
                      fontSize: 16,
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 12),
              SizedBox(
                width: double.infinity,
                height: 56,
                child: OutlinedButton(
                  onPressed: _isAccepting
                      ? null
                      : () {
                          _timer?.cancel();
                          context.go('/volunteer/dashboard');
                        },
                  style: OutlinedButton.styleFrom(
                    side: const BorderSide(color: AppColors.textSubdued),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                  ),
                  child: const Text(
                    'Decline',
                    style: TextStyle(
                      color: AppColors.textSecondary,
                      fontWeight: FontWeight.w600,
                      fontSize: 16,
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 16),
            ],
          ),
        ),
      ),
    );
  }
}

class _Chip extends StatelessWidget {
  final IconData icon;
  final String label;
  const _Chip({required this.icon, required this.label});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
      decoration: BoxDecoration(
        color: AppColors.cardBackground,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.cardBorder),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, color: AppColors.primaryRed, size: 18),
          const SizedBox(width: 8),
          Text(
            label,
            style: const TextStyle(
              color: AppColors.textPrimary,
              fontWeight: FontWeight.w600,
              fontSize: 14,
            ),
          ),
        ],
      ),
    );
  }
}
