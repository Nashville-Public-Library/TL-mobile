import 'package:flutter/material.dart';
import 'package:just_audio/just_audio.dart';
import 'package:http/http.dart' as http;
import 'dart:convert'; // For decoding JSON
import 'dart:async'; // Import Timer

void main() {
  runApp(MyApp());
}



class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: RadioPlayer(),
    );
  }
}

class NowPlaying extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return  DataFetcher();
    
  }
}

class DataFetcher extends StatelessWidget {  
  
  Future<Map<String, dynamic>> fetchData() async {
    final url = Uri.parse('https://api.nashvilletalkinglibrary.com/stream/status');
    final response = await http.post(url);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load data');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: FutureBuilder<Map<String, dynamic>>(
        future: fetchData(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return CircularProgressIndicator();
          } else if (snapshot.hasError) {
            return Text('Error: ${snapshot.error}');
          } else if (snapshot.hasData) {
            final data = snapshot.data!;
            return Text('Now Playing: ${data['title']}');
          } else {
            return Text('Program name not available');
          }
        },
      ),
    );
  }
}

class RadioPlayer extends StatefulWidget {
  @override
  _RadioPlayerState createState() => _RadioPlayerState();
}

class _RadioPlayerState extends State<RadioPlayer> {
  final AudioPlayer _audioPlayer = AudioPlayer();
  bool _isPlaying = false;
  bool _isLoading = false;
  String _errorMessage = '';

  @override
  void initState() {
    super.initState();
    _playRadio();
  }

  Future<void> _playRadio() async {
    setState(() {
      _isLoading = true;
    });

    try {
      String radioUrl = 'https://api.nashvilletalkinglibrary.com/stream/livestream.mp3'; // Replace with your radio URL
      await _audioPlayer.setUrl(radioUrl);
      // _audioPlayer.play();
      setState(() {
        _isPlaying = false;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
        _errorMessage = 'Error loading stream';
      });
      print('Error: $e');
    }
  }

  @override
  void dispose() {
    _audioPlayer.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('NTL Stream'),
        backgroundColor: Colors.blue,
        elevation: 4.0,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (_isLoading)
              CircularProgressIndicator()
            else if (_errorMessage.isNotEmpty)
              Text(
                _errorMessage,
                style: TextStyle(fontSize: 18, color: Colors.red),
                textAlign: TextAlign.center,
              )
            else ...[
              Text(
                _isPlaying ? 'Playing' : 'Paused',
                style: TextStyle(fontSize: 24),
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  setState(() {
                    if (_isPlaying) {
                      _audioPlayer.pause();
                    } else {
                      _audioPlayer.play();
                    }
                    _isPlaying = !_isPlaying;
                  });
                },
                child: Text(_isPlaying ? 'Pause' : 'Play'),
                
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  _audioPlayer.stop();
                  setState(() {
                    _isPlaying = false;
                  });
                },
                child: Text('Stop'),
              ),

              // NOW PLAYING HERE!
              DataFetcher(),
              Logo(),

            ],
          ], 
        ),
      ),
    );
  }
}

class Logo extends StatelessWidget {
  @override
  Widget build(BuildContext context) {


  return Padding(
    padding: EdgeInsets.only(top: 35, right: 10, left: 10),
    child: Container(
        height: 200,
        child: Column(
          children: <Widget>[
            Container(
              // don't forget about height
              height: 200,
              width: 200,
              child: Image.asset(
                'assets/img/NTL_fav.png', 
                width: 100,
                height: 100,
                fit:BoxFit.fill)),
            
          ],
        ),
      ),
  );
  }

  //   return Scaffold(
  //       body: Container(
  //         decoration: BoxDecoration(color: Colors.deepOrangeAccent),
  //           height: 50,
  //           width: 50,
  //           child: 
  //             Column(
  //           Container( Image.asset('assets/img/NTL_fav.png', 
  //                                         width: 100,
  //                                         height: 100,
  //                                         fit:BoxFit.fill)),
  //             )
  //       )
  //       )
  //     );
  // }


}


Future<Map<String, dynamic>> fetchData() async {
  final url = Uri.parse('https://api.nashvilletalkinglibrary.com/stream/status'); // Example API endpoint
  final response = await http.post(url);

  if (response.statusCode == 200) {
    // Parse the JSON response
    return json.decode(response.body);
  } else {
    // Handle errors
    throw Exception('Failed to load data');
  }
}