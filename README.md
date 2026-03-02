# Virtual Voice Assistant (Python)

A rebuilt version of your college project with **real voice commands** and **voice responses**.

## Features

- 🎙️ Voice command input through microphone
- 🔊 Spoken responses through speakers
A rebuilt version of your college project based on the resume description.

## Features

- Arithmetic calculations from natural commands (`add 10 and 5`, `divide 21 by 3`)
- Weather forecast notifications (mock response that is easy to replace with an API)
- Read newspapers/headlines by opening Google News
- Browse websites from command
- Play music via YouTube search
- Open local applications
- Send emails through SMTP (available via `SkillSet.send_mail`)

## Project Structure

```text
.
├── assistant/
│   ├── __init__.py
│   ├── core.py
│   ├── skills.py
│   └── voice.py
│   └── skills.py
├── tests/
│   └── test_assistant.py
├── main.py
├── requirements.txt
└── README.md
```

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> On Linux, PyAudio may need system packages (for example: `portaudio19-dev` and Python headers) before pip install succeeds.

## Run

### Voice mode (default)

## Run

```bash
python3 main.py
```

or

```bash
python3 main.py --mode voice
```

### CLI mode (text only)

```bash
python3 main.py --mode cli
```

## Example Commands
Then enter commands like:

- `add 20 and 22`
- `weather in delhi`
- `news`
- `browse github.com`
- `play relaxing piano`
- `open calculator`
- `exit`

## Notes

- If voice dependencies are missing, the assistant automatically falls back to CLI mode.
- You can later connect the weather skill to a live API for real forecasts.

Type `exit` to quit.

## Notes

- This rebuild is intentionally modular so you can extend it with speech recognition later.
- If you want full voice I/O, uncomment and install optional packages from `requirements.txt`.
