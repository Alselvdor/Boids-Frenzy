import 'package:flutter/material.dart';
import 'package:firebase_database/firebase_database.dart';

class ArrowControl extends StatefulWidget {
  final String playerName;

  ArrowControl({required this.playerName});

  @override
  _ArrowControlState createState() => _ArrowControlState();
}

class _ArrowControlState extends State<ArrowControl> {
  String currentDirection = '';
  final DatabaseReference _db = FirebaseDatabase.instance.reference();

  void _sendDirectionToFirebase(String direction) {
    _db
        .child('players')
        .child(widget.playerName)
        .update({'direction': direction});
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () {
                _sendDirectionToFirebase('up');
              },
              child: Icon(Icons.arrow_upward),
            ),
          ],
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () {
                _sendDirectionToFirebase('left');
              },
              child: Icon(Icons.arrow_back),
            ),
            ElevatedButton(
              onPressed: () {
                _sendDirectionToFirebase('right');
              },
              child: Icon(Icons.arrow_forward),
            ),
          ],
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () {
                _sendDirectionToFirebase('down');
              },
              child: Icon(Icons.arrow_downward),
            ),
          ],
        ),
        SizedBox(height: 20),
        Text('Current Direction: $currentDirection'),
      ],
    );
  }
}
