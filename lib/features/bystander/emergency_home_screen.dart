import 'dart:async';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:url_launcher/url_launcher.dart';
import '../../core/theme/app_colors.dart';
import '../../core/constants/app_constants.dart';

/// Bystander emergency home screen — SOS button, emergency type selector, GPS toggle.
/// Matches the mockup with large central SOS button and bottom navigation.
class EmergencyHomeScreen extends StatefulWidget {
  const EmergencyHomeScreen({super.key});

  @override
  State<EmergencyHomeScreen> createState() => _EmergencyHomeScreenState();
}

class _EmergencyHomeScreenState extends State<EmergencyHomeScreen>
    with SingleTickerProviderStateMixin {
  String? _selectedEmergencyType;
  bool _gpsEnabled = true;
  bool _isHolding = false;
  double _holdProgress = 0.0;
  Timer? _holdTimer;
  late AnimationController _pulseController;
  int _currentNavIndex = 0;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _holdTimer?.cancel();
    _pulseController.dispose();
    super.dispose();
  }

  void _startHold() {
    setState(() {
      _isHolding = true;
      _holdProgress = 0.0;
    });

    _holdTimer = Timer.periodic(const Duration(milliseconds: 50), (timer) {
      setState(() {
        _holdProgress +=
            0.05 / AppConstants.sosHoldDurationSeconds; // Normalized to 1.0
      });

      if (_holdProgress >= 1.0) {
        timer.cancel();
        _triggerSOS();
      }
    });
  }

  void _cancelHold() {
    _holdTimer?.cancel();
    setState(() {
      _isHolding = false;
      _holdProgress = 0.0;
    });
  }

  void _triggerSOS() {
    setState(() {
      _isHolding = false;
    });
    // Navigate to confirmation screen
    context.go(
      '/bystander/confirm',
      extra: {'emergencyType': _selectedEmergencyType ?? 'Other'},
    );
  }

  void _callEmergency() async {
    try {
      final uri = Uri.parse('tel:${AppConstants.emergencyNumber}');
      await launchUrl(uri);
    } catch (e) {
      debugPrint('Could not launch emergency call: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: Column(
          children: [
            // ── Top Bar ──
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
              child: Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: AppColors.primaryRed.withValues(alpha: 0.2),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Icon(
                      Icons.medical_services,
                      color: AppColors.primaryRed,
                      size: 24,
                    ),
                  ),
                  const SizedBox(width: 12),
                  const Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'MediRoute',
                        style: TextStyle(
                          color: AppColors.textPrimary,
                          fontSize: 18,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                      Text(
                        'Bystander Mode',
                        style: TextStyle(
                          color: AppColors.textSecondary,
                          fontSize: 12,
                        ),
                      ),
                    ],
                  ),
                  const Spacer(),
                  IconButton(
                    icon: const Icon(
                      Icons.settings,
                      color: AppColors.textSecondary,
                    ),
                    onPressed: () => context.go('/profile'),
                  ),
                ],
              ),
            ),

            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: 20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const SizedBox(height: 8),

                    // ── Emergency Type Selector ──
                    const Text(
                      'Emergency Type',
                      style: TextStyle(
                        color: AppColors.primaryRed,
                        fontWeight: FontWeight.w600,
                        fontSize: 14,
                      ),
                    ),
                    const SizedBox(height: 8),
                    GestureDetector(
                      onTap: _showEmergencyTypePicker,
                      child: Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 16,
                        ),
                        decoration: BoxDecoration(
                          color: AppColors.cardBackground,
                          borderRadius: BorderRadius.circular(14),
                          border: Border.all(color: AppColors.cardBorder),
                        ),
                        child: Row(
                          children: [
                            const Icon(
                              Icons.emergency,
                              color: AppColors.primaryRed,
                              size: 22,
                            ),
                            const SizedBox(width: 12),
                            Text(
                              _selectedEmergencyType ?? 'Select Emergency Type',
                              style: TextStyle(
                                color: _selectedEmergencyType != null
                                    ? AppColors.textPrimary
                                    : AppColors.textSubdued,
                                fontSize: 16,
                              ),
                            ),
                            const Spacer(),
                            const Icon(
                              Icons.expand_more,
                              color: AppColors.textSubdued,
                            ),
                          ],
                        ),
                      ),
                    ),

                    const SizedBox(height: 32),

                    // ── SOS Button Area ──
                    Center(
                      child: GestureDetector(
                        onLongPressStart: (_) => _startHold(),
                        onLongPressEnd: (_) => _cancelHold(),
                        onLongPressCancel: _cancelHold,
                        child: AnimatedBuilder(
                          animation: _pulseController,
                          builder: (context, child) {
                            final pulseValue = _pulseController.value;
                            return Stack(
                              alignment: Alignment.center,
                              children: [
                                // Outer pulse rings
                                if (!_isHolding) ...[
                                  Container(
                                    width: 280 + (pulseValue * 20),
                                    height: 280 + (pulseValue * 20),
                                    decoration: BoxDecoration(
                                      shape: BoxShape.circle,
                                      border: Border.all(
                                        color: AppColors.primaryRed.withValues(
                                          alpha: 0.1,
                                        ),
                                        width: 1,
                                      ),
                                    ),
                                  ),
                                  Container(
                                    width: 240 + (pulseValue * 10),
                                    height: 240 + (pulseValue * 10),
                                    decoration: BoxDecoration(
                                      shape: BoxShape.circle,
                                      border: Border.all(
                                        color: AppColors.primaryRed.withValues(
                                          alpha: 0.2,
                                        ),
                                        width: 1.5,
                                      ),
                                    ),
                                  ),
                                ],

                                // Hold progress ring
                                if (_isHolding)
                                  SizedBox(
                                    width: 220,
                                    height: 220,
                                    child: CircularProgressIndicator(
                                      value: _holdProgress,
                                      strokeWidth: 6,
                                      backgroundColor: AppColors.primaryRed
                                          .withValues(alpha: 0.2),
                                      valueColor:
                                          const AlwaysStoppedAnimation<Color>(
                                            AppColors.accentRed,
                                          ),
                                    ),
                                  ),

                                // Main SOS button
                                Container(
                                  width: 180,
                                  height: 180,
                                  decoration: BoxDecoration(
                                    shape: BoxShape.circle,
                                    gradient: RadialGradient(
                                      colors: [
                                        _isHolding
                                            ? AppColors.accentRed
                                            : AppColors.primaryRed,
                                        const Color(0xFFB71C1C),
                                      ],
                                    ),
                                    boxShadow: [
                                      BoxShadow(
                                        color: AppColors.primaryRed.withValues(
                                          alpha: _isHolding ? 0.6 : 0.3,
                                        ),
                                        blurRadius: _isHolding ? 40 : 24,
                                        spreadRadius: _isHolding ? 10 : 4,
                                      ),
                                    ],
                                  ),
                                  child: Column(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      const Icon(
                                        Icons.cell_tower,
                                        size: 36,
                                        color: Colors.white,
                                      ),
                                      const SizedBox(height: 4),
                                      const Text(
                                        'SOS',
                                        style: TextStyle(
                                          fontSize: 32,
                                          fontWeight: FontWeight.w900,
                                          color: Colors.white,
                                          letterSpacing: 4,
                                        ),
                                      ),
                                      Container(
                                        padding: const EdgeInsets.symmetric(
                                          horizontal: 12,
                                          vertical: 4,
                                        ),
                                        decoration: BoxDecoration(
                                          color: Colors.white.withValues(
                                            alpha: 0.2,
                                          ),
                                          borderRadius: BorderRadius.circular(
                                            12,
                                          ),
                                        ),
                                        child: const Text(
                                          'HOLD 3 SEC',
                                          style: TextStyle(
                                            fontSize: 11,
                                            fontWeight: FontWeight.w600,
                                            color: Colors.white,
                                          ),
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ],
                            );
                          },
                        ),
                      ),
                    ),

                    const SizedBox(height: 32),

                    // ── GPS Toggle ──
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: AppColors.cardBackground,
                        borderRadius: BorderRadius.circular(14),
                        border: Border.all(color: AppColors.cardBorder),
                      ),
                      child: Row(
                        children: [
                          Icon(
                            Icons.my_location,
                            color: _gpsEnabled
                                ? const Color(0xFF42A5F5)
                                : AppColors.textSubdued,
                          ),
                          const SizedBox(width: 12),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text(
                                'GPS Tracking',
                                style: TextStyle(
                                  color: AppColors.textPrimary,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                              Text(
                                _gpsEnabled
                                    ? 'Precise location enabled'
                                    : 'Location disabled',
                                style: const TextStyle(
                                  color: AppColors.textSecondary,
                                  fontSize: 12,
                                ),
                              ),
                            ],
                          ),
                          const Spacer(),
                          Switch(
                            value: _gpsEnabled,
                            activeThumbColor: const Color(0xFF42A5F5),
                            onChanged: _toggleGps,
                          ),
                        ],
                      ),
                    ),

                    const SizedBox(height: 16),

                    // ── Quick Call 108 ──
                    SizedBox(
                      width: double.infinity,
                      height: 56,
                      child: ElevatedButton.icon(
                        onPressed: _callEmergency,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.textPrimary,
                          foregroundColor: AppColors.background,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(16),
                          ),
                        ),
                        icon: const Icon(Icons.phone),
                        label: const Text(
                          'Quick Call 108',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                      ),
                    ),

                    const SizedBox(height: 12),

                    Center(
                      child: Text(
                        'Pressing SOS will alert nearby responders immediately.',
                        style: TextStyle(
                          fontSize: 12,
                          color: AppColors.textSubdued,
                        ),
                      ),
                    ),

                    const SizedBox(height: 20),
                  ],
                ),
              ),
            ),

            // ── Bottom Navigation ──
            Container(
              decoration: const BoxDecoration(
                color: AppColors.backgroundDark,
                border: Border(top: BorderSide(color: AppColors.divider)),
              ),
              child: BottomNavigationBar(
                currentIndex: _currentNavIndex,
                onTap: (i) {
                  setState(() => _currentNavIndex = i);
                  switch (i) {
                    case 1:
                      context.go(
                        '/bystander/first-aid',
                        extra: {'emergencyType': 'General'},
                      );
                      break;
                    case 2:
                      context.go('/bystander/hospitals');
                      break;
                    case 3:
                      context.go('/profile');
                      break;
                  }
                },
                backgroundColor: AppColors.backgroundDark,
                selectedItemColor: AppColors.primaryRed,
                unselectedItemColor: AppColors.textSubdued,
                type: BottomNavigationBarType.fixed,
                elevation: 0,
                items: const [
                  BottomNavigationBarItem(
                    icon: Icon(Icons.home),
                    label: 'Home',
                  ),
                  BottomNavigationBarItem(
                    icon: Icon(Icons.medical_information),
                    label: 'First Aid',
                  ),
                  BottomNavigationBarItem(icon: Icon(Icons.map), label: 'Map'),
                  BottomNavigationBarItem(
                    icon: Icon(Icons.person),
                    label: 'Profile',
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _toggleGps(bool value) {
    if (!value) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          backgroundColor: AppColors.cardBackground,
          title: const Text('Disable GPS?', style: TextStyle(color: AppColors.textPrimary)),
          content: const Text(
            'Disabling GPS means nearby volunteers will not be able to locate you. The system will fall back to manual positioning.',
            style: TextStyle(color: AppColors.textSecondary),
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(context);
              },
              child: const Text('Keep GPS On', style: TextStyle(color: Color(0xFF42A5F5))),
            ),
            TextButton(
              onPressed: () {
                setState(() => _gpsEnabled = false);
                Navigator.pop(context);
              },
              child: const Text('Disable', style: TextStyle(color: AppColors.primaryRed)),
            ),
          ],
        ),
      );
    } else {
      setState(() => _gpsEnabled = true);
    }
  }

  void _showEmergencyTypePicker() {
    showModalBottomSheet(
      context: context,
      backgroundColor: AppColors.cardBackground,
      isScrollControlled: true,
      useSafeArea: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      constraints: BoxConstraints(
        maxHeight: MediaQuery.of(context).size.height * 0.6,
      ),
      builder: (context) {
        return Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Select Emergency Type',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w700,
                  color: AppColors.textPrimary,
                ),
              ),
              const SizedBox(height: 16),
              ...AppConstants.emergencyTypes.map((type) {
                return ListTile(
                  leading: const Icon(
                    Icons.emergency,
                    color: AppColors.primaryRed,
                  ),
                  title: Text(
                    type,
                    style: const TextStyle(color: AppColors.textPrimary),
                  ),
                  onTap: () {
                    setState(() => _selectedEmergencyType = type);
                    Navigator.pop(context);
                  },
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                );
              }),
            ],
          ),
        );
      },
    );
  }
}
