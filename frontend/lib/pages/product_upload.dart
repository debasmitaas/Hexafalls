import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'dart:convert';
import 'preview_page.dart';

class ProductUploadPage extends StatefulWidget {
  const ProductUploadPage({super.key});

  @override
  State<ProductUploadPage> createState() => _ProductUploadPageState();
}

class _ProductUploadPageState extends State<ProductUploadPage> {
  final ImagePicker _picker = ImagePicker();
  final SpeechToText _speechToText = SpeechToText();
  final TextEditingController _productNameController = TextEditingController();
  final TextEditingController _priceController = TextEditingController();
  
  File? _selectedImage;
  bool _isListening = false;
  bool _speechEnabled = false;
  bool _isLoading = false;
  String _currentField = '';
  String _speechStatus = 'Tap microphone to start';
  
  // Language toggle
  bool _isBengali = false;
  
  // Translations
  final Map<String, Map<String, String>> _translations = {
    'en': {
      'appTitle': 'Craftsmen Marketplace',
      'productImage': 'Product Image',
      'selectImage': 'Select Image',
      'productName': 'Product Name',
      'productNameHint': 'Enter product name or use speech',
      'price': 'Price',
      'priceHint': 'Enter price or use speech',
      'post': 'Post to Instagram & Facebook',
      'posting': 'Posting...',
      'instructions': 'Instructions:',
      'step1': '1. Select a product image',
      'step2': '2. Enter product name (or use speech input)',
      'step3': '3. Enter price (or use speech input)',
      'step4': '4. Tap "Post to Instagram & Facebook"',
      'serverNote': 'Note: Make sure your backend server is running at localhost:8000',
      'debugInfo': 'Speech Debug Info:',
      'speechAvailable': 'Speech Available',
      'listening': 'Currently Listening',
      'status': 'Status',
      'testMic': 'Test Microphone Permission',
      'success': 'Success!',
      'productPosted': 'Product posted successfully!',
      'toggleLanguage': 'বাংলা',
    },
    'bn': {
      'appTitle': 'কারিগর মার্কেটপ্লেস',
      'productImage': 'পণ্যের ছবি',
      'selectImage': 'ছবি নির্বাচন করুন',
      'productName': 'পণ্যের নাম',
      'productNameHint': 'পণ্যের নাম লিখুন অথবা ভয়েস ব্যবহার করুন',
      'price': 'মূল্য/দাম',
      'priceHint': 'দাম লিখুন অথবা ভয়েস ব্যবহার করুন',
      'post': 'ইনস্টাগ্রাম এবং ফেসবুকে পোস্ট করুন',
      'posting': 'পোস্ট করা হচ্ছে...',
      'instructions': 'নির্দেশাবলী:',
      'step1': '১. একটি পণ্যের ছবি নির্বাচন করুন',
      'step2': '২. পণ্যের নাম লিখুন (অথবা ভয়েস ইনপুট ব্যবহার করুন)',
      'step3': '৩. দাম লিখুন (অথবা ভয়েস ইনপুট ব্যবহার করুন)',
      'step4': '৪. "ইনস্টাগ্রাম এবং ফেসবুকে পোস্ট করুন" বাটনে ক্লিক করুন',
      'serverNote': 'নোট: নিশ্চিত করুন যে আপনার ব্যাকএন্ড সার্ভার localhost:8000-এ চলছে',
      'debugInfo': 'স্পিচ ডিবাগ তথ্য:',
      'speechAvailable': 'স্পিচ উপলব্ধ',
      'listening': 'বর্তমানে শুনছে',
      'status': 'অবস্থা',
      'testMic': 'মাইক্রোফোন পা��মিশন পরীক্ষা করুন',
      'success': 'সফল!',
      'productPosted': 'পণ্য সফলভাবে পোস্ট করা হয়েছে!',
      'toggleLanguage': 'English',
    }
  };
  
