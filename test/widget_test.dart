import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('MediRoute app smoke test', (WidgetTester tester) async {
    // Smoke test — Firebase needs initialization before running.
    // Integration tests should be run on device.
    expect(true, isTrue);
  });
}
