"""Telegram Notifier - sends alerts via Telegram Bot API.

Uses the Icculus/openclaw bot to send messages.
Bot token should be in environment variable TELEGRAM_BOT_TOKEN.
Chat ID should be in environment variable TELEGRAM_CHAT_ID.
"""

import os
import json
import urllib.request
import urllib.error
from typing import Optional


def send_telegram_message(
    text: str,
    bot_token: Optional[str] = None,
    chat_id: Optional[str] = None,
    parse_mode: str = "HTML",
) -> bool:
    """Send a message via Telegram Bot API.

    Args:
        text: Message text (supports HTML formatting)
        bot_token: Bot API token (defaults to TELEGRAM_BOT_TOKEN env var)
        chat_id: Target chat ID (defaults to TELEGRAM_CHAT_ID env var)
        parse_mode: "HTML" or "Markdown"

    Returns:
        True if sent successfully, False otherwise
    """
    token = bot_token or os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat = chat_id or os.environ.get("TELEGRAM_CHAT_ID", "")

    if not token or not chat:
        print("Warning: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat,
        "text": text,
        "parse_mode": parse_mode,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            return result.get("ok", False)
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"Telegram send failed: {e}")
        return False


def send_job_alert(company: str, title: str, score: float, url: str = "") -> bool:
    """Send a high-score job alert via Telegram."""
    msg = (
        f"🎯 <b>Hot Job Match ({score:.0f}%)</b>\n\n"
        f"<b>{title}</b> at <b>{company}</b>\n"
    )
    if url:
        msg += f"\n<a href=\"{url}\">View Job</a>"
    return send_telegram_message(msg)


def send_response_alert(company: str, subject: str, sender: str) -> bool:
    """Send a company response alert via Telegram."""
    msg = (
        f"📬 <b>Response from {company}!</b>\n\n"
        f"Subject: {subject}\n"
        f"From: {sender}\n\n"
        f"Check Gmail and take action."
    )
    return send_telegram_message(msg)
