import 'package:flutter/material.dart';
import 'package:boidsgame/arrow_control.dart';
import 'package:firebase_database/firebase_database.dart';

class GamePage extends StatelessWidget {
  final String playerName;

  GamePage({required this.playerName});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: Center(
        child: ArrowControl(playerName: playerName),
      ),
    );
  }
}
