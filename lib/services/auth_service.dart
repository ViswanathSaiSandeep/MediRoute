import 'package:firebase_auth/firebase_auth.dart';

/// Handles Firebase Authentication — anonymous for bystanders, email for volunteers.
class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;

  /// Stream of authentication state changes.
  Stream<User?> get authStateChanges => _auth.authStateChanges();

  /// Currently signed-in user.
  User? get currentUser => _auth.currentUser;

  /// Sign in anonymously (bystander mode — no registration needed).
  Future<UserCredential> signInAnonymously() async {
    return await _auth.signInAnonymously();
  }

  /// Sign in with email and password (volunteer accounts).
  Future<UserCredential> signInWithEmail({
    required String email,
    required String password,
  }) async {
    return await _auth.signInWithEmailAndPassword(
      email: email,
      password: password,
    );
  }

  /// Register new volunteer with email and password.
  Future<UserCredential> registerWithEmail({
    required String email,
    required String password,
  }) async {
    return await _auth.createUserWithEmailAndPassword(
      email: email,
      password: password,
    );
  }

  /// Sign out current user.
  Future<void> signOut() async {
    await _auth.signOut();
  }
}
