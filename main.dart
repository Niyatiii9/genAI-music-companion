import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:just_audio/just_audio.dart';

void main() => runApp(MusicGenWebApp());

class MusicGenWebApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '🎵 Music Generator Web',
      theme: ThemeData.dark(),
      home: MusicHomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class MusicHomePage extends StatefulWidget {
  @override
  _MusicHomePageState createState() => _MusicHomePageState();
}

class _MusicHomePageState extends State<MusicHomePage> {
  final AudioPlayer _player = AudioPlayer();
  PlatformFile? _pickedFile;
  double _tempo = 1.0; // Normal tempo
  double _pitch = 1.0; // Normal pitch

  /// Function: Pick and load audio file
  Future<void> _pickAudioFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['mp3', 'wav'],
    );

    if (result != null) {
      _pickedFile = result.files.first;

      try {
        await _player.setFilePath(_pickedFile!.path!);
        _player.play();
      } catch (e) {
        print("Error loading audio: $e");
      }

      setState(() {});
    }
  }

  @override
  void dispose() {
    _player.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("🎧 Music Generator Web App"),
        centerTitle: true,
      ),
      body: Center(
        child: Padding(
          padding: EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ElevatedButton.icon(
                onPressed: _pickAudioFile,
                icon: Icon(Icons.upload_file),
                label: Text("Upload Audio File"),
                style: ElevatedButton.styleFrom(padding: EdgeInsets.all(12)),
              ),
              SizedBox(height: 30),

              if (_pickedFile != null) ...[
                Text(
                  "🎶 Now Playing: ${_pickedFile!.name}",
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
                ),
                SizedBox(height: 16),

                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    IconButton(
                      icon: Icon(Icons.play_arrow),
                      onPressed: () => _player.play(),
                    ),
                    IconButton(
                      icon: Icon(Icons.pause),
                      onPressed: () => _player.pause(),
                    ),
                    IconButton(
                      icon: Icon(Icons.stop),
                      onPressed: () => _player.stop(),
                    ),
                  ],
                ),

                SizedBox(height: 24),
                Text(
                  "Tempo: ${_tempo.toStringAsFixed(2)}",
                  style: TextStyle(fontSize: 16),
                ),
                Slider(
                  value: _tempo,
                  min: 0.5,
                  max: 2.0,
                  divisions: 15,
                  label: _tempo.toStringAsFixed(2),
                  onChanged: (val) => setState(() => _tempo = val),
                ),

                SizedBox(height: 20),
                Text(
                  "Pitch: ${_pitch.toStringAsFixed(2)}",
                  style: TextStyle(fontSize: 16),
                ),
                Slider(
                  value: _pitch,
                  min: 0.5,
                  max: 2.0,
                  divisions: 15,
                  label: _pitch.toStringAsFixed(2),
                  onChanged: (val) => setState(() => _pitch = val),
                ),

                SizedBox(height: 30),
                ElevatedButton.icon(
                  onPressed: () {
                    print("File: ${_pickedFile!.name}");
                    print("Tempo: $_tempo");
                    print("Pitch: $_pitch");

                    // TODO: Connect to AWS backend
                  },
                  icon: Icon(Icons.cloud_upload),
                  label: Text("Send to AWS to Generate Music 🎧"),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
