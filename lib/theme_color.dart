import 'package:flutter/material.dart';

enum ThemeColor {
  orange('暖橙', 0xFFFF664F),
  rose('玫红', 0xFFC25485),
  amber('琥珀', 0xFFB37000),
  teal('青绿', 0xFF009C84),
  blue('海蓝', 0xFF0089D0),
  violet('蓝紫', 0xFF7970D5),
  purple('紫', 0xFF6F42C1);

  const ThemeColor(this.label, this.seed);
  final String label;
  final int seed;

  static ThemeColor? byName(Object? name) =>
      values.where((color) => color.name == name).firstOrNull;

  /// 紫色使用指定色值组成的固定色板：种子色推导无法精确落到这些颜色。
  /// 其它预设返回 null，继续由 `ColorScheme.fromSeed` 生成。
  ColorScheme? schemeFor(Brightness brightness) {
    if (this != purple) return null;
    final dark = brightness == Brightness.dark;
    return ColorScheme.fromSeed(
      seedColor: const Color(0xFF6F42C1),
      brightness: brightness,
    ).copyWith(
      primary: Color(dark ? 0xFFB99CF6 : 0xFF6F42C1),
      onPrimary: Color(dark ? 0xFF241546 : 0xFFFFFFFF),
      primaryContainer: Color(dark ? 0xFF4D3E85 : 0xFFE9DCFB),
      onPrimaryContainer: Color(dark ? 0xFFE9DCFB : 0xFF2B1B4D),
      tertiary: Color(dark ? 0xFFCDBFFF : 0xFF5A4DB8),
      onTertiary: Color(dark ? 0xFF2A2148 : 0xFFFFFFFF),
      tertiaryContainer: Color(dark ? 0xFF423674 : 0xFFE4DEFF),
      onTertiaryContainer: Color(dark ? 0xFFE4DEFF : 0xFF1B1240),
      surface: Color(dark ? 0xFF111019 : 0xFFFAF8FC),
      onSurface: Color(dark ? 0xFFE8E5F0 : 0xFF211F2E),
      onSurfaceVariant: Color(dark ? 0xFFC9C3D9 : 0xFF625E70),
      surfaceContainerLowest: Color(dark ? 0xFF0B0A12 : 0xFFFFFFFF),
      surfaceContainerLow: Color(dark ? 0xFF181622 : 0xFFF5F1F9),
      surfaceContainer: Color(dark ? 0xFF1D1B26 : 0xFFEFEAF5),
      surfaceContainerHigh: Color(dark ? 0xFF272433 : 0xFFE9E3F0),
      surfaceContainerHighest: Color(dark ? 0xFF322E40 : 0xFFE3DCEB),
      outline: Color(dark ? 0xFF928CA3 : 0xFF9C96A8),
      outlineVariant: Color(dark ? 0xFF48425A : 0xFFD6CFE0),
      inverseSurface: Color(dark ? 0xFFE8E5F0 : 0xFF322F3B),
      onInverseSurface: Color(dark ? 0xFF211F2E : 0xFFF4EFF7),
      inversePrimary: Color(dark ? 0xFF6F42C1 : 0xFFCFBBFF),
    );
  }
}
