import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../../core/theme/app_colors.dart';
import '../../core/constants/app_constants.dart';

/// Emergency history screen — shows real data from Firestore.
class EmergencyHistoryScreen extends StatefulWidget {
  const EmergencyHistoryScreen({super.key});

  @override
  State<EmergencyHistoryScreen> createState() => _EmergencyHistoryScreenState();
}

class _EmergencyHistoryScreenState extends State<EmergencyHistoryScreen> {
  List<Map<String, dynamic>> _emergencies = [];
  bool _isLoading = true;
  int _resolvedCount = 0;
  String _userRole = 'bystander';

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    final uid = FirebaseAuth.instance.currentUser?.uid;
    if (uid == null) {
      setState(() => _isLoading = false);
      return;
    }

    try {
      // Check user role
      final userDoc = await FirebaseFirestore.instance
          .collection(AppConstants.usersCollection)
          .doc(uid)
          .get();
      final role = userDoc.data()?['role'] as String? ?? 'bystander';

      // Query emergencies for this user
      final query = FirebaseFirestore.instance
          .collection(AppConstants.emergenciesCollection)
          .where(
            role == 'volunteer' ? 'volunteerAssigned' : 'bystanderUid',
            isEqualTo: uid,
          )
          .orderBy('timestamp', descending: true)
          .limit(20);

      final snapshot = await query.get();
      final emergencies = snapshot.docs.map((doc) => doc.data()).toList();
      final resolved = emergencies
          .where((e) => e['status'] == 'resolved')
          .length;

      if (mounted) {
        setState(() {
          _userRole = role;
          _emergencies = emergencies;
          _resolvedCount = resolved;
          _isLoading = false;
        });
      }
    } catch (_) {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        title: const Text('Emergency History'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            if (_userRole == 'volunteer') {
              context.go('/volunteer/dashboard');
            } else {
              context.go('/bystander/home');
            }
          },
        ),
      ),
      body: SafeArea(
        child: _isLoading
            ? const Center(
                child: CircularProgressIndicator(color: AppColors.primaryRed),
              )
            : Column(
                children: [
                  // Summary Card
                  Padding(
                    padding: const EdgeInsets.all(16),
                    child: Container(
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                          colors: [Color(0xFF3D1C1C), Color(0xFF2D1111)],
                        ),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(
                          color: AppColors.cardBorder,
                          width: 0.5,
                        ),
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        children: [
                          _StatItem(
                            value: '${_emergencies.length}',
                            label: 'Total',
                          ),
                          _StatItem(
                            value: '$_resolvedCount',
                            label: 'Resolved',
                          ),
                          _StatItem(
                            value: '${_emergencies.length - _resolvedCount}',
                            label: 'Other',
                          ),
                        ],
                      ),
                    ),
                  ),

                  // List
                  Expanded(
                    child: _emergencies.isEmpty
                        ? Center(
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Icon(
                                  Icons.history,
                                  color: AppColors.textSubdued,
                                  size: 48,
                                ),
                                const SizedBox(height: 12),
                                const Text(
                                  'No emergency history yet',
                                  style: TextStyle(
                                    color: AppColors.textSecondary,
                                    fontSize: 15,
                                  ),
                                ),
                              ],
                            ),
                          )
                        : ListView.builder(
                            padding: const EdgeInsets.symmetric(horizontal: 16),
                            itemCount: _emergencies.length,
                            itemBuilder: (context, i) {
                              final e = _emergencies[i];
                              final status =
                                  e['status'] as String? ?? 'unknown';
                              final type = e['type'] as String? ?? 'Other';
                              final ts = e['timestamp'] as Timestamp?;
                              final date = ts?.toDate();

                              return Container(
                                margin: const EdgeInsets.only(bottom: 12),
                                padding: const EdgeInsets.all(16),
                                decoration: BoxDecoration(
                                  color: AppColors.cardBackground,
                                  borderRadius: BorderRadius.circular(14),
                                  border: Border.all(
                                    color: AppColors.cardBorder,
                                    width: 0.5,
                                  ),
                                ),
                                child: Row(
                                  children: [
                                    Container(
                                      width: 44,
                                      height: 44,
                                      decoration: BoxDecoration(
                                        color: AppColors.primaryRed.withValues(
                                          alpha: 0.15,
                                        ),
                                        borderRadius: BorderRadius.circular(12),
                                      ),
                                      child: const Icon(
                                        Icons.emergency,
                                        color: AppColors.primaryRed,
                                        size: 22,
                                      ),
                                    ),
                                    const SizedBox(width: 14),
                                    Expanded(
                                      child: Column(
                                        crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                        children: [
                                          Text(
                                            type,
                                            style: const TextStyle(
                                              color: AppColors.textPrimary,
                                              fontSize: 15,
                                              fontWeight: FontWeight.w600,
                                            ),
                                          ),
                                          const SizedBox(height: 3),
                                          Text(
                                            date != null
                                                ? '${date.day}/${date.month}/${date.year} • ${date.hour}:${date.minute.toString().padLeft(2, '0')}'
                                                : 'Unknown date',
                                            style: const TextStyle(
                                              color: AppColors.textSubdued,
                                              fontSize: 12,
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                    Container(
                                      padding: const EdgeInsets.symmetric(
                                        horizontal: 10,
                                        vertical: 4,
                                      ),
                                      decoration: BoxDecoration(
                                        color: _statusColor(
                                          status,
                                        ).withValues(alpha: 0.15),
                                        borderRadius: BorderRadius.circular(12),
                                      ),
                                      child: Text(
                                        status.toUpperCase(),
                                        style: TextStyle(
                                          color: _statusColor(status),
                                          fontSize: 10,
                                          fontWeight: FontWeight.w700,
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              );
                            },
                          ),
                  ),
                ],
              ),
      ),
    );
  }

  Color _statusColor(String status) {
    switch (status) {
      case 'resolved':
        return AppColors.acceptGreen;
      case 'active':
        return AppColors.primaryRed;
      case 'assigned':
        return const Color(0xFF42A5F5);
      case 'cancelled':
        return AppColors.textSubdued;
      default:
        return AppColors.textSubdued;
    }
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
            fontSize: 28,
            fontWeight: FontWeight.w800,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          textAlign: TextAlign.center,
          style: const TextStyle(color: AppColors.textSubdued, fontSize: 11),
        ),
      ],
    );
  }
}
