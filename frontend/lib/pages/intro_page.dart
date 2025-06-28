import 'package:flutter/material.dart';
import 'product_upload.dart';

class IntroPage extends StatelessWidget {
  const IntroPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Intro")),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => const ProductUploadPage()),
            );
          },
          child: const Text('Start Selling'),
        ),
      ),
    );
  }
}
