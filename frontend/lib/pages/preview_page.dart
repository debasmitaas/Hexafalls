import 'dart:io';

import 'package:flutter/material.dart';

class PreviewPage extends StatelessWidget {
  final String? imagePath;
  final String? productName;
  final String? price;
  final String? caption;

  const PreviewPage({Key? key, this.imagePath, this.productName, this.price, this.caption}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final Color mainPurple = const Color(0xFF6C4DD3);
    final Color lightPurple = const Color(0xFFB9A7F8);
    final Color bgPurple = const Color(0xFFEEE9FB);
    return Scaffold(
      backgroundColor: bgPurple,
      appBar: AppBar(
        backgroundColor: mainPurple,
        elevation: 0,
        title: const Text('Preview', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Image Preview
              if (imagePath != null)
                Card(
                  elevation: 8,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
                  color: Colors.white,
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(16),
                      child: Image.file(
                        File(imagePath!),
                        height: 200,
                        width: double.infinity,
                        fit: BoxFit.cover,
                      ),
                    ),
                  ),
                ),
              const SizedBox(height: 24),
              // Product Name
              if (productName != null && productName!.isNotEmpty)
                Card(
                  elevation: 4,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                  color: Colors.white,
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      children: [
                        Icon(Icons.label, color: mainPurple, size: 24),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            productName!,
                            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: mainPurple),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              const SizedBox(height: 16),
              // Price
              if (price != null && price!.isNotEmpty)
                Card(
                  elevation: 4,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                  color: Colors.white,
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      children: [
                        Icon(Icons.attach_money, color: mainPurple, size: 24),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            price!,
                            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: mainPurple),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              const SizedBox(height: 16),
              // Caption
              if (caption != null && caption!.isNotEmpty)
                Card(
                  elevation: 2,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                  color: Colors.white,
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Icon(Icons.textsms, color: mainPurple, size: 22),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            caption!,
                            style: const TextStyle(fontSize: 16, color: Colors.black87),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              const SizedBox(height: 32),
              // Post Button
              SizedBox(
                height: 50,
                child: ElevatedButton.icon(
                  onPressed: () {
                    // TODO: Add post logic here
                  },
                  icon: const Icon(Icons.share),
                  label: const Text('Post to Instagram & Facebook'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: mainPurple,
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                    elevation: 6,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
