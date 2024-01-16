import 'package:flutter/material.dart';
import 'package:firebase_database/firebase_database.dart';
import 'ready_page.dart';

class EnterNamePage extends StatelessWidget {
  final TextEditingController _nameController = TextEditingController();

  Future<void> _sendDataToFirebase(String playerName) async {
    final DatabaseReference _db = FirebaseDatabase.instance.reference();
    await _db.child('players').push().set({
      'name': playerName,
      'direction': '', // Initialize direction to an empty string
      'state': 'not_ready', // Initialize player state to 'not_ready'
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: TextField(
                controller: _nameController,
                decoration: InputDecoration(
                  labelText: 'Player\'s Name',
                ),
              ),
            ),
            ElevatedButton(
              onPressed: () async {
                String playerName = _nameController.text;
                await _sendDataToFirebase(playerName);
                Navigator.push(
                  context,
                  MaterialPageRoute(
                      builder: (context) => ReadyPage(playerName: playerName)),
                );
              },
              child: Text('Submit'),
            ),
          ],
        ),
      ),
    );
  }
}
