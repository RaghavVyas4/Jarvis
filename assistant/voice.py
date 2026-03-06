"""Voice input/output helpers for the Virtual Voice Assistant."""

from __future__ import annotations

import importlib
import importlib.util
from dataclasses import dataclass


@dataclass
class VoiceStatus:
    ready: bool
    message: str


class VoiceInterface:
    """Provides speech-to-text and text-to-speech with graceful fallbacks."""

    def __init__(self) -> None:
        self._speech_module = None
        self._tts_module = None
        self._recognizer = None
        self._microphone = None
        self._engine = None
        self.status = self._bootstrap()

    def _bootstrap(self) -> VoiceStatus:
        has_stt = importlib.util.find_spec("speech_recognition") is not None
        has_tts = importlib.util.find_spec("pyttsx3") is not None

        if not has_stt and not has_tts:
            return VoiceStatus(False, "Voice packages are missing. Install dependencies from requirements.txt.")
        if not has_stt:
            return VoiceStatus(False, "speech_recognition is missing. Install dependencies from requirements.txt.")
        if not has_tts:
            return VoiceStatus(False, "pyttsx3 is missing. Install dependencies from requirements.txt.")

        self._speech_module = importlib.import_module("speech_recognition")
        self._tts_module = importlib.import_module("pyttsx3")

        self._recognizer = self._speech_module.Recognizer()
        self._microphone = self._speech_module.Microphone()
        self._engine = self._tts_module.init()
        self._engine.setProperty("rate", 170)

        return VoiceStatus(True, "Voice system initialized.")

    def speak(self, text: str) -> None:
        print(f"Assistant: {text}")
        if not self.status.ready:
            return

        self._engine.say(text)
        self._engine.runAndWait()

    def listen(self) -> str | None:
        if not self.status.ready:
            return None

        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(source, duration=0.4)
            print("Listening...")
            try:
                audio = self._recognizer.listen(source, timeout=6, phrase_time_limit=8)
            except self._speech_module.WaitTimeoutError:
                return None

        try:
            heard = self._recognizer.recognize_google(audio)
            print(f"You (voice): {heard}")
            return heard.strip()
        except self._speech_module.UnknownValueError:
            self.speak("Sorry, I did not catch that.")
        except self._speech_module.RequestError:
            self.speak("Speech service is unavailable right now.")

        return None
