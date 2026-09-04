# FLAC Music Player

A feature-rich music player for FLAC files built with Python and Tkinter.

## Features

- 🎵 Play/Pause/Stop FLAC audio files
- 📂 Playlist management (add/remove songs)
- ⏱️ Progress bar with seek functionality
- 🔊 Volume control
- 📊 Display song metadata (title, artist, duration)
- 🎨 Clean and intuitive GUI
- ⏯️ Play next/previous track controls

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/school22-lang/flac-music-player.git
cd flac-music-player
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the player:
```bash
python main.py
```

### Controls

- **Add Files**: Click "Add Song" to select FLAC files
- **Play/Pause**: Click the play/pause button to control playback
- **Volume**: Use the volume slider to adjust volume
- **Seek**: Click on the progress bar to jump to a position
- **Playlist**: Double-click a song to play it, or use Previous/Next buttons
- **Remove**: Select a song and click "Remove" to delete from playlist

## Supported Formats

- FLAC (.flac)

## Technical Details

- **Audio Playback**: sounddevice + soundfile
- **Metadata Reading**: mutagen
- **GUI Framework**: tkinter (built-in with Python)

## Project Structure

```
flac-music-player/
├── main.py                 # Main application entry point
├── player.py               # Audio playback logic
├── metadata.py             # FLAC metadata handling
├── ui.py                   # GUI components
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## License

MIT License

## Contributing

Feel free to submit issues and pull requests!

---

**Enjoy your music! 🎶**
