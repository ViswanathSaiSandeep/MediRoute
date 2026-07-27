import 'dart:ui';

/// MediRoute color palette — dark maroon theme with red emergency accents.
/// Derived from UI mockup screens.
class AppColors {
  AppColors._();

  // ── Primary backgrounds ──
  static const Color background = Color(0xFF1A0A0A);
  static const Color backgroundDark = Color(0xFF0D0505);
  static const Color backgroundLight = Color(0xFF2D1111);

  // ── Card & surface colors ──
  static const Color cardBackground = Color(0xFF2A1212);
  static const Color cardBackgroundLight = Color(0xFF3D1C1C);
  static const Color cardBorder = Color(0xFF5A2D2D);
  static const Color surfaceDark = Color(0xFF1E0E0E);

  // ── Red accent palette ──
  static const Color primaryRed = Color(0xFFE53935);
  static const Color accentRed = Color(0xFFFF1744);
  static const Color sosRed = Color(0xFFFF0000);
  static const Color emergencyRed = Color(0xFFD32F2F);
  static const Color redGlow = Color(0x40FF1744);

  // ── Green accent (for accept/available) ──
  static const Color acceptGreen = Color(0xFF4CAF50);
  static const Color availableGreen = Color(0xFF66BB6A);

  // ── Text colors ──
  static const Color textPrimary = Color(0xFFFFFFFF);
  static const Color textSecondary = Color(0xFFB0B0B0);
  static const Color textSubdued = Color(0xFF757575);
  static const Color textRed = Color(0xFFFF1744);

  // ── Misc ──
  static const Color divider = Color(0xFF3A1A1A);
  static const Color shimmerBase = Color(0xFF2A1212);
  static const Color shimmerHighlight = Color(0xFF3D1C1C);
  static const Color progressTrack = Color(0xFF3A1A1A);
  static const Color progressFill = Color(0xFFE53935);
}
