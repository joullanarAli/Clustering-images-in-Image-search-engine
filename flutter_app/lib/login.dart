import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:test_flutter/register.dart';
import 'package:http/http.dart' as http;
import 'main_screen.dart';

class loginScreen extends StatefulWidget {
  const loginScreen({Key? key}) : super(key: key);
  _loginState createState() => _loginState();
}
class _loginState extends State<loginScreen>{
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  bool _isLoading = false;
  String? _errorMessage;
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();

  Future<void> _login() async {
    if (_formKey.currentState == null || !_formKey.currentState!.validate()) {
      // If the form state is null or validation fails, exit the function early
      return;
    }
    print(_emailController);
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

      // Replace with your API URL
      const String apiUrl = "http://10.0.2.2:5000/login";


      try {
        final response = await http.post(
          Uri.parse(apiUrl),
          headers: {
            'Content-Type': 'application/json', // Specify JSON content type
          },
          body: jsonEncode({
            'email': _emailController.text,
            'password': _passwordController.text,
          }),
        );

        if (response.statusCode == 200) {
          // Navigate to the main screen
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (context) => MainScreen()),
          );
        } else {
          // Show error message
          setState(() {
            _errorMessage = 'Login failed. Email or Password incorrect.';
          });
        }
        print('Server response: ${response.body}');
      } catch (e) {
        setState(() {
          _errorMessage = 'An error occurred. Please try again.';
        });

      } finally {
        setState(() {
          _isLoading = false;
        });
      }
    }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          Container(
            height: double.infinity,
            width: double.infinity,
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [Color(0xFF8978F1), Color(0xff281537)],
              ),
            ),
            child: const Padding(
              padding: EdgeInsets.only(top: 80.0, left:100),
              child:  Text(
                'Hello Sign in!',
                style: TextStyle(
                  fontSize: 30,
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.only(top: 150.0),
            child: SingleChildScrollView( // Wrap with SingleChildScrollView
              physics: const BouncingScrollPhysics(), // Optional: Add scrolling physics
              child: Container(
                decoration: const BoxDecoration(
                  borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(40),
                    topRight: Radius.circular(40),
                  ),
                  color: Colors.white,
                ),
                height: MediaQuery.of(context).size.height, // Adjust height
                width: double.infinity,
                child: Padding(
                  padding: const EdgeInsets.only(left: 18.0, right: 18),
                  child: Form(
                    key: _formKey,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      TextField(
                        controller: _emailController,
                        decoration: const InputDecoration(
                          suffixIcon: Icon(Icons.check, color: Colors.grey),
                          label: Text(

                            'Email',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color: Color(0xFF8978F1),
                            ),
                          ),
                        ),
                      ),
                      TextField(
                        controller: _passwordController,
                        obscureText: true,
                        decoration: const InputDecoration(
                          suffixIcon: Icon(Icons.visibility_off, color: Colors.grey),
                          label: Text(
                            'Password',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color: Color(0xFF8978F1),
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 20),
                      const SizedBox(height: 70),
                      _isLoading
                          ? const CircularProgressIndicator()
                          : ElevatedButton(
                        onPressed: _login,
                        style: ElevatedButton.styleFrom(
                          padding: EdgeInsets.zero,  // Removes default padding
                          minimumSize: const Size(300, 55),  // Set the button's size to match the desired dimensions
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(30),  // Apply border radius
                          ),
                        ).copyWith(
                          backgroundColor: MaterialStateProperty.resolveWith<Color>((Set<MaterialState> states) {
                            if (states.contains(MaterialState.pressed)) {
                              return const Color(0xff281537);  // Darker color when pressed
                            }
                            return Colors.transparent;  // Make the background transparent
                          }),

                        ),
                        child: Ink(
                          decoration: BoxDecoration(
                            gradient: const LinearGradient(
                              colors: [Color(0xFF8978F1), Color(0xff281537)],
                            ),
                            borderRadius: BorderRadius.circular(30),
                          ),
                          child: Container(
                            height: 55,
                            width: 300,
                            alignment: Alignment.center,
                            child: const Text(
                              'SIGN IN',
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 20,
                                color: Colors.white,
                              ),
                            ),
                          ),
                        ),
                      ),

                      if (_errorMessage != null) ...[
                              const SizedBox(height: 20),
                              Text(
                                _errorMessage!,
                                style: const TextStyle(
                                  color: Colors.red,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                      const SizedBox(height: 60),
                      Align(
                        alignment: Alignment.center,
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            const Text(
                              "Don't have an account?",
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                color: Colors.grey,
                              ),
                            ),
                          GestureDetector(  // Wrap Text with GestureDetector
                            onTap: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(builder: (context) => const RegScreen()),
                              );
                            },
                            child: const Text(
                              "Sign up",
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 17,
                                color: Colors.black,
                              ),
                            ),
                          )],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
          )],
      ),
    );
  }
}