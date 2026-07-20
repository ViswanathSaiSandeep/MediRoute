import 'package:firebase_core/firebase_core.dart' show FirebaseOptions;
import 'package:flutter/foundation.dart' show defaultTargetPlatform, kIsWeb, TargetPlatform;

/// Default [FirebaseOptions] for use with your Firebase apps.
class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    if (kIsWeb) {
      return web;
    }
    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return android;
      default:
        throw UnsupportedError(
          'DefaultFirebaseOptions are not configured for this platform.',
        );
    }
  }

  static const FirebaseOptions web = FirebaseOptions(
    apiKey: 'YOUR_FIREBASE_API_KEY_WEB',
    appId: '1:345683130305:web:7a8689db740aefd2436140',
    messagingSenderId: '345683130305',
    projectId: 'mediroute-33e0c',
    authDomain: 'mediroute-33e0c.firebaseapp.com',
    storageBucket: 'mediroute-33e0c.firebasestorage.app',
    measurementId: 'G-TVD7YL7JSQ',
  );

  static const FirebaseOptions android = FirebaseOptions(
    apiKey: 'YOUR_FIREBASE_API_KEY_ANDROID',
    appId: '1:345683130305:android:a600fdcb358e6d13436140',
    messagingSenderId: '345683130305',
    projectId: 'mediroute-33e0c',
    storageBucket: 'mediroute-33e0c.firebasestorage.app',
  );
}
