import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from assistant.core import VirtualVoiceAssistant


class AssistantTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assistant = VirtualVoiceAssistant()

    def test_arithmetic_add(self):
        result = self.assistant.handle("add 7 and 5")
        self.assertTrue(result.success)
        self.assertIn("12", result.message)

    def test_weather_intent(self):
        result = self.assistant.handle("weather in mumbai")
        self.assertTrue(result.success)
        self.assertIn("Mumbai", result.message)

    def test_unknown_intent(self):
        result = self.assistant.handle("write my assignment")
        self.assertFalse(result.success)

    @patch("builtins.input", side_effect=["quit"])
    @patch("assistant.core.VoiceInterface")
    def test_voice_mode_falls_back_to_cli_when_unavailable(self, mock_voice, _mock_input):
        mock_voice.return_value.status.ready = False
        mock_voice.return_value.status.message = "missing deps"

        stream = io.StringIO()
        with redirect_stdout(stream):
            self.assistant.run_voice()

        output = stream.getvalue()
        self.assertIn("Voice mode unavailable", output)
        self.assertIn("CLI mode", output)


if __name__ == "__main__":
    unittest.main()