  // Backend URL configurations
  // Use this to connect to your backend
  static const String backendUrl = 'http://192.168.133.28:8000'; // CHANGE THIS to your computer's IP address
  
  // You can use different URLs for different environments:
  // - Android Emulator: 'http://10.0.2.2:8000'
  // - iOS Simulator: 'http://localhost:8000'
  // - Physical Device: Use your computer's IP address, like '192.168.133.28:8000'

  @override
  void initState() {
    super.initState();
    _initSpeech();
  }

  void _initSpeech() async {
    try {
      _speechEnabled = await _speechToText.initialize(
        onError: (error) {
          debugPrint('Speech recognition error: $error');
          _showSnackBar('Speech recognition error: ${error.errorMsg}');
        },
        onStatus: (status) {
          debugPrint('Speech recognition status: $status');
        },
      );
      if (!_speechEnabled) {
        _showSnackBar('Speech recognition not available on this device');
      }
    } catch (e) {
      debugPrint('Failed to initialize speech recognition: $e');
      _showSnackBar('Failed to initialize speech recognition: $e');
      _speechEnabled = false;
    }
    setState(() {});
  }

  Future<void> _pickImage() async {
    try {
      final XFile? image = await _picker.pickImage(source: ImageSource.gallery);
      if (image != null) {
        setState(() {
          _selectedImage = File(image.path);
        });
      }
    } catch (e) {
      _showSnackBar('Error picking image: $e');
    }
  }

  void _startListening(String field) async {
    // Check if speech is available
    if (!_speechEnabled) {
      _showSnackBar('Speech recognition is not available. Please type manually.');
      return;
    }

    // Request microphone permission
    var status = await Permission.microphone.status;
    if (!status.isGranted) {
      status = await Permission.microphone.request();
    }
    
    if (!status.isGranted) {
      _showSnackBar('Microphone permission is required for speech input');
      return;
    }

    // Check if already listening
    if (_isListening) {
      _showSnackBar('Already listening...');
      return;
    }      try {
        setState(() {
          _isListening = true;
          _currentField = field;
          _speechStatus = 'Initializing...';
        });
      
      bool available = await _speechToText.initialize();
      if (!available) {
        setState(() {
          _isListening = false;
          _currentField = '';
          _speechStatus = 'Speech recognition not available';
        });
        _showSnackBar('Speech recognition not available');
        return;
      }

      setState(() {
        _speechStatus = 'Listening... Speak now!';
      });

      await _speechToText.listen(
        onResult: (result) {
          setState(() {
            if (field == 'name') {
              _productNameController.text = result.recognizedWords;
            } else if (field == 'price') {
              _priceController.text = result.recognizedWords;
            }
            _speechStatus = result.recognizedWords.isEmpty 
              ? 'Listening...' 
              : 'Recognized: ${result.recognizedWords}';
          });
        },
        listenFor: const Duration(seconds: 10),
        pauseFor: const Duration(seconds: 3),
        partialResults: true,
        cancelOnError: true,
        listenMode: ListenMode.confirmation,
      );
      
      // Auto-stop after listening period
      Future.delayed(const Duration(seconds: 10), () {
        if (_isListening) {
          _stopListening();
        }
      });
    } catch (e) {
      debugPrint('Error starting speech recognition: $e');
      _showSnackBar('Error starting speech recognition: $e');
      setState(() {
        _isListening = false;
        _currentField = '';
      });
    }
  }

  void _stopListening() async {
    try {
      if (_isListening) {
        await _speechToText.stop();
        setState(() {
          _isListening = false;
          _currentField = '';
          _speechStatus = 'Tap microphone to start';
        });
      }
    } catch (e) {
      debugPrint('Error stopping speech recognition: $e');
      setState(() {
        _isListening = false;
        _currentField = '';
        _speechStatus = 'Error occurred';
      });
    }
  }

