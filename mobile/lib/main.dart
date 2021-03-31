import 'package:flutter/material.dart';
import './screens/login_page.dart';

void main() => runApp(App());

class App extends StatelessWidget {
  @override
  MaterialApp build(BuildContext ctx) => MaterialApp(
    debugShowCheckedModeBanner: false,
    home: LoginPage(),
    theme: ThemeData(
      appBarTheme: AppBarTheme(
        backgroundColor: Colors.white
      )
    ),
  );
}
