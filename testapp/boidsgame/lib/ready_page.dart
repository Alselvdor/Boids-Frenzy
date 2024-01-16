import 'package:flutter/material.dart';
import 'package:firebase_database/firebase_database.dart';
import 'game_page.dart';

class ReadyPage extends StatelessWidget {
  final String playerName;

  ReadyPage({required this.playerName});

  Future<void> _updatePlayerStateToFirebase(String state) async {
    final DatabaseReference _db = FirebaseDatabase.instance.reference();

    try {
      DataSnapshot snapshot = await (_db
          .child('players')
          .orderByChild('name')
          .equalTo(playerName)
          .once() as DataSnapshot);

      // Null check and type cast
      Map<dynamic, dynamic>? data = snapshot.value as Map<dynamic, dynamic>?;

      if (data != null) {
        String playerKey = data.keys.first;
        await _db.child('players').child(playerKey).update({'state': state});
      }
    } catch (error) {
      print('Error updating player state: $error');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            ElevatedButton(
              onPressed: () async {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('Waiting for other players...'),
                  ),
                );
                await _updatePlayerStateToFirebase('ready');
                Navigator.push(
                  context,
                  MaterialPageRoute(
                      builder: (context) => GamePage(playerName: playerName)),
                );
              },
              child: Text('Ready'),
            ),
          ],
        ),
      ),
    );
  }
}
