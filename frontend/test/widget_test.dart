// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter_test/flutter_test.dart';

import 'package:frontend/main.dart';

void main() {
testWidgets('App starts with Intro page', (WidgetTester tester) async {
  await tester.pumpWidget(const MyApp()); // or CraftsmenMarketplaceApp if renamed

  // Check for Intro title and Start Selling button
  expect(find.text('Intro'), findsOneWidget);
  expect(find.text('Start Selling'), findsOneWidget);
});

}
