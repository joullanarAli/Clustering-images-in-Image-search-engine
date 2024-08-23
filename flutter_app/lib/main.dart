import 'package:flutter/material.dart';
import 'main_screen.dart';
import 'cluster_screen.dart';
import 'results_screen.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Image Search Engine',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.deepPurple,
        scaffoldBackgroundColor: const Color(0xFFF5F6FD),// Global background color
        appBarTheme: const AppBarTheme(
            iconTheme: IconThemeData(
            color: Colors.white,
            weight: 300
        )),
        textTheme: const TextTheme(
          displayLarge: TextStyle(
            fontSize: 50,
            fontWeight: FontWeight.bold,
            color: Color(0xFF8978F1),
          ),
          displayMedium: TextStyle(
            fontSize: 18,
            color: Color(0xFF8978F1),
          ),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: const Color(0xFF8978F1), // Button background color
            foregroundColor: Colors.white, // Button text color
            textStyle: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(20),
            ),
          ),
        ),
        textButtonTheme: TextButtonThemeData(
          style: TextButton.styleFrom(
            backgroundColor: const Color(0xFF8978F1), // TextButton text color
            textStyle: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: Colors.white,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(20),
            borderSide: const BorderSide(
              color: Color(0xFF8978F1),
              style: BorderStyle.solid,
              width: 2,
            ),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(20),
            borderSide: const BorderSide(
              color: Color(0xFF8978F1),
              style: BorderStyle.solid,
              width: 2,
            ),
          ),
          hintStyle: TextStyle(color: const Color(0xFF8978F1).withOpacity(0.7)),
        ),
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => MainScreen(),
        '/results': (context) => ResultsScreen(query: ModalRoute.of(context)!.settings.arguments as String),
    '/cluster': (context) {
    final args = ModalRoute.of(context)!.settings.arguments as Map<String, dynamic>;
    return ClusterScreen(
    clusterKey: args['clusterKey'],
    images: args['images'],
    );
    },
      },
    );
  }
}
