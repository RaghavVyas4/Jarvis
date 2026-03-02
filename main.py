"""Entry point for Virtual Voice Assistant."""

from assistant import VirtualVoiceAssistant


if __name__ == "__main__":
    assistant = VirtualVoiceAssistant()
    assistant.run_cli()
