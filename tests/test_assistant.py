import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from assistant.core import VirtualVoiceAssistant
from assistant.skills import SkillSet
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
            "starttls",
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
            security="starttls",
        )

    @patch("assistant.skills.smtplib.SMTP")
    def test_send_mail_starttls_mode(self, mock_smtp):
        skills = SkillSet()
        result = skills.send_mail(
            smtp_server="smtp.example.com",
            port=587,
            username="sender@example.com",
            password="secret",
            to="to@example.com",
            subject="Hello",
            body="Body",
            security="starttls",
        )

        self.assertTrue(result.success)
        smtp_instance = mock_smtp.return_value.__enter__.return_value
        smtp_instance.starttls.assert_called_once()
        smtp_instance.login.assert_called_once_with("sender@example.com", "secret")
        smtp_instance.send_message.assert_called_once()

    @patch("assistant.skills.smtplib.SMTP_SSL")
    def test_send_mail_ssl_mode(self, mock_smtp_ssl):
        skills = SkillSet()
        result = skills.send_mail(
            smtp_server="smtp.example.com",
            port=465,
            username="sender@example.com",
            password="secret",
            to="to@example.com",
            subject="Hello",
            body="Body",
            security="ssl",
        )

        self.assertTrue(result.success)
        smtp_instance = mock_smtp_ssl.return_value.__enter__.return_value
        smtp_instance.login.assert_called_once_with("sender@example.com", "secret")
        smtp_instance.send_message.assert_called_once()

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
