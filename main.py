import httpx
from time import sleep

import os

API_URL = "https://api.telegram.org"
API_TOKEN = os.environ.get("API_TOKEN", None)
API_URL_FULL = f"{API_URL}/bot{API_TOKEN}"


def handle_message(message):
    chat_id = message["chat"]["id"]
    httpx.post(
        f"{API_URL_FULL}/sendMessage", data={"chat_id": chat_id, "text": "fuck you"}
    )


def request(last_update_id):
    offset = 0

    if last_update_id:
        offset = last_update_id + 1

    r = httpx.get(
        f"{API_URL_FULL}/getUpdates",
        params={"allowed_updates": ["message"], "offset": offset},
    )

    # Deserialization. Transforms the text from response's body into a list of dictionaries
    response = r.json()
    updates = response["result"]

    for update in updates:
        last_update_id = update["update_id"]
        message = update["message"]

        if "voice" in message:
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
