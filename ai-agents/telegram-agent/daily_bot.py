import requests
import random
import datetime

# ---------------- CONFIG ---------------- #

BOT_TOKEN = "<TelegramBotToken>"
CHAT_ID = "1209913841"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:1.5b"

# ---------------- AI CONTENT ---------------- #

def generate_tip():

    prompt = f"""
You are a senior QA mentor.

Generate ONE short daily QA learning message.
Rotate between:
- QA tip
- Automation best practice
- API testing insight
- Test design concept
- Motivational quote for QA engineers

Keep it under 120 words.
Make it practical.
Do not use markdown.
Today is {datetime.date.today()}.
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=120
    )

    data = response.json()
    return data.get("response", "Keep learning every day!")

# ---------------- TELEGRAM SEND ---------------- #

def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    requests.post(url, data=payload)

# ---------------- MAIN ---------------- #

if __name__ == "__main__":

    print("Generating QA tip...")
    message = generate_tip()

    print("Sending to Telegram...")
    send_message(message)

    print("Done.")
