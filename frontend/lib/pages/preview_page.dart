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
              // Facebook Post Preview Card
              Card(
                elevation: 10,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
                color: Colors.white,
                child: Padding(
                  padding: const EdgeInsets.all(18.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Header (Profile + Name)
                      Row(
                        children: [
                          CircleAvatar(
                            backgroundColor: mainPurple.withOpacity(0.2),
                            child: const Icon(Icons.person, color: Colors.white),
                          ),
                          const SizedBox(width: 10),
                          Text(
                            'You',
                            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: mainPurple),
                          ),
                          const SizedBox(width: 8),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                            decoration: BoxDecoration(
                              color: mainPurple.withOpacity(0.1),
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: const Text('Facebook', style: TextStyle(fontSize: 12, color: Colors.black54)),
                          ),
                        ],
                      ),
                      const SizedBox(height: 16),
                      // Caption
                      if (caption != null && caption!.isNotEmpty)
                        Text(
                          caption!,
                          style: const TextStyle(fontSize: 16, color: Colors.black87),
                        ),
                      if (caption != null && caption!.isNotEmpty)
                        const SizedBox(height: 10),
                      // Image
                      if (imagePath != null)
                        ClipRRect(
                          borderRadius: BorderRadius.circular(16),
                          child: Image.file(
                            File(imagePath!),
                            height: 220,
                            width: double.infinity,
                            fit: BoxFit.cover,
                          ),
                        ),
                      if (imagePath != null) const SizedBox(height: 10),
                      // Product Name & Price
                      if ((productName != null && productName!.isNotEmpty) || (price != null && price!.isNotEmpty))
                        Row(
                          children: [
                            if (productName != null && productName!.isNotEmpty)
                              Flexible(
                                child: Text(
                                  productName!,
                                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: mainPurple),
                                ),
                              ),
                            if (productName != null && productName!.isNotEmpty && price != null && price!.isNotEmpty)
                              const SizedBox(width: 12),
                            if (price != null && price!.isNotEmpty)
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                decoration: BoxDecoration(
                                  color: mainPurple.withOpacity(0.08),
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: Text(
                                  '৳ $price',
                                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: mainPurple),
                                ),
                              ),
                          ],
                        ),
                      const SizedBox(height: 10),
                      // Like, Comment, Share Row (for FB look)
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        children: [
                          Row(
                            children: [
                              Icon(Icons.thumb_up_alt_outlined, color: Colors.grey.shade400, size: 20),
                              const SizedBox(width: 4),
                              const Text('Like', style: TextStyle(color: Colors.black54)),
                            ],
                          ),
                          Row(
                            children: [
                              Icon(Icons.comment_outlined, color: Colors.grey.shade400, size: 20),
                              const SizedBox(width: 4),
                              const Text('Comment', style: TextStyle(color: Colors.black54)),
                            ],
                          ),
                          Row(
                            children: [
                              Icon(Icons.share_outlined, color: Colors.grey.shade400, size: 20),
                              const SizedBox(width: 4),
                              const Text('Share', style: TextStyle(color: Colors.black54)),
                            ],
                          ),
                        ],
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
