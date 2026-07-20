import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../../core/theme/app_colors.dart';
import '../../core/constants/app_constants.dart';

/// Splash screen — checks auth state and routes accordingly.
class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _fadeAnimation;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 2000),
    );

    _fadeAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(parent: _controller, curve: Curves.easeIn));

    _scaleAnimation = Tween<double>(
      begin: 0.8,
      end: 1.0,
    ).animate(CurvedAnimation(parent: _controller, curve: Curves.easeOutBack));

    _controller.forward();

    // Check auth and navigate after animation
    Future.delayed(const Duration(seconds: 3), () {
      if (mounted) _checkAuthAndNavigate();
    });
  }

  Future<void> _checkAuthAndNavigate() async {
    final user = FirebaseAuth.instance.currentUser;

    if (user == null) {
      // Not logged in
      if (mounted) context.go('/role-selection');
      return;
    }

    // User is logged in — check their role from Firestore
    try {
      final doc = await FirebaseFirestore.instance
          .collection(AppConstants.usersCollection)
          .doc(user.uid)
          .get();

      if (!mounted) return;

      if (doc.exists) {
        final role = doc.data()?['role'] as String?;
        if (role == 'volunteer') {
          context.go('/volunteer/dashboard');
        } else if (role == 'hospital') {
          context.go('/hospital/dashboard');
        } else {
          context.go('/bystander/home');
        }
      } else {
        // User exists in auth but not in Firestore — go to role selection
        context.go('/role-selection');
      }
    } catch (_) {
      // Fallback to role selection on error
      if (mounted) context.go('/role-selection');
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: Container(
        width: double.infinity,
        decoration: const BoxDecoration(
          gradient: RadialGradient(
            center: Alignment.center,
            radius: 1.2,
            colors: [Color(0xFF2D1111), AppColors.background],
          ),
        ),
        child: FadeTransition(
          opacity: _fadeAnimation,
          child: ScaleTransition(
            scale: _scaleAnimation,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Spacer(flex: 3),

                // Logo
                Container(
                  width: 140,
                  height: 140,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    gradient: const RadialGradient(
                      colors: [AppColors.primaryRed, Color(0xFFB71C1C)],
                    ),
                    boxShadow: [
                      BoxShadow(
                        color: AppColors.primaryRed.withValues(alpha: 0.4),
                        blurRadius: 40,
                        spreadRadius: 10,
                      ),
                    ],
                  ),
                  child: const Icon(
                    Icons.medical_services_rounded,
                    size: 64,
                    color: Colors.white,
                  ),
                ),

                const SizedBox(height: 32),

                RichText(
                  text: const TextSpan(
                    style: TextStyle(
                      fontSize: 36,
                      fontWeight: FontWeight.w800,
                      letterSpacing: 1,
                    ),
                    children: [
                      TextSpan(
                        text: 'Medi',
                        style: TextStyle(color: AppColors.textPrimary),
                      ),
                      TextSpan(
                        text: 'Route',
                        style: TextStyle(color: AppColors.primaryRed),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 8),

                Text(
                  'Help arrives faster.',
                  style: TextStyle(
                    fontSize: 16,
                    color: AppColors.textSecondary,
                    letterSpacing: 0.5,
                  ),
                ),

                const Spacer(flex: 4),

                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 80),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(4),
                    child: const LinearProgressIndicator(
                      backgroundColor: AppColors.progressTrack,
                      valueColor: AlwaysStoppedAnimation<Color>(
                        AppColors.primaryRed,
                      ),
                    ),
                  ),
                ),

                const SizedBox(height: 12),

                Text(
                  'Initializing...',
                  style: TextStyle(fontSize: 13, color: AppColors.textSubdued),
                ),

                const SizedBox(height: 32),

                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      Icons.verified_user_outlined,
                      size: 16,
                      color: AppColors.textSubdued,
                    ),
                    const SizedBox(width: 6),
                    Text(
                      'Secure Connection',
                      style: TextStyle(
                        fontSize: 12,
                        color: AppColors.textSubdued,
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 48),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
