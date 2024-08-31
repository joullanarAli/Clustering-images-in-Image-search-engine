import 'package:flutter/material.dart';

class BaseScreen extends StatelessWidget {
  final Widget body;
  final String title;

  const BaseScreen({required this.body, required this.title});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(title,
          style: const TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold
          ),
        ),
        backgroundColor: const Color(0xFF8978F1),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout,
              color: Colors.white,
              weight: 200,
            ),
            onPressed: () {
              Navigator.pushNamed(context, '/');
            },
          ),

        ],
      ),
      drawer: Drawer(
        child: Column(
          children: [
            const DrawerHeader(
              decoration: BoxDecoration(
                color: Color(0xFF8978F1),
                //shape: BoxShape.rectangle
              ),
              padding: EdgeInsets.symmetric(horizontal: 120.5,vertical: 40),
              child: Text(
                'Menu',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                  fontWeight: FontWeight.bold
                ),
              ),
              
            ),
            ListTile(
              title: const Text('Search History',
                style: TextStyle(
                  color: Color(0xFF8978F1),
                  fontWeight: FontWeight.bold,
                  fontSize: 25
                ),
              ),
              onTap: () {
                Navigator.pushNamed(context, '/history',);
              },
            ),
            ListTile(
              title: const Text('Logout',
                  style: TextStyle(
                    color: Color(0xFF8978F1),
                    fontWeight: FontWeight.bold,
                    fontSize: 25
                  ),
                ),
              onTap: () {
                Navigator.pushNamed(context, '/');
              },
            ),
          ],
        ),
      ),
      body: body,
      // bottomNavigationBar: BottomAppBar(
      //   child: Row(
      //     mainAxisAlignment: MainAxisAlignment.spaceAround,
      //     children: [
      //       IconButton(
      //         icon: const Icon(Icons.login),
      //         onPressed: () {
      //           Navigator.pushNamed(context, '/login');
      //         },
      //       ),
      //       IconButton(
      //         icon: const Icon(Icons.app_registration),
      //         onPressed: () {
      //           Navigator.pushNamed(context, '/register');
      //         },
      //       ),
      //     ],
      //   ),
      // ),
    );
  }
}
