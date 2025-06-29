import 'package:flutter/material.dart';
import 'product_upload.dart';

class IntroPage extends StatelessWidget {
  const IntroPage({super.key});

  @override
  Widget build(BuildContext context) {
    // Define warm earthy colors
    const Color terracotta = Color(0xFFE2725B);
    const Color mustard = Color(0xFFF6C244);
    const Color mutedBrown = Color(0xFF8D6748);
    const Color background = Color(0xFFFFF8F2);

    return Scaffold(
      backgroundColor: background,
      body: Stack(
        children: [
          // Subtle rural art pattern background (alpana/jute/terracotta texture)
          Positioned.fill(
            child: Opacity(
              opacity: 0.08,
              child: Image.asset(
                'assets/images/terracotta_pattern.png',
                fit: BoxFit.cover,
                // Add your own pattern image in assets/images/
              ),
            ),
          ),
          Center(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 32.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  // Left: Hero content
                  // Expanded(
                    // flex: 2,
                    // child: Column(
                      // mainAxisAlignment: MainAxisAlignment.center,
                      // crossAxisAlignment: CrossAxisAlignment.center,
                      // children: [
                        // Logo placeholder
                        Container(
                          width: 80,
                          height: 80,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: terracotta.withOpacity(0.15),
                            border: Border.all(color: terracotta, width: 2),
                          ),
                          child: Center(
                            child: Icon(Icons.record_voice_over, size: 48, color: terracotta),
                            // Replace with custom logo if available
                          ),
                        ),
                        const SizedBox(height: 24),
                        // App Name
                        Text(
                          'ShilpoSphere',
                          style: TextStyle(
                            fontSize: 40,
                            fontWeight: FontWeight.bold,
                            color: terracotta,
                            letterSpacing: 1.5,
                            fontFamily: 'Roboto', // Use a rounded font if available
                          ),
                        ),
                        const SizedBox(height: 12),
                        // Tagline
                        Text(
                          'Connecting rural hands to digital hearts.',
                          style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.w500,
                            color: mutedBrown,
                            fontFamily: 'Roboto',
                          ),
                        ),
                        const SizedBox(height: 18),
                        // Subheading
                        Text(
                          'A voice-powered platform helping rural artisans post and sell handmade art online with just one photo and one tap.',
                          style: TextStyle(
                            fontSize: 16,
                            color: Colors.brown,
                            fontFamily: 'Roboto',
                          ),
                        ),
                        const SizedBox(height: 32),
                        // CTA Button
                        SizedBox(
                          width: double.infinity,
                          child: ElevatedButton(
                            style: ElevatedButton.styleFrom(
                              backgroundColor: terracotta,
                              foregroundColor: Colors.white,
                              padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 20),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(30),
                              ),
                              textStyle: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
                            ),
                            onPressed: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(builder: (context) => const ProductUploadPage()),
                              );
                            },
                            child: const Text('Get Started'),
                          ),
                        ),
                      ],
                    ),
                  ),
                //   const SizedBox(width: 40),
                //   // Right: Phone mockup
                //   Expanded(
                //     flex: 2,
                //     child: Center(
                //       child: Container(
                //         width: 260,
                //         height: 520,
                //         decoration: BoxDecoration(
                //           color: Colors.white,
                //           borderRadius: BorderRadius.circular(40),
                //           boxShadow: [
                //             BoxShadow(
                //               color: Colors.black.withOpacity(0.08),
                //               blurRadius: 24,
                //               offset: const Offset(0, 8),
                //             ),
                //           ],
                //           border: Border.all(color: mustard, width: 3),
                //         ),
                //         child: Column(
                //           mainAxisAlignment: MainAxisAlignment.start,
                //           children: [
                //             // Phone notch
                //             Container(
                //               margin: const EdgeInsets.symmetric(vertical: 12),
                //               width: 60,
                //               height: 6,
                //               decoration: BoxDecoration(
                //                 color: Colors.grey[300],
                //                 borderRadius: BorderRadius.circular(3),
                //               ),
                //             ),
                //             // Terracotta craft image
                //             ClipRRect(
                //               borderRadius: BorderRadius.circular(24),
                //               child: Image.asset(
                //                 'assets/images/terracotta_craft.jpg',
                //                 width: 200,
                //                 height: 160,
                //                 fit: BoxFit.cover,
                //               ),
                //             ),
                //             const Spacer(),
                //             // Facebook logo (optional)
                //             Padding(
                //               padding: const EdgeInsets.only(bottom: 18.0),
                //               child: Icon(Icons.facebook, color: Colors.blue[800], size: 32),
                //             ),
                //           ],
                //         ),
                //       ),
                //     ),
                //   ),
                // ],
              ),
            // ),
          // ),
        ],
      ),
    );
  }
}
