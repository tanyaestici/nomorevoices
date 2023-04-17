import os
import httpx
from time import sleep
from random import choice

API_URL = "https://api.telegram.org"
API_TOKEN = os.environ.get("API_TOKEN", None)
API_URL_FULL = f"{API_URL}/bot{API_TOKEN}"

REPLIES = [
    "Please, abstain from sending voices",
    "We don't like voice messages here",
    "Unfortunately, nobody will listen to it",
    "Keep your voices to yourself",
    "Text is always better",
    "Show some respect and write it down",
]


def handle_message(message):
    chat_id = message["chat"]["id"]
    reply_to_id = message["message_id"]

    httpx.post(
        f"{API_URL_FULL}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": choice(REPLIES),
            "reply_to_message_id": reply_to_id,
        },
    )


def request(last_update_id):
    offset = 0

    if last_update_id:
        offset = last_update_id + 1

    r = httpx.get(
        f"{API_URL_FULL}/getUpdates",
        params={"allowed_updates": ["message"], "offset": offset},
    )

    response = r.json()
    updates = response["result"]

    for update in updates:
        last_update_id = update["update_id"]
        message = update.get("message", None)

        if message and "voice" in message:
            handle_message(message)

    return last_update_id


def main():
    if not API_TOKEN:
        print("error: Telegram API token (API_TOKEN) is required")
        exit(1)

    last_update_id = 0

    while True:
        try:
            last_update_id = request(last_update_id)
        except httpx.RequestError:
            pass
        sleep(2)


if __name__ == "__main__":
    main()
