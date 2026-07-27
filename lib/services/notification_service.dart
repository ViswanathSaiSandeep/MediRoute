import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import '../core/routing/app_router.dart';

/// Handles Firebase Cloud Messaging — token management and notification handling.
class NotificationService {
  final FirebaseMessaging _messaging = FirebaseMessaging.instance;

  /// Initialize FCM and request notification permissions.
  Future<void> initialize() async {
    // Request permission (required for Android 13+)
    final settings = await _messaging.requestPermission(
      alert: true,
      badge: true,
      sound: true,
      criticalAlert: true, // Important for emergency alerts
    );

    debugPrint('FCM permission status: ${settings.authorizationStatus}');

    // Handle foreground messages
    FirebaseMessaging.onMessage.listen(_handleForegroundMessage);

    // Handle messages that opened the app from background
    FirebaseMessaging.onMessageOpenedApp.listen(_handleBackgroundMessage);

    // Check if app was opened from a terminated state notification
    final initialMessage = await _messaging.getInitialMessage();
    if (initialMessage != null) {
      _handleBackgroundMessage(initialMessage);
    }
  }

  /// Get the FCM device token for this device.
  Future<String?> getToken() async {
    if (kIsWeb) return null;
    return await _messaging.getToken();
  }

  /// Subscribe to a topic (e.g., volunteer alerts for a region).
  Future<void> subscribeToTopic(String topic) async {
    if (kIsWeb) return;
    await _messaging.subscribeToTopic(topic);
  }

  /// Unsubscribe from a topic.
  Future<void> unsubscribeFromTopic(String topic) async {
    if (kIsWeb) return;
    await _messaging.unsubscribeFromTopic(topic);
  }

  /// Handle foreground messages — show local alert.
  void _handleForegroundMessage(RemoteMessage message) {
    debugPrint('Foreground message received: ${message.messageId}');
    final notification = message.notification;
    final data = message.data;

    final context = AppRouter.router.routerDelegate.navigatorKey.currentContext;
    if (context == null || notification == null) return;

    // Show custom themed alert dialog
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF2A1212),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: const Row(
          children: [
            Icon(Icons.warning_amber_rounded, color: Color(0xFFE53935)),
            SizedBox(width: 8),
            Text(
              'EMERGENCY ALERT',
              style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 18),
            ),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              notification.title ?? 'New SOS Alert',
              style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14),
            ),
            const SizedBox(height: 6),
            Text(
              notification.body ?? 'An active emergency SOS has been reported nearby.',
              style: const TextStyle(color: Color(0xFFB0B0B0), fontSize: 13),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Dismiss', style: TextStyle(color: Color(0xFF757575))),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              // Extract fields and navigate to volunteer alert screen
              final emergencyId = data['emergencyId'] as String?;
              final emergencyType = data['emergencyType'] as String? ?? data['type'] as String? ?? 'Emergency';
              final distanceStr = data['distance'] as String?;
              final latStr = data['latitude'] as String?;
              final lngStr = data['longitude'] as String?;

              final distance = distanceStr != null ? double.tryParse(distanceStr) : null;
              final latitude = latStr != null ? double.tryParse(latStr) : null;
              final longitude = lngStr != null ? double.tryParse(lngStr) : null;

              AppRouter.router.go(
                '/volunteer/alert',
                extra: {
                  'emergencyId': emergencyId,
                  'emergencyType': emergencyType,
                  'distance': distance,
                  'latitude': latitude,
                  'longitude': longitude,
                },
              );
            },
            child: const Text(
              'Respond',
              style: TextStyle(color: Color(0xFFE53935), fontWeight: FontWeight.bold),
            ),
          ),
        ],
      ),
    );
  }

  /// Handle messages from background/terminated state.
  void _handleBackgroundMessage(RemoteMessage message) {
    debugPrint('Background message opened: ${message.messageId}');
    final data = message.data;

    // Navigate to volunteer alert screen
    final emergencyId = data['emergencyId'] as String?;
    final emergencyType = data['emergencyType'] as String? ?? data['type'] as String? ?? 'Emergency';
    final distanceStr = data['distance'] as String?;
    final latStr = data['latitude'] as String?;
    final lngStr = data['longitude'] as String?;

    final distance = distanceStr != null ? double.tryParse(distanceStr) : null;
    final latitude = latStr != null ? double.tryParse(latStr) : null;
    final longitude = lngStr != null ? double.tryParse(lngStr) : null;

    AppRouter.router.go(
      '/volunteer/alert',
      extra: {
        'emergencyId': emergencyId,
        'emergencyType': emergencyType,
        'distance': distance,
        'latitude': latitude,
        'longitude': longitude,
      },
    );
  }
}

/// Top-level background message handler (must be a top-level function).
@pragma('vm:entry-point')
Future<void> firebaseMessagingBackgroundHandler(RemoteMessage message) async {
  debugPrint('Background message: ${message.messageId}');
}
