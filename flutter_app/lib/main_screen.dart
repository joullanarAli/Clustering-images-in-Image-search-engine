import 'package:flutter/material.dart';

import 'base_screen.dart';
import 'results_screen.dart';

class MainScreen extends StatefulWidget {
  @override
  _MainScreenState createState() => _MainScreenState();
}
class _MainScreenState extends State<MainScreen> {
  String _searchQuery = '';
  int _selectedClusterCount = 2;
  @override
  Widget build(BuildContext context) {
    return BaseScreen(
        title: "Image Search Engine",

        body: Center(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  'Image Search',
                  style: Theme.of(context).textTheme.displayLarge, // Uses the headline style
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 20),
                TextField(
                  onChanged: (value) {
                    setState(() {
                      _searchQuery = value;
                    });
                  },
                  decoration: InputDecoration(
                    hintText: 'Enter search query',
                    hintStyle: Theme.of(context)
                        .inputDecorationTheme
                        .hintStyle, // Uses the hint style from the theme
                  ),

                ),
                const SizedBox(height: 20),
                // Dropdown to select the number of clusters
                DropdownButton<int>(
                  value: _selectedClusterCount,
                  items: <int>[1, 2, 3, 4, 5, 6, 7, 8, 9, 10] // Options for clusters
                      .map<DropdownMenuItem<int>>((int value) {
                    return DropdownMenuItem<int>(
                      value: value,
                      child: Text('$value clusters'),
                    );
                  }).toList(),
                  onChanged: (int? newValue) {
                    setState(() {
                      _selectedClusterCount = newValue!;

                    });
                  },
                ),
                const SizedBox(height: 20),
                ElevatedButton(
                  onPressed: () {
                    if (_searchQuery.isNotEmpty) {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => ResultsScreen(
                              query: _searchQuery,
                              clusterCount: _selectedClusterCount,),
                        ),
                      );
                    } else {
                      // Optionally, show a warning if the query is empty
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text('Please enter a search query'),
                        ),
                      );
                    }
                  },
                  child: const Text('Search'),
                ),
              ],
            ),
          ),
        ),
    );
  }
}
