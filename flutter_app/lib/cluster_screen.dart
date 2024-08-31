import 'package:flutter/material.dart';

class ClusterScreen extends StatelessWidget {
  final String clusterKey;
  final List<String> images;

  const ClusterScreen({Key? key, required this.clusterKey, required this.images}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Cluster $clusterKey',
            style: const TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.bold,
            ),),
        backgroundColor: const Color(0xFF8978F1),

      ),
      body: images.isEmpty
          ? Center(child: Text('No images available'))
          : GridView.builder(
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 3,
          crossAxisSpacing: 8.0,
          mainAxisSpacing: 8.0,
        ),
        itemCount: images.length,
        itemBuilder: (context, index) {
          final imageUrl = 'http://10.0.2.2:5000/static/clusters/cluster_${clusterKey}/${images[index]}';
          return Image.network(
            imageUrl,
            fit: BoxFit.cover,
            errorBuilder: (context, error, stackTrace) {
              return Center(child: Text('Error loading image'));
            },
          );
        },
      ),
    );
  }
}
