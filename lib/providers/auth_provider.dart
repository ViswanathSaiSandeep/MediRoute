import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../services/auth_service.dart';

/// Provides the AuthService singleton.
final authServiceProvider = Provider<AuthService>((ref) => AuthService());

/// Stream of Firebase auth state changes.
final authStateProvider = StreamProvider<User?>((ref) {
  return ref.watch(authServiceProvider).authStateChanges;
});

/// The currently authenticated user (or null).
final currentFirebaseUserProvider = Provider<User?>((ref) {
  return ref.watch(authStateProvider).asData?.value;
});
