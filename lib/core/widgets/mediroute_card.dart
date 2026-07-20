import 'package:flutter/material.dart';
import '../theme/app_colors.dart';

/// Dark-themed card container matching the MediRoute UI — rounded corners, subtle border.
class MedirouteCard extends StatelessWidget {
  final Widget child;
  final EdgeInsetsGeometry? padding;
  final Color? color;
  final VoidCallback? onTap;
  final double borderRadius;

  const MedirouteCard({
    super.key,
    required this.child,
    this.padding,
    this.color,
    this.onTap,
    this.borderRadius = 16,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: padding ?? const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: color ?? AppColors.cardBackground,
          borderRadius: BorderRadius.circular(borderRadius),
          border: Border.all(color: AppColors.cardBorder, width: 0.5),
        ),
        child: child,
      ),
    );
  }
}
