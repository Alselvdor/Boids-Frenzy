import 'package:flutter/material.dart';
import 'enter_name_page.dart';

class BoidHomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Expanded(
            child: Align(
              alignment: Alignment.center,
              child: Text(
                ' BOID\'s',
                style: TextStyle(fontSize: 24.0, fontWeight: FontWeight.bold),
              ),
            ),
          ),
          Align(
            alignment: Alignment.bottomCenter,
            child: Padding(
              padding: const EdgeInsets.only(bottom: 16.0),
              child: ElevatedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => EnterNamePage()),
                  );
                },
                style: ElevatedButton.styleFrom(
                  padding: EdgeInsets.all(16.0),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10.0),
                  ),
                ),
                child: Text('Begin'),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
