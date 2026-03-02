"""Entry point for Virtual Voice Assistant."""

from __future__ import annotations

import argparse

from assistant import VirtualVoiceAssistant


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Virtual Voice Assistant")
    parser.add_argument(
        "--mode",
        choices=["cli", "voice"],
        default="voice",
        help="Run assistant in text CLI or microphone/speaker voice mode.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    assistant = VirtualVoiceAssistant()
    if args.mode == "voice":
        assistant.run_voice()
    else:
        assistant.run_cli()
from assistant import VirtualVoiceAssistant


if __name__ == "__main__":
    assistant = VirtualVoiceAssistant()
    assistant.run_cli()
