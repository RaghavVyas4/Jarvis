"""Skill handlers for the Virtual Voice Assistant."""

from __future__ import annotations

import datetime as _dt
import math
import operator
import os
import smtplib
import ssl
import subprocess
import webbrowser
from dataclasses import dataclass
from email.message import EmailMessage
from typing import Callable


@dataclass
class SkillResult:
    success: bool
    message: str


class SkillSet:
    """Collection of task automation helpers used by the assistant."""

    OPERATIONS: dict[str, Callable[[float, float], float]] = {
        "add": operator.add,
        "plus": operator.add,
        "sum": operator.add,
        "subtract": operator.sub,
        "minus": operator.sub,
        "multiply": operator.mul,
        "times": operator.mul,
        "divide": operator.truediv,
        "power": operator.pow,
    }
    SMTP_SECURITY_MODES = {"auto", "starttls", "ssl", "none"}

    def _normalize_security_mode(self, security: str) -> str | None:
        mode = security.strip().lower()
        if mode in self.SMTP_SECURITY_MODES:
            return mode
        return None

    def arithmetic(self, expression: str) -> SkillResult:
        """Solve simple arithmetic commands like 'add 3 and 4'."""
        tokens = expression.lower().replace("?", "").split()
        if len(tokens) < 3:
            return SkillResult(False, "Please provide enough terms for a calculation.")

        op_key = next((token for token in tokens if token in self.OPERATIONS), None)
        if not op_key:
            return SkillResult(False, "I couldn't find a supported arithmetic operation.")

        numbers: list[float] = []
        for token in tokens:
            try:
                numbers.append(float(token))
            except ValueError:
                continue

        if len(numbers) < 2:
            return SkillResult(False, "Please provide at least two numbers.")

        a, b = numbers[0], numbers[1]
        if op_key == "divide" and math.isclose(b, 0.0):
            return SkillResult(False, "Division by zero is not allowed.")

        result = self.OPERATIONS[op_key](a, b)
        return SkillResult(True, f"The result is {result:g}.")

    def weather_forecast(self, city: str) -> SkillResult:
        """Mock weather forecast that can be replaced with a live API call later."""
        now = _dt.datetime.now().strftime("%A")
        message = (
            f"Forecast for {city.title()} on {now}: partly cloudy, 27°C, "
            "and a 20% chance of rain."
        )
        return SkillResult(True, message)

    def read_headlines(self) -> SkillResult:
        """Open a news site and report completion."""
        webbrowser.open("https://news.google.com")
        return SkillResult(True, "Opened the latest headlines in your browser.")

    def browse(self, url: str) -> SkillResult:
        """Open any website."""
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        webbrowser.open(url)
        return SkillResult(True, f"Opening {url}.")

    def play_music(self, query: str = "lofi") -> SkillResult:
        """Play music on YouTube using the default browser."""
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        return SkillResult(True, f"Playing music for '{query}'.")

    def open_application(self, app_name: str) -> SkillResult:
        """Open common applications by shelling out to the OS."""
        try:
            if os.name == "nt":
                subprocess.Popen(["start", app_name], shell=True)
            elif os.uname().sysname == "Darwin":
                subprocess.Popen(["open", "-a", app_name])
            else:
                subprocess.Popen([app_name])
        except Exception as exc:
            return SkillResult(False, f"Couldn't open {app_name}: {exc}")

        return SkillResult(True, f"Opening {app_name}.")

    def send_mail(
        self,
        smtp_server: str,
        port: int,
        username: str,
        password: str,
        to: str,
        subject: str,
        body: str,
        security: str = "auto",
    ) -> SkillResult:
        """Send an email via SMTP.

        security values: auto, starttls, ssl, none.
        """
        mode = self._normalize_security_mode(security)
        if mode is None:
            valid = ", ".join(sorted(self.SMTP_SECURITY_MODES))
            return SkillResult(False, f"SMTP security must be one of: {valid}.")

        msg = EmailMessage()
        msg["From"] = username
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)

        context = ssl.create_default_context()

        try:
            if mode == "ssl" or (mode == "auto" and port == 465):
                with smtplib.SMTP_SSL(smtp_server, port, timeout=15, context=context) as server:
                    server.login(username, password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(smtp_server, port, timeout=15) as server:
                    server.ehlo()
                    if mode == "starttls" or (mode == "auto" and port != 25):
                        server.starttls(context=context)
                        server.ehlo()
                    server.login(username, password)
                    server.send_message(msg)
        except Exception as exc:
            return SkillResult(False, f"Failed to send email ({mode} mode): {exc}")

        return SkillResult(True, f"Email sent successfully to {to}.")
