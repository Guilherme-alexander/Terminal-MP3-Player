# Terminal MP3 Player

Modern terminal-based MP3 player built with Python, curses and pygame.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue?style=for-the-badge)
![Terminal](https://img.shields.io/badge/UI-Terminal-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-apache-blue?style=for-the-badge)

---

## Preview

```text
████████╗███╗   ███╗██████╗
╚══██╔══╝████╗ ████║██╔══██╗
   ██║   ██╔████╔██║██████╔╝
   ██║   ██║╚██╔╝██║██╔═══╝
   ██║   ██║ ╚═╝ ██║██║
   ╚═╝   ╚═╝     ╚═╝╚═╝

┌─────────────────────────────┐
|     TERMINAL MP3 PLAYER     |
└─────────────────────────────┘
```

---

## Features

- MP3 playback
- Terminal UI with curses
- Modern blue/white terminal theme
- Music progress bar
- Automatic music scanning
- Keyboard navigation
- Pagination system
- Pause and resume
- Volume control
- Next/previous music
- Real-time playback status
- Cross-platform support

---

## Technologies

- Python
- curses
- pygame
- mutagen
- rich

---

## Requirements

- Python 3.10+
- Windows Terminal / Linux Terminal
- MP3 files inside your Music folder

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Guilherme-alexander/Terminal-MP3-Player.git
```

Enter the project folder:

```bash
cd Terminal-MP3-Player
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run

```bash
python main.py
```

---

## Music Folder

The application automatically scans your default Music folder:

### Windows

```text
C:\Users\Guilherme-alexander\Music
```

### Linux

```text
/home/Guilherme-alexander/Music
```

Used internally:

```python
PATH = os.path.join(
    os.path.expanduser("~"),
    "Music"
)
```

---

## Controls

| Key | Action |
|---|---|
| ↑ ↓ | Navigate music |
| ← → | Change page |
| ENTER | Play music |
| SPACE | Pause / Resume |
| S | Stop music |
| N | Next music |
| B | Previous music |
| + - | Volume control |
| ESC | Back to menu |
| Q | Quit application |
| CTRL + C | Force close |

---

## Screenshots

### Main Menu

```text
♫ TERMINAL MP3 PLAYER ♫
────────────────────────────────────────────

> music_01.mp3
  music_02.mp3
  music_03.mp3
```

### Player

```text
Music : my_music.mp3

00:01:52 [██████████░░░░░░░░] 52%

Status : PLAYING
Volume : 50%
```

---

## Customization

### Songs per page

```python
TOTAL_MUSICS = 15
```

### Default volume

```python
volume = 0.5
```

### Progress bar style

```python
"█" * fill + "░" * empty
```

---

## Project Structure

```text
Terminal-MP3-Player/
│
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Future Improvements

- Playlist support
- Shuffle mode
- Repeat mode
- Audio visualizer
- Themes system
- Config file
- Search system
- Mouse support
- Album metadata
- WAV/FLAC support

---

## License

Apache License (Apache-2.0 license)

---

## Author

#### @Guilherme-alexander
Terminal MP3 Player was developed using Python with a focus on terminal aesthetics and retro-modern CLI interfaces.
