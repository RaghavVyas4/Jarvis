# Virtual Voice Assistant (Python)

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
│   └── skills.py
├── tests/
│   └── test_assistant.py
├── main.py
├── requirements.txt
└── README.md
```

## Run

```bash
python3 main.py
```

Then enter commands like:

- `add 20 and 22`
- `weather in delhi`
- `news`
- `browse github.com`
- `play relaxing piano`
- `open calculator`

Type `exit` to quit.

## Notes

- This rebuild is intentionally modular so you can extend it with speech recognition later.
- If you want full voice I/O, uncomment and install optional packages from `requirements.txt`.
