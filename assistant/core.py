"""Main assistant runtime and command router."""

from __future__ import annotations

from dataclasses import dataclass

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

        return SkillResult(
            False,
            "I can help with arithmetic, weather, headlines, browsing, playing music, and opening apps.",
        )

    def run_cli(self) -> None:
        print("Virtual Voice Assistant is running in CLI mode. Type 'exit' to quit.")
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("Assistant: Goodbye!")
                break

            result = self.handle(user_input)
            print(f"Assistant: {result.message}")

    def run_voice(self) -> None:
        voice = VoiceInterface()
        if not voice.status.ready:
            print(f"Voice mode unavailable: {voice.status.message}")
            print("Falling back to CLI mode.")
            self.run_cli()
            return

        voice.speak("Virtual Voice Assistant is running in voice mode. Say exit to stop.")

        while True:
            heard = voice.listen()
            if not heard:
                continue

            if heard.lower() in {"exit", "quit", "stop"}:
                voice.speak("Goodbye!")
                break

            result = self.handle(heard)
            voice.speak(result.message)
