import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../../core/theme/app_colors.dart';
import '../../core/widgets/mediroute_button.dart';
import '../../core/widgets/mediroute_text_field.dart';
import '../../core/constants/app_constants.dart';
import '../../data/models/user_model.dart';
import '../../services/notification_service.dart';

/// Volunteer registration + authentication screen.
class VolunteerRegistrationScreen extends StatefulWidget {
  const VolunteerRegistrationScreen({super.key});

  @override
  State<VolunteerRegistrationScreen> createState() =>
      _VolunteerRegistrationScreenState();
}

class _VolunteerRegistrationScreenState
    extends State<VolunteerRegistrationScreen> {
  final _nameController = TextEditingController();
  final _phoneController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final List<String> _selectedSkills = [];
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

        final fcmToken = await NotificationService().getToken();
        final user = UserModel(
          uid: credential.user!.uid,
          role: 'volunteer',
          name: _nameController.text.trim(),
          email: email,
          phone: _phoneController.text.trim(),
          skills: _selectedSkills,
          availability: true,
          createdAt: DateTime.now(),
          fcmToken: fcmToken,
        );

        await FirebaseFirestore.instance
            .collection(AppConstants.usersCollection)
            .doc(credential.user!.uid)
            .set(user.toJson());
      }

      if (mounted) context.go('/volunteer/dashboard');
    } on FirebaseAuthException catch (e) {
      setState(() {
        _errorMessage = _getAuthErrorMessage(e.code);
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'An unexpected error occurred.';
      });
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  String _getAuthErrorMessage(String code) {
    switch (code) {
      case 'email-already-in-use':
        return 'Email already registered. Try logging in.';
      case 'weak-password':
        return 'Password must be at least 6 characters.';
      case 'user-not-found':
        return 'No account found with this email.';
      case 'wrong-password':
      case 'invalid-credential':
        return 'Invalid credentials. Check email and password.';
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
        title: const Text('Volunteer'),
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
                      color: const Color(0xFF42A5F5).withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Icon(
                      Icons.volunteer_activism,
                      color: Color(0xFF42A5F5),
                      size: 28,
                    ),
                  ),
                  const SizedBox(width: 14),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        _isLogin ? 'Welcome Back' : 'Register as Volunteer',
                        style: const TextStyle(
                          color: AppColors.textPrimary,
                          fontSize: 22,
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                      Text(
                        _isLogin
                            ? 'Log in to respond to emergencies'
                            : 'Help save lives in your community',
                        style: const TextStyle(
                          color: AppColors.textSecondary,
                          fontSize: 13,
                        ),
                      ),
                    ],
                  ),
                ],
              ),

              const SizedBox(height: 24),

              // Error
              if (_errorMessage != null) ...[
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(12),
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
                        size: 18,
                      ),
                      const SizedBox(width: 8),
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
                const SizedBox(height: 16),
              ],

              // Form
              if (!_isLogin) ...[
                MedirouteTextField(
                  label: 'Full Name',
                  hint: 'Enter your full name',
                  prefixIcon: Icons.person,
                  controller: _nameController,
                ),
                const SizedBox(height: 16),
                MedirouteTextField(
                  label: 'Phone Number',
                  hint: '+91 XXXXX XXXXX',
                  prefixIcon: Icons.phone,
                  controller: _phoneController,
                  keyboardType: TextInputType.phone,
                ),
                const SizedBox(height: 16),
              ],

              MedirouteTextField(
                label: 'Email Address',
                hint: 'you@example.com',
                prefixIcon: Icons.email,
                controller: _emailController,
                keyboardType: TextInputType.emailAddress,
              ),
              const SizedBox(height: 16),

              MedirouteTextField(
                label: 'Password',
                hint: 'Min. 6 characters',
                prefixIcon: Icons.lock,
                controller: _passwordController,
                obscureText: true,
              ),

              // Skills (sign up only)
              if (!_isLogin) ...[
                const SizedBox(height: 24),
                const Text(
                  'Medical Skills / Certifications',
                  style: TextStyle(
                    color: AppColors.textPrimary,
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 10),
                Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: AppConstants.medicalSkills.map((skill) {
                    final selected = _selectedSkills.contains(skill);
                    return FilterChip(
                      label: Text(
                        skill,
                        style: TextStyle(
                          color: selected
                              ? Colors.white
                              : AppColors.textSecondary,
                          fontSize: 13,
                        ),
                      ),
                      selected: selected,
                      onSelected: (v) {
                        setState(() {
                          if (v) {
                            _selectedSkills.add(skill);
                          } else {
                            _selectedSkills.remove(skill);
                          }
                        });
                      },
                      selectedColor: const Color(0xFF42A5F5),
                      backgroundColor: AppColors.cardBackground,
                      checkmarkColor: Colors.white,
                      side: BorderSide(
                        color: selected
                            ? const Color(0xFF42A5F5)
                            : AppColors.cardBorder,
                      ),
                    );
                  }).toList(),
                ),
              ],

              const SizedBox(height: 28),

              MedirouteButton(
                label: _isLogin ? 'Log In' : 'Create Volunteer Account',
                icon: _isLogin ? Icons.login : Icons.volunteer_activism,
                isLoading: _isLoading,
                onPressed: _submit,
              ),

              const SizedBox(height: 16),

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
                              : 'Already registered? ',
                          style: const TextStyle(
                            color: AppColors.textSecondary,
                            fontSize: 14,
                          ),
                        ),
                        TextSpan(
                          text: _isLogin ? 'Sign Up' : 'Log In',
                          style: const TextStyle(
                            color: Color(0xFF42A5F5),
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
