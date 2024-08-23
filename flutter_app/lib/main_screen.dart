import 'package:flutter/material.dart';

import 'base_screen.dart';
import 'results_screen.dart';

class MainScreen extends StatefulWidget {
  @override
  _MainScreenState createState() => _MainScreenState();
}
class _MainScreenState extends State<MainScreen> {
  String _searchQuery = '';
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
                ElevatedButton(
                  onPressed: () {
                    if (_searchQuery.isNotEmpty) {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => ResultsScreen(query: _searchQuery),
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
