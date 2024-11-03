import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: PasswordStrengthChecker(),
    );
  }
}

class PasswordStrengthChecker extends StatefulWidget {
  const PasswordStrengthChecker({super.key});

  @override
  PasswordStrengthCheckerState createState() =>
      PasswordStrengthCheckerState(); // Updated to public
}

class PasswordStrengthCheckerState extends State<PasswordStrengthChecker> {
  String _strength = '';

  void _checkPasswordStrength(String password) {
    setState(() {
      _strength = _getStrength(password);
    });
  }

  String _getStrength(String password) {
    if (password.isEmpty) return 'Enter a password';
    if (password.length < 6) return 'Weak';
    if (password.length < 10) return 'Moderate';
    if (password.contains(RegExp(r'[A-Z]')) &&
        password.contains(RegExp(r'[0-9]')) &&
        password.contains(RegExp(r'[!@#$%^&*(),.?":{}|<>]'))) {
      return 'Strong';
    }
    return 'Moderate';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Password Strength Checker'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              obscureText: true,
              decoration: const InputDecoration(labelText: 'Enter Password'),
              onChanged: _checkPasswordStrength,
            ),
            const SizedBox(height: 20),
            Text(
              'Strength: $_strength',
              style: TextStyle(
                fontSize: 24,
                color: _strength == 'Strong'
                    ? Colors.green
                    : (_strength == 'Moderate' ? Colors.orange : Colors.red),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
