import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../../core/theme/app_colors.dart';
import '../../core/constants/app_constants.dart';
import '../../data/models/user_model.dart';

/// Profile screen — shows user details, stats, and logout.
class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  UserModel? _user;
  int _emergencyCount = 0;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadProfile();
  }

  Future<void> _loadProfile() async {
    final uid = FirebaseAuth.instance.currentUser?.uid;
    if (uid == null) {
      if (mounted) context.go('/role-selection');
      return;
    }

    try {
      final doc = await FirebaseFirestore.instance
          .collection(AppConstants.usersCollection)
          .doc(uid)
          .get();

      if (doc.exists) {
        _user = UserModel.fromJson(doc.data()!);
      }

      // Count emergencies
      final emergencyQuery = await FirebaseFirestore.instance
          .collection(AppConstants.emergenciesCollection)
          .where(
            _user?.role == 'volunteer' ? 'volunteerAssigned' : 'bystanderUid',
            isEqualTo: uid,
          )
          .get();
      _emergencyCount = emergencyQuery.docs.length;
    } catch (_) {}

    if (mounted) setState(() => _isLoading = false);
  }

  Future<void> _logout() async {
    await FirebaseAuth.instance.signOut();
    if (mounted) context.go('/role-selection');
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Scaffold(
        backgroundColor: AppColors.background,
        body: Center(
          child: CircularProgressIndicator(color: AppColors.primaryRed),
        ),
      );
    }

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        title: const Text('Profile'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            if (_user?.role == 'volunteer') {
              context.go('/volunteer/dashboard');
            } else {
              context.go('/bystander/home');
            }
          },
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            children: [
              // Avatar + Name
              CircleAvatar(
                radius: 44,
                backgroundColor: AppColors.primaryRed.withValues(alpha: 0.2),
                child: Text(
                  (_user?.name ?? 'U').substring(0, 1).toUpperCase(),
                  style: const TextStyle(
                    color: AppColors.primaryRed,
                    fontSize: 36,
                    fontWeight: FontWeight.w800,
                  ),
                ),
              ),
              const SizedBox(height: 14),
              Text(
                _user?.name ?? 'User',
                style: const TextStyle(
                  color: AppColors.textPrimary,
                  fontSize: 24,
                  fontWeight: FontWeight.w800,
                ),
              ),
              const SizedBox(height: 4),
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 14,
                  vertical: 4,
                ),
                decoration: BoxDecoration(
                  color: _user?.role == 'volunteer'
                      ? const Color(0xFF42A5F5).withValues(alpha: 0.15)
                      : AppColors.primaryRed.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  (_user?.role ?? 'user').toUpperCase(),
                  style: TextStyle(
                    color: _user?.role == 'volunteer'
                        ? const Color(0xFF42A5F5)
                        : AppColors.primaryRed,
                    fontWeight: FontWeight.w700,
                    fontSize: 12,
                  ),
                ),
              ),

              const SizedBox(height: 28),

              // Stats row
              Container(
                padding: const EdgeInsets.all(18),
                decoration: BoxDecoration(
                  color: AppColors.cardBackground,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: AppColors.cardBorder),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    _StatItem(value: '$_emergencyCount', label: 'Emergencies'),
                    _StatItem(
                      value: _user?.role == 'volunteer'
                          ? '${_user?.skills.length ?? 0}'
                          : '--',
                      label: 'Skills',
                    ),
                    _StatItem(
                      value: _formatDate(_user?.createdAt),
                      label: 'Joined',
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 24),

              // Info tiles
              _InfoTile(
                icon: Icons.email,
                label: 'Email',
                value: _user?.email ?? '-',
              ),
              _InfoTile(
                icon: Icons.phone,
                label: 'Phone',
                value: _user?.phone.isNotEmpty == true
                    ? _user!.phone
                    : 'Not set',
              ),

              // Skills (volunteer only)
              if (_user?.role == 'volunteer' && _user!.skills.isNotEmpty) ...[
                const SizedBox(height: 20),
                Align(
                  alignment: Alignment.centerLeft,
                  child: const Text(
                    'Skills & Certifications',
                    style: TextStyle(
                      color: AppColors.textPrimary,
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
                const SizedBox(height: 10),
                Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: _user!.skills
                      .map(
                        (s) => Chip(
                          label: Text(
                            s,
                            style: const TextStyle(
                              color: AppColors.textPrimary,
                              fontSize: 12,
                            ),
                          ),
                          backgroundColor: AppColors.cardBackground,
                          side: BorderSide(color: AppColors.cardBorder),
                        ),
                      )
                      .toList(),
                ),
              ],

              const SizedBox(height: 32),

              // Logout
              SizedBox(
                width: double.infinity,
                height: 52,
                child: OutlinedButton.icon(
                  onPressed: _logout,
                  style: OutlinedButton.styleFrom(
                    side: const BorderSide(color: AppColors.primaryRed),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(14),
                    ),
                  ),
                  icon: const Icon(Icons.logout, color: AppColors.primaryRed),
                  label: const Text(
                    'Log Out',
                    style: TextStyle(
                      color: AppColors.primaryRed,
                      fontWeight: FontWeight.w700,
                      fontSize: 16,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  String _formatDate(DateTime? date) {
    if (date == null) return '--';
    final months = [
      '',
      'Jan',
      'Feb',
      'Mar',
      'Apr',
      'May',
      'Jun',
      'Jul',
      'Aug',
      'Sep',
      'Oct',
      'Nov',
      'Dec',
    ];
    return '${months[date.month]} ${date.year}';
  }
}

class _StatItem extends StatelessWidget {
  final String value;
  final String label;
  const _StatItem({required this.value, required this.label});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          value,
          style: const TextStyle(
            color: AppColors.textPrimary,
            fontSize: 22,
            fontWeight: FontWeight.w800,
          ),
        ),
        const SizedBox(height: 2),
        Text(
          label,
          style: const TextStyle(color: AppColors.textSubdued, fontSize: 11),
        ),
      ],
    );
  }
}

class _InfoTile extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  const _InfoTile({
    required this.icon,
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.cardBackground,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: AppColors.cardBorder),
      ),
      child: Row(
        children: [
          Icon(icon, color: AppColors.primaryRed, size: 20),
          const SizedBox(width: 14),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                label,
                style: const TextStyle(
                  color: AppColors.textSubdued,
                  fontSize: 11,
                ),
              ),
              Text(
                value,
                style: const TextStyle(
                  color: AppColors.textPrimary,
                  fontSize: 15,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
