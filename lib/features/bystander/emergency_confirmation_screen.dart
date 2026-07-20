import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../../core/theme/app_colors.dart';
import '../../core/widgets/mediroute_button.dart';
import '../../services/emergency_service.dart';

/// Confirms emergency details then creates real SOS in Firestore.
class EmergencyConfirmationScreen extends StatefulWidget {
  final String emergencyType;

  const EmergencyConfirmationScreen({super.key, required this.emergencyType});

  @override
  State<EmergencyConfirmationScreen> createState() =>
      _EmergencyConfirmationScreenState();
}

class _EmergencyConfirmationScreenState
    extends State<EmergencyConfirmationScreen> {
  bool _isLoading = false;
  String? _error;

  Future<void> _confirmAndSend() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final user = FirebaseAuth.instance.currentUser;
      if (user == null) {
        setState(() => _error = 'Not authenticated. Please sign in again.');
        return;
      }

      final emergencyService = EmergencyService();
      final emergency = await emergencyService.createEmergency(
        bystanderUid: user.uid,
        emergencyType: widget.emergencyType,
      );

      if (mounted) {
        context.go(
          '/bystander/hospital-alert',
          extra: {
            'emergencyId': emergency.emergencyId,
          },
        );
      }
    } catch (e) {
      setState(() {
        _error = 'Failed to send alert. Check GPS and try again.';
      });
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        title: const Text('Confirm Emergency'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/bystander/home'),
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Column(
            children: [
              const SizedBox(height: 16),

              // Emergency Icon
              Container(
                width: 100,
                height: 100,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: AppColors.primaryRed.withValues(alpha: 0.15),
                ),
                child: const Icon(
                  Icons.warning_amber_rounded,
                  size: 56,
                  color: AppColors.primaryRed,
                ),
              ),

              const SizedBox(height: 24),

              Text(
                'Sending Emergency Alert',
                style: Theme.of(context).textTheme.headlineMedium,
              ),

              const SizedBox(height: 12),

              Text(
                'You are about to send a real emergency alert for:',
                style: Theme.of(context).textTheme.bodyLarge,
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: 20),

              // Emergency Type Badge
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 24,
                  vertical: 14,
                ),
                decoration: BoxDecoration(
                  color: AppColors.primaryRed.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: AppColors.primaryRed),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.emergency, color: AppColors.primaryRed),
                    const SizedBox(width: 10),
                    Text(
                      widget.emergencyType,
                      style: const TextStyle(
                        color: AppColors.primaryRed,
                        fontSize: 18,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 28),

              // Info Items
              _InfoRow(
                icon: Icons.location_on,
                label: 'Location',
                value: 'Using current GPS coordinates',
              ),
              const SizedBox(height: 12),
              _InfoRow(
                icon: Icons.people,
                label: 'Volunteers',
                value: 'Will alert within 1km radius',
              ),
              const SizedBox(height: 12),
              _InfoRow(
                icon: Icons.local_hospital,
                label: 'Hospital',
                value: 'Nearest hospital will be notified',
              ),

              if (_error != null) ...[
                const SizedBox(height: 16),
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: AppColors.primaryRed.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Text(
                    _error!,
                    style: const TextStyle(
                      color: AppColors.primaryRed,
                      fontSize: 13,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ),
              ],

              const SizedBox(height: 32),

              // Confirm Button
              MedirouteButton(
                label: 'Confirm & Send Alert',
                icon: Icons.campaign,
                isLoading: _isLoading,
                onPressed: _confirmAndSend,
              ),

              const SizedBox(height: 12),

              MedirouteButton(
                label: 'Cancel',
                isOutlined: true,
                onPressed: () => context.go('/bystander/home'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _InfoRow extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;

  const _InfoRow({
    required this.icon,
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.cardBackground,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.cardBorder, width: 0.5),
      ),
      child: Row(
        children: [
          Icon(icon, color: AppColors.textSecondary, size: 22),
          const SizedBox(width: 12),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                label,
                style: const TextStyle(
                  color: AppColors.textSubdued,
                  fontSize: 12,
                  fontWeight: FontWeight.w500,
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
        ],
      ),
    );
  }
}
