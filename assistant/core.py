"""Main assistant runtime and command router."""

from __future__ import annotations

import getpass
import os
from dataclasses import dataclass
from typing import Callable

from .skills import SkillResult, SkillSet
from .voice import VoiceInterface


@dataclass
class ParsedCommand:
    intent: str
    payload: str = ""


class VirtualVoiceAssistant:
    """Simple assistant with CLI and voice I/O modes."""

    def __init__(self) -> None:
        self.skills = SkillSet()

    def parse_command(self, command: str) -> ParsedCommand:
        text = command.strip().lower()

        if any(word in text for word in ("add", "subtract", "multiply", "divide", "plus", "minus", "times")):
            return ParsedCommand("arithmetic", command)
        if "weather" in text:
            city = text.replace("weather", "").replace("in", "").strip() or "your city"
            return ParsedCommand("weather", city)
        if "news" in text or "headline" in text:
            return ParsedCommand("news")
        if text.startswith("open "):
            return ParsedCommand("open_app", text.removeprefix("open ").strip())
        if text.startswith("browse "):
            return ParsedCommand("browse", text.removeprefix("browse ").strip())
        if text.startswith("play "):
            return ParsedCommand("music", text.removeprefix("play ").strip())
        if "send email" in text or "send mail" in text or text == "email":
            return ParsedCommand("email")
        return ParsedCommand("unknown", command)

    def handle(self, command: str) -> SkillResult:
        parsed = self.parse_command(command)

        if parsed.intent == "arithmetic":
            return self.skills.arithmetic(parsed.payload)
        if parsed.intent == "weather":
            return self.skills.weather_forecast(parsed.payload)
        if parsed.intent == "news":
            return self.skills.read_headlines()
        if parsed.intent == "open_app":
            return self.skills.open_application(parsed.payload)
        if parsed.intent == "browse":
            return self.skills.browse(parsed.payload)
        if parsed.intent == "music":
            return self.skills.play_music(parsed.payload)
        if parsed.intent == "email":
            return SkillResult(True, "Starting email workflow.")

        return SkillResult(
            False,
            "I can help with arithmetic, weather, headlines, browsing, playing music, opening apps, and sending emails.",
        )

    def _send_email_interactive(self, ask: Callable[[str, bool], str | None]) -> SkillResult:
        smtp_server = ask("SMTP server", False) or ""
        port_text = ask("SMTP port", False) or ""
        username = ask("Email username", False) or ""
        password = ask("Email password", True) or ""
        receiver = ask("Recipient email", False) or ""
        subject = ask("Email subject", False) or ""
        body = ask("Email body", False) or ""

        if not all([smtp_server, port_text, username, password, receiver, subject, body]):
            return SkillResult(False, "Email cancelled because one or more required fields were empty.")

        try:
            port = int(port_text)
        except ValueError:
            return SkillResult(False, "SMTP port must be a valid number.")

        return self.skills.send_mail(
            smtp_server=smtp_server,
            port=port,
            username=username,
            password=password,
            to=receiver,
            subject=subject,
            body=body,
        )

    def _cli_ask(self, prompt: str, is_secret: bool) -> str | None:
        if is_secret:
            return getpass.getpass(f"{prompt}: ").strip()
        return input(f"{prompt}: ").strip()

    def run_cli(self) -> None:
        print("Virtual Voice Assistant is running in CLI mode. Type 'exit' to quit.")
        print("Tip: type 'send email' to start the email workflow.")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("Assistant: Goodbye!")
                break

            parsed = self.parse_command(user_input)
            if parsed.intent == "email":
                result = self._send_email_interactive(self._cli_ask)
            else:
                result = self.handle(user_input)
            print(f"Assistant: {result.message}")

    def run_voice(self) -> None:
        voice = VoiceInterface()
        if not voice.status.ready:
            print(f"Voice mode unavailable: {voice.status.message}")
            print("Falling back to CLI mode.")
            self.run_cli()
            return

        def voice_ask(prompt: str, _is_secret: bool) -> str | None:
            voice.speak(f"Please say {prompt}.")
            return voice.listen()

        voice.speak("Virtual Voice Assistant is running in voice mode. Say exit to stop.")
        voice.speak("Say send email to compose and send an email.")

        while True:
            heard = voice.listen()
            if not heard:
                continue

            if heard.lower() in {"exit", "quit", "stop"}:
                voice.speak("Goodbye!")
                break

            parsed = self.parse_command(heard)
            if parsed.intent == "email":
                if not os.getenv("ALLOW_VOICE_EMAIL_PASSWORD"):
                    voice.speak(
                        "For safety, set ALLOW_VOICE_EMAIL_PASSWORD=1 before sharing passwords in voice mode."
                    )
                    continue
                result = self._send_email_interactive(voice_ask)
            else:
                result = self.handle(heard)
            voice.speak(result.message)
