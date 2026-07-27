import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../../core/theme/app_colors.dart';
import '../../core/widgets/mediroute_button.dart';
import '../../core/widgets/mediroute_text_field.dart';
import '../../services/notification_service.dart';
import '../../data/models/user_model.dart';

/// Bystander authentication screen — sign up or log in before accessing SOS.
class BystanderAuthScreen extends StatefulWidget {
  const BystanderAuthScreen({super.key});

  @override
  State<BystanderAuthScreen> createState() => _BystanderAuthScreenState();
}

class _BystanderAuthScreenState extends State<BystanderAuthScreen> {
  final _nameController = TextEditingController();
  final _phoneController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLogin = false;
  bool _isLoading = false;
  String? _errorMessage;

  @override
  void dispose() {
    _nameController.dispose();
    _phoneController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    final email = _emailController.text.trim();
    final password = _passwordController.text.trim();

    if (email.isEmpty || password.isEmpty) {
      setState(() => _errorMessage = 'Email and password are required.');
      return;
    }
    if (!_isLogin && _nameController.text.trim().isEmpty) {
      setState(() => _errorMessage = 'Name is required.');
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final auth = FirebaseAuth.instance;
      UserCredential credential;

      if (_isLogin) {
        credential = await auth.signInWithEmailAndPassword(
          email: email,
          password: password,
        );
      } else {
        credential = await auth.createUserWithEmailAndPassword(
          email: email,
          password: password,
        );

        // Save user profile to Firestore
        final fcmToken = await NotificationService().getToken();
        final user = UserModel(
          uid: credential.user!.uid,
          role: 'bystander',
          name: _nameController.text.trim(),
          email: email,
          phone: _phoneController.text.trim(),
          createdAt: DateTime.now(),
          fcmToken: fcmToken,
        );

        await FirebaseFirestore.instance
            .collection('users')
            .doc(credential.user!.uid)
            .set(user.toJson());
      }

      if (mounted) {
        context.go('/bystander/home');
      }
    } on FirebaseAuthException catch (e) {
      setState(() {
        _errorMessage = _getAuthErrorMessage(e.code);
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'An unexpected error occurred. Please try again.';
      });
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  String _getAuthErrorMessage(String code) {
    switch (code) {
      case 'email-already-in-use':
        return 'This email is already registered. Try logging in.';
      case 'invalid-email':
        return 'Please enter a valid email address.';
      case 'weak-password':
        return 'Password must be at least 6 characters.';
      case 'user-not-found':
        return 'No account found with this email.';
      case 'wrong-password':
        return 'Incorrect password. Please try again.';
      case 'invalid-credential':
        return 'Invalid credentials. Check your email and password.';
      default:
        return 'Authentication failed. Please try again.';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        title: const Text('MediRoute'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/role-selection'),
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: AppColors.primaryRed.withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Icon(
                      Icons.medical_services,
                      color: AppColors.primaryRed,
                      size: 28,
                    ),
                  ),
                  const SizedBox(width: 14),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        _isLogin ? 'Welcome Back' : 'Bystander Sign Up',
                        style: const TextStyle(
                          color: AppColors.textPrimary,
                          fontSize: 24,
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                      Text(
                        _isLogin
                            ? 'Log in to access emergency SOS'
                            : 'Create an account to report emergencies',
                        style: const TextStyle(
                          color: AppColors.textSecondary,
                          fontSize: 13,
                        ),
                      ),
                    ],
                  ),
                ],
              ),

              const SizedBox(height: 32),

              // Error message
              if (_errorMessage != null) ...[
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: AppColors.primaryRed.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: AppColors.primaryRed.withValues(alpha: 0.3),
                    ),
                  ),
                  child: Row(
                    children: [
                      const Icon(
                        Icons.error_outline,
                        color: AppColors.primaryRed,
                        size: 20,
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          _errorMessage!,
                          style: const TextStyle(
                            color: AppColors.primaryRed,
                            fontSize: 13,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 20),
              ],

              // Name (sign up only)
              if (!_isLogin) ...[
                MedirouteTextField(
                  label: 'Full Name',
                  hint: 'Enter your full name',
                  prefixIcon: Icons.person,
                  controller: _nameController,
                ),
                const SizedBox(height: 18),

                MedirouteTextField(
                  label: 'Phone Number',
                  hint: '+91 XXXXX XXXXX',
                  prefixIcon: Icons.phone,
                  controller: _phoneController,
                  keyboardType: TextInputType.phone,
                ),
                const SizedBox(height: 18),
              ],

              MedirouteTextField(
                label: 'Email Address',
                hint: 'you@example.com',
                prefixIcon: Icons.email,
                controller: _emailController,
                keyboardType: TextInputType.emailAddress,
              ),

              const SizedBox(height: 18),

              MedirouteTextField(
                label: 'Password',
                hint: 'Min. 6 characters',
                prefixIcon: Icons.lock,
                controller: _passwordController,
                obscureText: true,
              ),

              const SizedBox(height: 28),

              // Submit
              MedirouteButton(
                label: _isLogin ? 'Log In' : 'Create Account',
                icon: _isLogin ? Icons.login : Icons.person_add,
                isLoading: _isLoading,
                onPressed: _submit,
              ),

              const SizedBox(height: 20),

              // Toggle login/signup
              Center(
                child: GestureDetector(
                  onTap: () => setState(() {
                    _isLogin = !_isLogin;
                    _errorMessage = null;
                  }),
                  child: RichText(
                    text: TextSpan(
                      children: [
                        TextSpan(
                          text: _isLogin
                              ? "Don't have an account? "
                              : 'Already have an account? ',
                          style: const TextStyle(
                            color: AppColors.textSecondary,
                            fontSize: 14,
                          ),
                        ),
                        TextSpan(
                          text: _isLogin ? 'Sign Up' : 'Log In',
                          style: const TextStyle(
                            color: AppColors.primaryRed,
                            fontWeight: FontWeight.w700,
                            fontSize: 14,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),

              const SizedBox(height: 32),
            ],
          ),
        ),
      ),
    );
  }
}
