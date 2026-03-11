# Jarvis - Virtual Voice Assistant

Jarvis is a Python-based desktop voice assistant that listens to voice commands and responds using speech and on-screen output.

## Features

- Voice input using microphone
- Voice responses using text-to-speech
- Wikipedia search summary
- Open common websites (YouTube, Google, Gmail, HackerRank, Stack Overflow)
- Tell current time
- CPU usage check
- Read top business headlines (NewsAPI)
- Basic utility commands like addition, waiting, and coin toss
- Email sending support via Gmail SMTP

## Setup

1. Clone this repository.
2. (Recommended) Create a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Set these optional environment variables for full functionality:

- `NEWS_API_KEY` - API key for https://newsapi.org
- `JARVIS_EMAIL` - sender Gmail address
- `JARVIS_EMAIL_PASSWORD` - sender Gmail app password
- `JARVIS_FLIP_SOUND` - full path to a coin flip sound file

### Example (Linux/macOS)

```bash
export NEWS_API_KEY="your_api_key"
export JARVIS_EMAIL="youremail@gmail.com"
export JARVIS_EMAIL_PASSWORD="your_app_password"
export JARVIS_FLIP_SOUND="/full/path/to/flip.mp3"
```

### Example (Windows PowerShell)

```powershell
$env:NEWS_API_KEY="your_api_key"
$env:JARVIS_EMAIL="youremail@gmail.com"
$env:JARVIS_EMAIL_PASSWORD="your_app_password"
$env:JARVIS_FLIP_SOUND="C:\full\path\flip.mp3"
```

## Run

```bash
python jarvis.py
```

## Notes

- Microphone and speaker access are required.
- For Gmail, use an app password instead of your main account password.
- The Visual Studio Code launcher path in the script is currently set for one machine and may need updating.
