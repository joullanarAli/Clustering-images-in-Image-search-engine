import 'package:flutter/material.dart';

import 'login.dart';

class RegScreen extends StatelessWidget {
  const RegScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Stack(//thanks for watching
          children: [
            Container(
              height: double.infinity,
              width: double.infinity,
              decoration: const BoxDecoration(
                gradient: LinearGradient(colors: [
                  Color(0xFF8978F1),
                  Color(0xff281537),
                ]),
              ),
              child: const Padding(
                padding: EdgeInsets.only(top: 60.0, left: 60),
                child: Text(
                  'Create Your Account',
                  style: TextStyle(
                      fontSize: 30,
                      color: Colors.white,
                      fontWeight: FontWeight.bold),
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.only(top: 150.0),
              child: SingleChildScrollView( // Wrap with SingleChildScrollView
                physics: const BouncingScrollPhysics(),
                child: Container(
                decoration: const BoxDecoration(
                  borderRadius: BorderRadius.only(
                      topLeft: Radius.circular(40), topRight: Radius.circular(40)),
                  color: Colors.white,
                ),
                height: MediaQuery.of(context).size.height,
                width: double.infinity,
                child:  Padding(
                  padding: const EdgeInsets.only(left: 18.0,right: 18),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const TextField(
                        decoration: InputDecoration(
                            suffixIcon: Icon(Icons.check,color: Colors.grey,),
                            label: Text('User Name',style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color:Color(0xFF8978F1),
                            ),)
                        ),
                      ),
                      const TextField(
                        decoration: InputDecoration(
                            suffixIcon: Icon(Icons.check,color: Colors.grey,),
                            label: Text('Email',style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color:Color(0xFF8978F1),
                            ),)
                        ),
                      ),
                      const TextField(
                        decoration: InputDecoration(
                            suffixIcon: Icon(Icons.visibility_off,color: Colors.grey,),
                            label: Text('Password',style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color:Color(0xFF8978F1),
                            ),)
                        ),
                      ),
                      const TextField(
                        decoration: InputDecoration(
                            suffixIcon: Icon(Icons.visibility_off,color: Colors.grey,),
                            label: Text('Confirm Password',style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color:Color(0xFF8978F1),
                            ),)
                        ),
                      ),

                      const SizedBox(height: 10,),
                      const SizedBox(height: 70,),
                      Container(
                        height: 55,
                        width: 300,
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(30),
                          gradient: const LinearGradient(
                              colors: [
                                Color(0xFF8978F1),
                                Color(0xff281537),
                              ]
                          ),
                        ),
                        child: const Center(child: Text('SIGN UP',style: TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 20,
                            color: Colors.white
                        ),),),
                      ),
                      const SizedBox(height: 10,),
                      Align(
                        alignment: Alignment.center,
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            const Text("Already have an account?",
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                color: Colors.grey
                               ),
                            ),
                        GestureDetector(  // Wrap Text with GestureDetector
                          onTap: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(builder: (context) => const loginScreen()),
                            );
                          },
                          child: const Text("Sign in",style: TextStyle(///done login page
                                fontWeight: FontWeight.bold,
                                fontSize: 17,
                                color: Colors.black
                            ),),
                        )],
                        ),
                      )
                    ],
                  ),
                ),
              ),
            ),
            )],
        ));
  }
}