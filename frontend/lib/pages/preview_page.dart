import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class PreviewPage extends StatefulWidget {
  final String? imagePath;
  final String? productName;
  final String? price;
  final String? caption;

  const PreviewPage({Key? key, this.imagePath, this.productName, this.price, this.caption}) : super(key: key);

  @override
  State<PreviewPage> createState() => _PreviewPageState();
}

class _PreviewPageState extends State<PreviewPage> {
  String? generatedCaption;
  bool isGeneratingCaption = false;
  bool isPosting = false;
  
  // Backend URL - same as in product_upload.dart
  static const String backendUrl = 'http://192.168.133.28:8000';

  @override
  void initState() {
    super.initState();
    _generateCaption();
  }

  Future<void> _generateCaption() async {
    if (widget.productName == null || widget.price == null) return;
    
    setState(() {
      isGeneratingCaption = true;
    });

    try {
      final response = await http.post(
        Uri.parse('$backendUrl/ai/generate-caption'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'product_name': widget.productName,
          'price': double.tryParse(widget.price ?? '0') ?? 0.0,
        }),
      ).timeout(const Duration(seconds: 30)); // Increased timeout for AI generation

      print('AI Caption Response Status: ${response.statusCode}');
      print('AI Caption Response Body: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          // Only use fallback if the backend truly failed to provide a caption
          if (data['caption'] != null && data['caption'].toString().trim().isNotEmpty) {
            generatedCaption = data['caption'];
            print('✅ Generated caption: $generatedCaption');
          } else {
            // Show a clear error message instead of generic fallback
            generatedCaption = 'AI caption generation failed. Please try again or enter a custom caption.';
            print('❌ No caption in response: $data');
          }
        });
      } else {
        print('❌ AI Caption generation failed with status: ${response.statusCode}');
        setState(() {
          generatedCaption = 'Unable to generate AI caption (Status: ${response.statusCode}). Please check your connection and try again.';
        });
      }
    } catch (e) {
      print('❌ Error generating caption: $e');
      setState(() {
        // Show informative error message instead of generic fallback
        generatedCaption = 'Unable to generate AI caption. Please check your connection and try again. Error: $e';
      });
    } finally {
      setState(() {
        isGeneratingCaption = false;
      });
    }
  }

  Future<void> _postToSocialMedia() async {
    if (widget.imagePath == null || widget.productName == null || widget.price == null) {
      _showSnackBar('Missing required information');
      return;
    }

    setState(() {
      isPosting = true;
    });

    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$backendUrl/native_products/create-and-post-native'),
      );

      // Add the image file
      request.files.add(
        await http.MultipartFile.fromPath('file', widget.imagePath!),
      );

      request.fields['product_name'] = widget.productName!;
      request.fields['price'] = widget.price!;
      
      // Send the generated caption if available (this is key!)
      if (generatedCaption != null && generatedCaption!.trim().isNotEmpty) {
        request.fields['caption'] = generatedCaption!;
        print('📝 Sending caption to backend: $generatedCaption');
      }

      print('🚀 Posting to backend with:');
      print('- Product: ${widget.productName}');
      print('- Price: ${widget.price}');
      print('- Caption: ${generatedCaption ?? "None"}');
      print('- Image: ${widget.imagePath}');

      var response = await request.send();
      var responseBody = await response.stream.bytesToString();

      print('📊 Backend Response Status: ${response.statusCode}');
      print('📊 Backend Response Body: $responseBody');

      if (response.statusCode == 200) {
        var jsonResponse = json.decode(responseBody);
        _showSuccessDialog(jsonResponse);
      } else {
        _showSnackBar('Error: ${response.statusCode} - $responseBody');
      }
    } catch (e) {
      print('❌ Network error: $e');
      _showSnackBar('Network error: $e');
    } finally {
      setState(() {
        isPosting = false;
      });
    }
  }

  void _showSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }

  void _showSuccessDialog(Map<String, dynamic> response) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Success!'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Product posted successfully!'),
              const SizedBox(height: 10),
              if (response['facebook_post_id'] != null)
                Text('Facebook Post ID: ${response['facebook_post_id']}'),
              if (response['instagram_post_id'] != null)
                Text('Instagram Post ID: ${response['instagram_post_id']}'),
              if (response['ai_caption'] != null)
                Text('AI Caption: ${response['ai_caption']}'),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop(); // Close dialog
                Navigator.of(context).pop(); // Go back to upload page
              },
              child: const Text('OK'),
            ),
          ],
        );
      },
    );
  }

  void _editCaption() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        String editedCaption = generatedCaption ?? '';
        return AlertDialog(
          title: const Text('Edit Caption'),
          content: TextField(
            controller: TextEditingController(text: editedCaption),
            maxLines: 5,
            decoration: const InputDecoration(
              hintText: 'Enter your caption...',
              border: OutlineInputBorder(),
            ),
            onChanged: (value) {
              editedCaption = value;
            },
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Cancel'),
            ),
            TextButton(
              onPressed: () {
                setState(() {
                  generatedCaption = editedCaption;
                });
                Navigator.of(context).pop();
              },
              child: const Text('Save'),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    // Use warm earthy colors as in intro_page.dart
    const Color terracotta = Color(0xFFE2725B);
    const Color mustard = Color(0xFFF6C244);
    const Color mutedBrown = Color(0xFF8D6748);
    const Color background = Color(0xFFFFF8F2);
    
    return Scaffold(
      backgroundColor: background,
      appBar: AppBar(
        backgroundColor: terracotta,
        elevation: 0,
        title: const Text('Post Preview', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Facebook Post-like Card
            Card(
              elevation: 8,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              color: Colors.white,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Post Header (like Facebook)
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      children: [
                        CircleAvatar(
                          backgroundColor: terracotta,
                          radius: 20,
                          child: const Icon(Icons.store, color: Colors.white, size: 20),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text(
                                'ShilpoSphere',
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 16,
                                ),
                              ),
                              Text(
                                'Just now',
                                style: TextStyle(
                                  color: mutedBrown,
                                  fontSize: 12,
                                ),
                              ),
                            ],
                          ),
                        ),
                        Icon(Icons.more_horiz, color: mutedBrown),
                      ],
                    ),
                  ),
                  
                  // Post Caption/Text
                  if (generatedCaption != null || isGeneratingCaption)
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 16.0),
                      child: isGeneratingCaption
                          ? Row(
                              children: [
                                SizedBox(
                                  width: 16,
                                  height: 16,
                                  child: CircularProgressIndicator(
                                    strokeWidth: 2,
                                    color: terracotta,
                                  ),
                                ),
                                const SizedBox(width: 8),
                                const Text('Generating caption...'),
                              ],
                            )
                          : Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    Expanded(
                                      child: Text(
                                        generatedCaption!,
                                        style: const TextStyle(
                                          fontSize: 15,
                                          height: 1.4,
                                        ),
                                      ),
                                    ),
                                    IconButton(
                                      icon: Icon(Icons.edit, size: 20, color: terracotta),
                                      onPressed: () => _editCaption(),
                                      tooltip: 'Edit caption',
                                    ),
                                  ],
                                ),
                              ],
                            ),
                    ),
                  
                  const SizedBox(height: 12),
                  
                  // Post Image
                  if (widget.imagePath != null)
                    ClipRRect(
                      borderRadius: const BorderRadius.only(
                        bottomLeft: Radius.circular(16),
                        bottomRight: Radius.circular(16),
                      ),
                      child: Image.file(
                        File(widget.imagePath!),
                        width: double.infinity,
                        height: 300,
                        fit: BoxFit.cover,
                      ),
                    ),
                  
                  // Product Info Overlay (like Facebook marketplace posts)
                  if (widget.productName != null || widget.price != null)
                    Container(
                      width: double.infinity,
                      decoration: BoxDecoration(
                        color: mustard.withOpacity(0.10),
                        border: Border(
                          top: BorderSide(color: terracotta.withOpacity(0.2)),
                        ),
                      ),
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          if (widget.productName != null)
                            Text(
                              widget.productName!,
                              style: TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                                color: mutedBrown,
                              ),
                            ),
                          const SizedBox(height: 4),
                          if (widget.price != null)
                            Text(
                              '₹ ${widget.price}',
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                                color: terracotta,
                              ),
                            ),
                        ],
                      ),
                    ),
                  
                  // Engagement Bar (like Facebook)
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 12.0),
                    decoration: BoxDecoration(
                      border: Border(
                        top: BorderSide(color: terracotta.withOpacity(0.15)),
                      ),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        _buildEngagementButton(Icons.thumb_up, 'Like', terracotta),
                        _buildEngagementButton(Icons.comment, 'Comment', mutedBrown),
                        _buildEngagementButton(Icons.share, 'Share', mutedBrown),
                        _buildEngagementButton(Icons.message, 'Message', mustard),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            
            const SizedBox(height: 24),
            
            // Action Buttons
            Row(
              children: [
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: () => Navigator.pop(context),
                    icon: const Icon(Icons.edit),
                    label: const Text('Edit Post'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: mutedBrown,
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      padding: const EdgeInsets.symmetric(vertical: 14),
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: isPosting ? null : _postToSocialMedia,
                    icon: isPosting 
                        ? SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(
                              strokeWidth: 2,
                              color: Colors.white,
                            ),
                          )
                        : const Icon(Icons.publish),
                    label: Text(isPosting ? 'Posting...' : 'Post Now'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: terracotta,
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      padding: const EdgeInsets.symmetric(vertical: 14),
                    ),
                  ),
                ),
              ],
            ),
            
            const SizedBox(height: 16),
            
            // Preview Note
            Card(
              elevation: 2,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              color: mustard.withOpacity(0.15),
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Row(
                  children: [
                    Icon(Icons.info_outline, color: terracotta, size: 20),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        'This is how your post will appear on Facebook and Instagram',
                        style: TextStyle(
                          color: terracotta,
                          fontSize: 13,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEngagementButton(IconData icon, String label, Color color) {
    return InkWell(
      onTap: () {}, // Just for preview, no actual functionality
      borderRadius: BorderRadius.circular(8),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 6.0),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 18, color: color),
            const SizedBox(width: 4),
            Text(
              label,
              style: TextStyle(
                color: color,
                fontSize: 13,
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ),
      ),
    );
  }
}