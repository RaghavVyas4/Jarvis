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


if __name__ == "__main__":
    unittest.main()
