// Flutter Web App: Music Playback + AWS Integration (With Sound Fix)

import 'dart:html' as html;
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:just_audio/just_audio.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: AudioUploadPage(),
    );
  }
}

class AudioUploadPage extends StatefulWidget {
  const AudioUploadPage({super.key});

  @override
  State<AudioUploadPage> createState() => _AudioUploadPageState();
}

class _AudioUploadPageState extends State<AudioUploadPage> {
  final AudioPlayer _audioPlayer = AudioPlayer();
  double _pitch = 1.0;
  double _speed = 1.0;
  String? _fileName;
  bool _isAudioLoaded = false;

  Future<void> _pickAudio() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['mp3', 'wav'],
    );

    if (result != null && result.files.single.bytes != null) {
      final fileBytes = result.files.single.bytes!;
      final fileName = result.files.single.name;

      final blob = html.Blob([fileBytes], 'audio/mpeg');
      final url = html.Url.createObjectUrlFromBlob(blob);

      try {
        final duration = await _audioPlayer.setUrl(url);
        print('Audio duration: $duration');
        _audioPlayer.setVolume(1.0);
        setState(() {
          _fileName = fileName;
          _isAudioLoaded = true;
        });
      } catch (e) {
        print("Error loading audio: $e");
        setState(() {
          _isAudioLoaded = false;
        });
      }
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
      backgroundColor: Colors.grey[200],
      appBar: AppBar(
        title: const Text('Music Generator Web App'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: _pickAudio,
              child: const Text('Upload Audio File'),
            ),
            const SizedBox(height: 10),
            Text(_fileName ?? 'No file selected'),
            const SizedBox(height: 20),
            if (_isAudioLoaded) ...[
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  ElevatedButton(
                    onPressed: () {
                      _audioPlayer.play().catchError((error) {
                        print("Play error: $error");
                      });
                    },
                    child: const Text('Play'),
                  ),
                  const SizedBox(width: 10),
                  ElevatedButton(
                    onPressed: _audioPlayer.pause,
                    child: const Text('Pause'),
                  ),
                ],
              ),
              const SizedBox(height: 20),
              Column(
                children: [
                  const Text("Tempo"),
                  Slider(
                    value: _speed,
                    min: 0.5,
                    max: 2.0,
                    divisions: 15,
                    label: "${_speed.toStringAsFixed(2)}x",
                    onChanged: (value) {
                      setState(() {
                        _speed = value;
                        _audioPlayer.setSpeed(_speed);
                      });
                    },
                  ),
                  const Text("Pitch (Experimental)"),
                  Slider(
                    value: _pitch,
                    min: 0.5,
                    max: 2.0,
                    divisions: 15,
                    label: "${_pitch.toStringAsFixed(2)}x",
                    onChanged: (value) {
                      setState(() {
                        _pitch = value;
                        // just_audio doesn't support pitch natively on web
                      });
                    },
                  ),
                ],
              ),
            ],
            const SizedBox(height: 20),
            const Text("AWS backend integration is in progress..."),
          ],
        ),
      ),
    );
  }
}
