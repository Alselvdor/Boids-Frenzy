import 'package:firebase_database/firebase_database.dart';

class DatabaseService {
  final DatabaseReference _db = FirebaseDatabase.instance.reference();

  Future<void> sendDirection(String direction) async {
    await _db.child('directions').push().set({
      'direction': direction,
      'timestamp': ServerValue.timestamp,
    });
  }
}
