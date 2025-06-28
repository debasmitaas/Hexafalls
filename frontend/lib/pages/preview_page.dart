import 'package:flutter/material.dart';

class PreviewPage extends StatelessWidget {
  const PreviewPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Preview'),
      ),
      body: Center(
        child: ElevatedButton.icon(
          onPressed: () {
            // TODO: Add post logic here
          },
          icon: const Icon(Icons.share),
          label: const Text('Post to Instagram & Facebook'),
        ),
      ),
    );
  }
}
