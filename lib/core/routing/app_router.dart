import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../features/splash/splash_screen.dart';
import '../../features/auth/role_selection_screen.dart';
import '../../features/auth/bystander_auth_screen.dart';
import '../../features/auth/hospital_registration_screen.dart';
import '../../features/hospital/hospital_dashboard_screen.dart';
import '../../features/bystander/emergency_home_screen.dart';
import '../../features/bystander/emergency_confirmation_screen.dart';
import '../../features/bystander/first_aid_guidance_screen.dart';
import '../../features/bystander/volunteer_tracking_screen.dart';
import '../../features/bystander/hospital_alert_screen.dart';
import '../../features/bystander/hospital_map_screen.dart';
import '../../features/volunteer/volunteer_registration_screen.dart';
import '../../features/volunteer/volunteer_dashboard_screen.dart';
import '../../features/volunteer/emergency_alert_screen.dart';
import '../../features/volunteer/volunteer_navigation_screen.dart';
import '../../features/volunteer/case_completion_screen.dart';
import '../../features/shared/emergency_history_screen.dart';
import '../../features/shared/profile_screen.dart';

/// Application routing configuration using GoRouter.
class AppRouter {
  static final GoRouter router = GoRouter(
    initialLocation: '/',
    routes: [
      // ── Splash ──
      GoRoute(
        path: '/',
        name: 'splash',
        builder: (context, state) => const SplashScreen(),
      ),

      // ── Role Selection ──
      GoRoute(
        path: '/role-selection',
        name: 'role-selection',
        builder: (context, state) => const RoleSelectionScreen(),
      ),

      // ── Auth ──
      GoRoute(
        path: '/bystander/auth',
        name: 'bystander-auth',
        builder: (context, state) => const BystanderAuthScreen(),
      ),

      // ── Bystander Flow ──
      GoRoute(
        path: '/bystander/home',
        name: 'bystander-home',
        builder: (context, state) => const EmergencyHomeScreen(),
      ),
      GoRoute(
        path: '/bystander/confirm',
        name: 'bystander-confirm',
        builder: (context, state) {
          final extra = state.extra as Map<String, dynamic>?;
          return EmergencyConfirmationScreen(
            emergencyType: extra?['emergencyType'] as String? ?? 'Other',
          );
        },
      ),
      GoRoute(
        path: '/bystander/first-aid',
        name: 'bystander-first-aid',
        builder: (context, state) {
          final extra = state.extra as Map<String, dynamic>?;
          return FirstAidGuidanceScreen(
            emergencyType: extra?['emergencyType'] as String? ?? 'Other',
            emergencyId: extra?['emergencyId'] as String?,
          );
        },
      ),
      GoRoute(
        path: '/bystander/tracking',
        name: 'bystander-tracking',
        builder: (context, state) {
          final extra = state.extra as Map<String, dynamic>?;
          return VolunteerTrackingScreen(
            emergencyId: extra?['emergencyId'] as String?,
          );
        },
      ),
      GoRoute(
        path: '/bystander/hospital-alert',
        name: 'bystander-hospital-alert',
        builder: (context, state) {
          final extra = state.extra as Map<String, dynamic>?;
          return HospitalAlertScreen(
            emergencyId: extra?['emergencyId'] as String?,
          );
        },
      ),
      GoRoute(
        path: '/bystander/hospitals',
        name: 'bystander-hospitals',
        builder: (context, state) => const HospitalMapScreen(),
      ),

      // ── Hospital Flow ──
      GoRoute(
        path: '/hospital/register',
        name: 'hospital-register',
        builder: (context, state) => const HospitalRegistrationScreen(),
      ),
      GoRoute(
        path: '/hospital/dashboard',
        name: 'hospital-dashboard',
        builder: (context, state) => const HospitalDashboardScreen(),
      ),

      // ── Volunteer Flow ──
      GoRoute(
        path: '/volunteer/register',
        name: 'volunteer-register',
        builder: (context, state) => const VolunteerRegistrationScreen(),
      ),
      GoRoute(
        path: '/volunteer/dashboard',
        name: 'volunteer-dashboard',
        builder: (context, state) => const VolunteerDashboardScreen(),
      ),
      GoRoute(
        path: '/volunteer/alert',
        name: 'volunteer-alert',
        builder: (context, state) {
          final extra = state.extra as Map<String, dynamic>?;
          return EmergencyAlertScreen(
            emergencyId: extra?['emergencyId'] as String?,
            emergencyType: extra?['emergencyType'] as String?,
            distance: extra?['distance'] as double?,
            latitude: extra?['latitude'] as double?,
            longitude: extra?['longitude'] as double?,
          );
        },
      ),
      GoRoute(
        path: '/volunteer/navigation',
        name: 'volunteer-navigation',
        builder: (context, state) {
          final extra = state.extra as Map<String, dynamic>?;
          return VolunteerNavigationScreen(
            emergencyId: extra?['emergencyId'] as String?,
            victimLat: extra?['victimLat'] as double?,
            victimLng: extra?['victimLng'] as double?,
          );
        },
      ),
      GoRoute(
        path: '/volunteer/complete',
        name: 'volunteer-complete',
        builder: (context, state) {
          final extra = state.extra as Map<String, dynamic>?;
          return CaseCompletionScreen(
            emergencyId: extra?['emergencyId'] as String?,
          );
        },
      ),

      // ── Shared ──
      GoRoute(
        path: '/history',
        name: 'history',
        builder: (context, state) => const EmergencyHistoryScreen(),
      ),
      GoRoute(
        path: '/profile',
        name: 'profile',
        builder: (context, state) => const ProfileScreen(),
      ),
    ],
    errorBuilder: (context, state) => Scaffold(
      backgroundColor: const Color(0xFF1A0A0A),
      body: Center(
        child: Text(
          'Page not found',
          style: Theme.of(context).textTheme.headlineMedium,
        ),
      ),
    ),
  );
}
