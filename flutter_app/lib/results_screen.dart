import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'cluster_screen.dart'; // Import the ClusterScreen

class ResultsScreen extends StatefulWidget {
  final String query;
  final int x=1;

  final dynamic clusterCount;
  const ResultsScreen({Key? key, required this.query, required this.clusterCount}) : super(key: key);

  @override
  _ResultsScreenState createState() => _ResultsScreenState();
}

class _ResultsScreenState extends State<ResultsScreen> {
  Map<String, List<String>> _clusters = {};
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchResults();
  }

  Future<void> _fetchResults() async {
    try {
      final url = Uri.parse('http://10.0.2.2:5000/search?query=${widget.query}&n_clusters=${widget.clusterCount}');

      final response = await http.get(url);

      if (response.statusCode == 200) {
        final jsonResponse = json.decode(response.body);
        final clusters = jsonResponse['clusters'] as Map<String, dynamic>;

        setState(() {
          _clusters = clusters.map((key, value) => MapEntry(key, List<String>.from(value)));
          _isLoading = false;
        });
      } else {
        throw Exception('Failed to load results');
      }
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error fetching results: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    // Sort the cluster keys numerically
    final sortedClusterKeys = _clusters.keys.toList()..sort((a, b) => int.parse(a).compareTo(int.parse(b)));

    return Scaffold(
      appBar: AppBar(
        title: Text('Results for "${widget.query}"',
        style: const TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
        ),
        ),
        backgroundColor: const Color(0xFF8978F1),
      ),
      body: _isLoading
          ? Center(child: CircularProgressIndicator())
          : _clusters.isEmpty
          ? Center(child: Text('No results found'))
          : ListView.builder(
        itemCount: sortedClusterKeys.length,
        itemBuilder: (context, index) {
          final clusterKey = sortedClusterKeys[index];
          final clusterImages = _clusters[clusterKey]!;

          // Limit to first 3 images
          final imagesToShow = clusterImages.take(3).toList();

          return Padding(
            padding: const EdgeInsets.all(8.0),
            child: GestureDetector(
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => ClusterScreen(
                      clusterKey: clusterKey,
                      images: clusterImages,
                    ),
                  ),
                );
              },
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Cluster ${int.parse(clusterKey)+1}',
                    style: Theme.of(context).textTheme.displayLarge,
                  ),
                  const SizedBox(height: 10),
                  GridView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 3,
                      crossAxisSpacing: 8.0,
                      mainAxisSpacing: 8.0,
                    ),
                    itemCount: imagesToShow.length,
                    itemBuilder: (context, imageIndex) {
                      final imageUrl = 'http://10.0.2.2:5000/static/clusters/cluster_${clusterKey}/${imagesToShow[imageIndex]}';
                      return Image.network(
                        imageUrl,
                        fit: BoxFit.cover,
                        errorBuilder: (context, error, stackTrace) {
                          return Center(child: Text('Error loading image'));
                        },
                      );
                    },
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
