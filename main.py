import os
import httpx
from time import sleep
from random import choice


REPLIES = [
    "Please, abstain from sending voices",
    "We don't like voice messages here",
    "Unfortunately, nobody will listen to it",
    "Keep your voices to yourself",
    "Text is always better",
    "Show some respect and write it down",
]


class TelegramClient:
    API_URL = "https://api.telegram.org"

    def __init__(self, token):
        self.token = token
        self.api_url_full = f"{self.API_URL}/bot{self.token}"

    def get_messages(self, offset):
        r = httpx.post(
            f"{self.api_url_full}/getUpdates",
            data={"allowed_updates": ["message"], "offset": offset},
        )
        response = r.json()

        if not response["ok"]:
            print(response["error_code"], response["description"])
            return []
        return response["result"]

    def send_messages(self, chat_id, text, reply_to_message_id=None):
        httpx.post(
            f"{self.api_url_full}/sendMessage",
            data={
                "chat_id": chat_id,
                "text": choice(REPLIES),
                "reply_to_message_id": reply_to_message_id,
            },
        )


def request(client, last_update_id):
    offset = 0

    if last_update_id:
        offset = last_update_id + 1

    messages = client.get_messages(offset)

    for message in messages:
        last_update_id = message["update_id"]
        message = message.get("message", None)

        if message and "voice" in message:
            chat_id = message["chat"]["id"]
            reply_to_message_id = message["message_id"]

            client.send_messages(chat_id, choice(REPLIES), reply_to_message_id)

    return last_update_id


def main():
    token = os.environ.get("API_TOKEN", None)

    if not token:
        print("error: Telegram API token (API_TOKEN) is required")
        exit(1)

    last_update_id = 0
    client = TelegramClient(token)

    while True:
        try:
            last_update_id = request(client, last_update_id)
        except httpx.RequestError:
            pass
        sleep(2)


if __name__ == "__main__":
    main()
