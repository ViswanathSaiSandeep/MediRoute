import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../../core/theme/app_colors.dart';
import '../../core/widgets/mediroute_button.dart';
import '../../core/widgets/mediroute_text_field.dart';
import '../../core/constants/app_constants.dart';
import '../../data/models/hospital_model.dart';
import '../../data/models/user_model.dart';
import '../../services/notification_service.dart';
import '../../services/location_service.dart';

/// Hospital registration and login onboarding flow.
class HospitalRegistrationScreen extends StatefulWidget {
  const HospitalRegistrationScreen({super.key});

  @override
  State<HospitalRegistrationScreen> createState() =>
      _HospitalRegistrationScreenState();
}

class _HospitalRegistrationScreenState
    extends State<HospitalRegistrationScreen> {
  final _nameController = TextEditingController();
  final _phoneController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _addressController = TextEditingController();
  final _proofNumberController = TextEditingController();

  String _selectedProofType = 'Certificate of Registration';
  final List<String> _selectedEmergencyTypes = [];
  double? _latitude;
  double? _longitude;
  bool _isFetchingLocation = false;

  bool _isLogin = false;
  bool _isLoading = false;
  String? _errorMessage;

  final List<String> _proofTypes = [
    'Certificate of Registration',
    'Medical Practice License',
    'Government Hospital Permit',
    'Official Accreditation ID',
  ];

  @override
  void dispose() {
    _nameController.dispose();
    _phoneController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _addressController.dispose();
    _proofNumberController.dispose();
    super.dispose();
  }

  Future<void> _getCurrentLocation() async {
    setState(() {
      _isFetchingLocation = true;
      _errorMessage = null;
    });

    try {
      final locationService = LocationService();
      final hasPermission = await locationService.requestPermission();
      if (hasPermission) {
        final pos = await locationService.getCurrentPosition();
        setState(() {
          _latitude = pos.latitude;
          _longitude = pos.longitude;
        });
      } else {
        setState(() {
          _errorMessage = 'Location permissions were denied.';
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'Failed to retrieve GPS location.';
      });
    } finally {
      setState(() => _isFetchingLocation = false);
    }
  }

  Future<void> _submit() async {
    final email = _emailController.text.trim();
    final password = _passwordController.text.trim();

    if (email.isEmpty || password.isEmpty) {
      setState(() => _errorMessage = 'Email and password are required.');
      return;
    }

    if (!_isLogin) {
      if (_nameController.text.trim().isEmpty) {
        setState(() => _errorMessage = 'Hospital name is required.');
        return;
      }
      if (_phoneController.text.trim().isEmpty) {
        setState(() => _errorMessage = 'Contact phone number is required.');
        return;
      }
      if (_addressController.text.trim().isEmpty) {
        setState(() => _errorMessage = 'Hospital address is required.');
        return;
      }
      if (_proofNumberController.text.trim().isEmpty) {
        setState(() => _errorMessage = 'Accreditation/Proof number is required.');
        return;
      }
      if (_latitude == null || _longitude == null) {
        setState(() => _errorMessage = 'Hospital coordinates must be acquired via GPS.');
        return;
      }
      if (_selectedEmergencyTypes.isEmpty) {
        setState(() => _errorMessage = 'Please select at least one handled emergency type.');
        return;
      }
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
        
        // 1. Save general user document for authentication role routing
        final user = UserModel(
          uid: credential.user!.uid,
          role: 'hospital',
          name: _nameController.text.trim(),
          email: email,
          phone: _phoneController.text.trim(),
          createdAt: DateTime.now(),
          fcmToken: fcmToken,
        );

        await FirebaseFirestore.instance
            .collection(AppConstants.usersCollection)
            .doc(credential.user!.uid)
            .set(user.toJson());

        // 2. Save hospital details document for location tracking and alerts
        final hospital = HospitalModel(
          hospitalId: credential.user!.uid,
          name: _nameController.text.trim(),
          latitude: _latitude!,
          longitude: _longitude!,
          phone: _phoneController.text.trim(),
          address: _addressController.text.trim(),
          emergencyTypes: _selectedEmergencyTypes,
          proofType: _selectedProofType,
          proofNumber: _proofNumberController.text.trim(),
          active: true,
        );

        await FirebaseFirestore.instance
            .collection(AppConstants.hospitalsCollection)
            .doc(credential.user!.uid)
            .set(hospital.toJson());
      }

      if (mounted) context.go('/hospital/dashboard');
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
        title: const Text('Hospital Partner'),
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
                      Icons.local_hospital,
                      color: AppColors.primaryRed,
                      size: 28,
                    ),
                  ),
                  const SizedBox(width: 14),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          _isLogin ? 'Hospital Sign In' : 'Register Hospital',
                          style: const TextStyle(
                            color: AppColors.textPrimary,
                            fontSize: 22,
                            fontWeight: FontWeight.w800,
                          ),
                        ),
                        Text(
                          _isLogin
                              ? 'Log in to coordinate emergency intake'
                              : 'Add your medical facility to MediRoute',
                          style: const TextStyle(
                            color: AppColors.textSecondary,
                            fontSize: 13,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 24),

              // Error display
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

              // Form fields
              if (!_isLogin) ...[
                MedirouteTextField(
                  label: 'Hospital Name',
                  hint: 'Enter official hospital name',
                  prefixIcon: Icons.business,
                  controller: _nameController,
                ),
                const SizedBox(height: 16),
                MedirouteTextField(
                  label: 'Contact Phone Number',
                  hint: '+91 XXXXX XXXXX',
                  prefixIcon: Icons.phone,
                  controller: _phoneController,
                  keyboardType: TextInputType.phone,
                ),
                const SizedBox(height: 16),
                MedirouteTextField(
                  label: 'Full Physical Address',
                  hint: 'Enter hospital address details',
                  prefixIcon: Icons.location_on,
                  controller: _addressController,
                ),
                const SizedBox(height: 20),

                // Accreditation / Verification info
                const Text(
                  'Accreditation & Proof Verification',
                  style: TextStyle(
                    color: AppColors.textPrimary,
                    fontSize: 15,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 10),

                // Dropdown for Proof Type
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12),
                  decoration: BoxDecoration(
                    color: AppColors.cardBackground,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: AppColors.cardBorder),
                  ),
                  child: DropdownButtonHideUnderline(
                    child: DropdownButton<String>(
                      value: _selectedProofType,
                      isExpanded: true,
                      dropdownColor: AppColors.cardBackground,
                      style: const TextStyle(color: AppColors.textPrimary, fontSize: 15),
                      items: _proofTypes.map((type) {
                        return DropdownMenuItem<String>(
                          value: type,
                          child: Text(type),
                        );
                      }).toList(),
                      onChanged: (val) {
                        if (val != null) {
                          setState(() => _selectedProofType = val);
                        }
                      },
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                MedirouteTextField(
                  label: 'Certificate / Accreditation ID Number',
                  hint: 'Enter identification number',
                  prefixIcon: Icons.verified,
                  controller: _proofNumberController,
                ),
                const SizedBox(height: 20),

                // Location GPS coordinate picker
                const Text(
                  'Hospital Coordinates (GPS)',
                  style: TextStyle(
                    color: AppColors.textPrimary,
                    fontSize: 15,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 8),
                Container(
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: AppColors.cardBackground,
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: AppColors.cardBorder),
                  ),
                  child: Row(
                    children: [
                      Icon(
                        Icons.my_location,
                        color: (_latitude != null && _longitude != null)
                            ? Colors.green
                            : AppColors.textSubdued,
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              (_latitude != null && _longitude != null)
                                  ? 'Coordinates Acquired'
                                  : 'Coordinates Required',
                              style: TextStyle(
                                color: (_latitude != null && _longitude != null)
                                    ? Colors.green
                                    : AppColors.textPrimary,
                                fontWeight: FontWeight.w600,
                                fontSize: 13,
                              ),
                            ),
                            Text(
                              (_latitude != null && _longitude != null)
                                  ? 'Lat: ${_latitude!.toStringAsFixed(5)}, Lng: ${_longitude!.toStringAsFixed(5)}'
                                  : 'Click button to fetch facility GPS',
                              style: const TextStyle(
                                color: AppColors.textSecondary,
                                fontSize: 12,
                              ),
                            ),
                          ],
                        ),
                      ),
                      ElevatedButton(
                        onPressed: _isFetchingLocation ? null : _getCurrentLocation,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.primaryRed,
                          foregroundColor: Colors.white,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                        ),
                        child: _isFetchingLocation
                            ? const SizedBox(
                                width: 16,
                                height: 16,
                                child: CircularProgressIndicator(
                                  color: Colors.white,
                                  strokeWidth: 2,
                                ),
                              )
                            : const Text('Fetch GPS'),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 20),

                // Emergency Types Handled
                const Text(
                  'Emergency Types Handled',
                  style: TextStyle(
                    color: AppColors.textPrimary,
                    fontSize: 15,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 10),
                Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: AppConstants.emergencyTypes.map((type) {
                    final selected = _selectedEmergencyTypes.contains(type);
                    return FilterChip(
                      label: Text(
                        type,
                        style: TextStyle(
                          color: selected ? Colors.white : AppColors.textSecondary,
                          fontSize: 13,
                        ),
                      ),
                      selected: selected,
                      onSelected: (val) {
                        setState(() {
                          if (val) {
                            _selectedEmergencyTypes.add(type);
                          } else {
                            _selectedEmergencyTypes.remove(type);
                          }
                        });
                      },
                      selectedColor: AppColors.primaryRed,
                      backgroundColor: AppColors.cardBackground,
                      checkmarkColor: Colors.white,
                      side: BorderSide(
                        color: selected ? AppColors.primaryRed : AppColors.cardBorder,
                      ),
                    );
                  }).toList(),
                ),
                const SizedBox(height: 24),
              ],

              MedirouteTextField(
                label: 'Email Address',
                hint: 'you@hospital.com',
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

              const SizedBox(height: 28),

              MedirouteButton(
                label: _isLogin ? 'Log In' : 'Register Facility',
                icon: _isLogin ? Icons.login : Icons.local_hospital,
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
