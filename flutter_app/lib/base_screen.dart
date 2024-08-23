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
            icon: const Icon(Icons.login,
              color: Colors.white,
              weight: 200,
            ),
            onPressed: () {
              Navigator.pushNamed(context, '/login');
            },
          ),
          IconButton(
            icon: const Icon(Icons.app_registration,
              color: Colors.white,
            ),
            onPressed: () {
              Navigator.pushNamed(context, '/register');
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
              title: const Text('Login',
                style: TextStyle(
                  color: Color(0xFF8978F1),
                  fontWeight: FontWeight.bold,
                  fontSize: 25
                ),
              ),
              onTap: () {
                Navigator.pushNamed(context, '/login',);
              },
            ),
            ListTile(
              title: const Text('Register',
                  style: TextStyle(
                    color: Color(0xFF8978F1),
                    fontWeight: FontWeight.bold,
                    fontSize: 25
                  ),
                ),
              onTap: () {
                Navigator.pushNamed(context, '/register');
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