  Future<void> _createAndPostProduct() async {
    if (_selectedImage == null) {
      _showSnackBar('Please select an image');
      return;
    }
    
    if (_productNameController.text.isEmpty) {
      _showSnackBar('Please enter a product name');
      return;
    }
    
    if (_priceController.text.isEmpty) {
      _showSnackBar('Please enter a price');
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$backendUrl/native_products/create-and-post-native'),
      );

      // Add the image file
      request.files.add(
        await http.MultipartFile.fromPath('file', _selectedImage!.path),
      );

      // Add other fields
      request.fields['product_name'] = _productNameController.text;
      request.fields['price'] = _priceController.text;

      var response = await request.send();
      var responseBody = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        var jsonResponse = json.decode(responseBody);
        _showSuccessDialog(jsonResponse);
        _resetForm();
      } else {
        _showSnackBar('Error: ${response.statusCode} - $responseBody');
      }
    } catch (e) {
      _showSnackBar('Network error: $e');
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _resetForm() {
    setState(() {
      _selectedImage = null;
      _productNameController.clear();
      _priceController.clear();
    });
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
          title: Text(_t('success')),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(_t('productPosted')),
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
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('OK'),
            ),
          ],
        );
      },
    );
  }

  // Helper method to get translation
  String _t(String key) {
    final lang = _isBengali ? 'bn' : 'en';
    return _translations[lang]?[key] ?? key;
  }

  @override
  Widget build(BuildContext context) {
    final Color mainPurple = const Color(0xFF6C4DD3);
    final Color lightPurple = const Color(0xFFB9A7F8);
    final Color darkPurple = const Color(0xFF4B2FAE);
    final Color bgPurple = const Color(0xFFEEE9FB);
    return Scaffold(
      backgroundColor: bgPurple,
      appBar: AppBar(
        backgroundColor: mainPurple,
        elevation: 0,
        title: Text(_t('appTitle'), style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
        actions: [
          TextButton(
            onPressed: () {
              setState(() {
                _isBengali = !_isBengali;
              });
            },
            child: Text(
              _t('toggleLanguage'),
              style: const TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 16,
                color: Colors.white,
              ),
            ),
          ),
        ],
      ),
      body: Stack(
        children: [
          Positioned(
            top: 0,
            left: 0,
            right: 0,
            child: Container(
              height: 120,
              decoration: BoxDecoration(
                color: mainPurple,
                borderRadius: const BorderRadius.only(
                  bottomLeft: Radius.circular(32),
                  bottomRight: Radius.circular(32),
                ),
              ),
            ),
          ),
          SingleChildScrollView(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Image Section
                Card(
                  elevation: 8,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
                  color: Colors.white,
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      children: [
                        Row(
                          children: [
                            Icon(Icons.image, color: mainPurple, size: 28),
                            const SizedBox(width: 8),
                            Text(
                              _t('productImage'),
                              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: mainPurple),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        AnimatedSwitcher(
                          duration: const Duration(milliseconds: 500),
                          child: _selectedImage != null
                              ? ClipRRect(
                                  borderRadius: BorderRadius.circular(16),
                                  child: Image.file(
                                    _selectedImage!,
                                    height: 180,
                                    width: double.infinity,
                                    fit: BoxFit.cover,
                                    key: ValueKey(_selectedImage!.path),
                                  ),
                                )
                              : Container(
                                  height: 180,
                                  width: double.infinity,
                                  decoration: BoxDecoration(
                                    border: Border.all(color: lightPurple, width: 2),
                                    borderRadius: BorderRadius.circular(16),
                                    color: bgPurple,
                                  ),
                                  child: const Icon(
                                    Icons.add_photo_alternate,
                                    size: 60,
                                    color: Color(0xFFB9A7F8),
                                  ),
                                ),
                        ),
                        const SizedBox(height: 16),
                        ElevatedButton.icon(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: mainPurple,
                            foregroundColor: Colors.white,
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                            elevation: 4,
                          ),
                          onPressed: _pickImage,
                          icon: const Icon(Icons.photo_camera),
                          label: Text(_t('selectImage'), style: const TextStyle(fontWeight: FontWeight.bold)),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 18),
                // Product Name Section
                Card(
                  elevation: 6,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                  color: Colors.white,
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(Icons.label, color: mainPurple, size: 24),
                            const SizedBox(width: 8),
                            Text(
                              _t('productName'),
                              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: mainPurple),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Row(
                          children: [
                            Expanded(
                              child: TextField(
                                controller: _productNameController,
                                decoration: InputDecoration(
                                  hintText: _t('productNameHint'),
                                  border: const OutlineInputBorder(),
                                ),
                              ),
                            ),
                            const SizedBox(width: 8),
                            AnimatedSwitcher(
                              duration: const Duration(milliseconds: 300),
                              child: IconButton(
                                key: ValueKey(_isListening && _currentField == 'name'),
                                onPressed: _speechEnabled 
                                  ? (_isListening && _currentField == 'name' ? _stopListening : () => _startListening('name'))
                                  : null,
                                icon: Icon(
                                  _isListening && _currentField == 'name' ? Icons.mic_off : Icons.mic,
                                  color: _isListening && _currentField == 'name' ? Colors.red : mainPurple,
                                ),
                              ),
                            ),
                          ],
                        ),
                        if (_isListening && _currentField == 'name')
                          Padding(
                            padding: const EdgeInsets.only(top: 8.0),
                            child: Text(
                              _speechStatus,
                              style: const TextStyle(color: Colors.red, fontSize: 12),
                            ),
                          ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 18),
                // Price Section
                Card(
                  elevation: 6,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                  color: Colors.white,
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(Icons.attach_money, color: mainPurple, size: 24),
                            const SizedBox(width: 8),
                            Text(
                              _t('price'),
                              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: mainPurple),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Row(
                          children: [
                            Expanded(
                              child: TextField(
                                controller: _priceController,
                                decoration: InputDecoration(
                                  hintText: _t('priceHint'),
                                  border: const OutlineInputBorder(),
                                ),
                                keyboardType: TextInputType.number,
                              ),
                            ),
                            const SizedBox(width: 8),
                            AnimatedSwitcher(
                              duration: const Duration(milliseconds: 300),
                              child: IconButton(
                                key: ValueKey(_isListening && _currentField == 'price'),
                                onPressed: _speechEnabled 
                                  ? (_isListening && _currentField == 'price' ? _stopListening : () => _startListening('price'))
                                  : null,
                                icon: Icon(
                                  _isListening && _currentField == 'price' ? Icons.mic_off : Icons.mic,
                                  color: _isListening && _currentField == 'price' ? Colors.red : mainPurple,
                                ),
                              ),
                            ),
                          ],
                        ),
                        if (_isListening && _currentField == 'price')
                          Padding(
                            padding: const EdgeInsets.only(top: 8.0),
                            child: Text(
                              _speechStatus,
                              style: const TextStyle(color: Colors.red, fontSize: 12),
                            ),
                          ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 28),
                // Generate & Preview Button
                AnimatedContainer(
                  duration: const Duration(milliseconds: 400),
                  curve: Curves.easeInOut,
                  child: SizedBox(
                    height: 50,
                    child: ElevatedButton.icon(
                      onPressed: _isLoading
                          ? null
                          : () {
                              // Validate required fields before preview
                              if (_selectedImage == null) {
                                _showSnackBar('Please select an image first');
                                return;
                              }
                              if (_productNameController.text.isEmpty) {
                                _showSnackBar('Please enter a product name');
                                return;
                              }
                              if (_priceController.text.isEmpty) {
                                _showSnackBar('Please enter a price');
                                return;
                              }
                              
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                    builder: (context) => PreviewPage(
                                      imagePath: _selectedImage!.path,
                                      productName: _productNameController.text,
                                      price: _priceController.text,
                                    )),
                              );
                            },
                      icon: const Icon(Icons.remove_red_eye),
                      label: const Text('Generate & Preview'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: darkPurple,
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                        elevation: 6,
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 18),
                // Submit Button
                AnimatedContainer(
                  duration: const Duration(milliseconds: 400),
                  curve: Curves.easeInOut,
                  child: SizedBox(
                    height: 50,
                    child: ElevatedButton.icon(
                      onPressed: _isLoading ? null : _createAndPostProduct,
                      icon: _isLoading 
                        ? const SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                          )
                        : const Icon(Icons.share),
                      label: Text(_isLoading ? _t('posting') : 'Post'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: mainPurple,
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                        elevation: 6,
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 18),
                // Instructions
                // Card(
                //   elevation: 2,
                //   shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                //   color: Colors.white,
                //   child: Padding(
                //     padding: const EdgeInsets.all(16.0),
                //     child: Column(
                //       crossAxisAlignment: CrossAxisAlignment.start,
                //       children: [
                //         Row(
                //           children: [
                //             Icon(Icons.info_outline, color: mainPurple),
                //             const SizedBox(width: 8),
                //             Text(
                //               _t('instructions'),
                //               style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: mainPurple),
                //             ),
                //           ],
                //         ),
                //         const SizedBox(height: 8),
                //         Text(_t('step1'), style: const TextStyle(fontSize: 14)),
                //         Text(_t('step2'), style: const TextStyle(fontSize: 14)),
                //         Text(_t('step3'), style: const TextStyle(fontSize: 14)),
                //         Text(_t('step4'), style: const TextStyle(fontSize: 14)),
                //         const SizedBox(height: 8),
                //         Text(
                //           _t('serverNote'),
                //           style: const TextStyle(fontStyle: FontStyle.italic, color: Colors.grey),
                //         ),
                //       ],
                //     ),
                //   ),
                // ),
                // const SizedBox(height: 10),
                // // Debug Info
                // Card(
                //   elevation: 1,
                //   shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                //   color: Colors.white,
                //   child: Padding(
                //     padding: const EdgeInsets.all(16.0),
                //     child: Column(
                //       crossAxisAlignment: CrossAxisAlignment.start,
                //       children: [
                //         Row(
                //           children: [
                //             Icon(Icons.bug_report, color: mainPurple),
                //             const SizedBox(width: 8),
                //             Text(
                //               _t('debugInfo'),
                //               style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: mainPurple),
                //             ),
                //           ],
                //         ),
                //         const SizedBox(height: 4),
                //         Text('${_t('speechAvailable')}: ${_speechEnabled ? "Yes" : "No"}', 
                //              style: const TextStyle(fontSize: 12)),
                //         Text('${_t('listening')}: ${_isListening ? "Yes" : "No"}', 
                //              style: const TextStyle(fontSize: 12)),
                //         Text('${_t('status')}: $_speechStatus', 
                //              style: const TextStyle(fontSize: 12)),
                //         const SizedBox(height: 8),
                //         ElevatedButton(
                //           style: ElevatedButton.styleFrom(
                //             backgroundColor: mainPurple,
                //             foregroundColor: Colors.white,
                //             shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                //           ),
                //           onPressed: () async {
                //             var status = await Permission.microphone.status;
                //             _showSnackBar('Microphone permission: \\${status.toString()}');
                //             if (!status.isGranted) {
                //               status = await Permission.microphone.request();
                //               _showSnackBar('After request: \\${status.toString()}');
                //             }
                //           },
                //           child: Text(_t('testMic'), style: const TextStyle(fontWeight: FontWeight.bold)),
                //         ),
                //       ],
                //     ),
                //   ),
                // ),
                const SizedBox(height: 24),
              ],
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _productNameController.dispose();
    _priceController.dispose();
    super.dispose();
  }
}
