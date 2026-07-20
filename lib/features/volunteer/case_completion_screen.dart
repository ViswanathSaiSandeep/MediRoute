import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../core/theme/app_colors.dart';
import '../../core/widgets/mediroute_button.dart';
import '../../services/emergency_service.dart';

/// Case completion — volunteer submits report after arrival.
class CaseCompletionScreen extends StatefulWidget {
  final String? emergencyId;

  const CaseCompletionScreen({super.key, this.emergencyId});

  @override
  State<CaseCompletionScreen> createState() => _CaseCompletionScreenState();
}

class _CaseCompletionScreenState extends State<CaseCompletionScreen> {
  final _notesController = TextEditingController();
  String _outcome = 'Stabilized';
  bool _isLoading = false;
  final EmergencyService _emergencyService = EmergencyService();

  @override
  void dispose() {
    _notesController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    setState(() => _isLoading = true);

    try {
      if (widget.emergencyId != null) {
        await _emergencyService.resolveEmergency(
          emergencyId: widget.emergencyId!,
          helpProvided: _notesController.text.trim(),
          outcome: _outcome,
        );
      }

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Case report submitted. Thank you!'),
            backgroundColor: Colors.green,
          ),
        );
        context.go('/volunteer/dashboard');
      }
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Failed to submit report. Please try again.'),
            backgroundColor: AppColors.primaryRed,
          ),
        );
      }
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
        title: const Text('Complete Case'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/volunteer/dashboard'),
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Success header
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: Colors.green.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(
                    color: Colors.green.withValues(alpha: 0.3),
                  ),
                ),
                child: const Column(
                  children: [
                    Icon(Icons.check_circle, color: Colors.green, size: 48),
                    SizedBox(height: 10),
                    Text(
                      'You have arrived!',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 20,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                    SizedBox(height: 4),
                    Text(
                      'Please complete the case report below.',
                      style: TextStyle(
                        color: AppColors.textSecondary,
                        fontSize: 13,
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 28),

              // Help description
              const Text(
                'What help did you provide?',
                style: TextStyle(
                  color: AppColors.textPrimary,
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 10),
              TextField(
                controller: _notesController,
                maxLines: 4,
                style: const TextStyle(
                  color: AppColors.textPrimary,
                  fontSize: 14,
                ),
                decoration: InputDecoration(
                  hintText: 'Describe what happened and actions taken...',
                  hintStyle: const TextStyle(
                    color: AppColors.textSubdued,
                    fontSize: 14,
                  ),
                  filled: true,
                  fillColor: AppColors.cardBackground,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(14),
                    borderSide: BorderSide(color: AppColors.cardBorder),
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(14),
                    borderSide: BorderSide(color: AppColors.cardBorder),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(14),
                    borderSide: const BorderSide(color: AppColors.primaryRed),
                  ),
                ),
              ),

              const SizedBox(height: 28),

              // Outcome
              const Text(
                'Outcome',
                style: TextStyle(
                  color: AppColors.textPrimary,
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 10),
              RadioGroup<String>(
                groupValue: _outcome,
                onChanged: (v) {
                  if (v != null) setState(() => _outcome = v);
                },
                child: Column(
                  children: ['Stabilized', 'Transported to Hospital', 'Cancelled'].map((
                    outcome,
                  ) {
                    return RadioListTile<String>(
                      value: outcome,
                      title: Text(
                        outcome,
                        style: const TextStyle(
                          color: AppColors.textPrimary,
                          fontSize: 15,
                        ),
                      ),
                      activeColor: AppColors.primaryRed,
                      contentPadding: EdgeInsets.zero,
                      dense: true,
                    );
                  }).toList(),
                ),
              ),

              const SizedBox(height: 32),

              MedirouteButton(
                label: 'Submit Report',
                icon: Icons.send,
                isLoading: _isLoading,
                onPressed: _submit,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
