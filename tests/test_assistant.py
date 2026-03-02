import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
import unittest

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

    def test_email_intent_parse(self):
        parsed = self.assistant.parse_command("send email")
        self.assertEqual(parsed.intent, "email")

    def test_email_workflow_calls_send_mail(self):
        responses = iter([
            "smtp.example.com",
            "587",
            "sender@example.com",
            "secret",
            "to@example.com",
            "Project Update",
            "Hello from assistant",
        ])

        def fake_ask(_prompt: str, _is_secret: bool) -> str | None:
            return next(responses)

        with patch.object(self.assistant.skills, "send_mail") as mock_send_mail:
            mock_send_mail.return_value.success = True
            mock_send_mail.return_value.message = "Email sent successfully."
            result = self.assistant._send_email_interactive(fake_ask)

        self.assertTrue(result.success)
        mock_send_mail.assert_called_once_with(
            smtp_server="smtp.example.com",
            port=587,
            username="sender@example.com",
            password="secret",
            to="to@example.com",
            subject="Project Update",
            body="Hello from assistant",
        )

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
