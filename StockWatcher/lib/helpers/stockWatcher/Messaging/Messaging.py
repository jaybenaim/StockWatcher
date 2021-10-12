# MESSAGING
import os

from StockWatcher.lib.helpers.stockWatcher.Messaging.twilio_notifications.middleware import (
    MessageClient,
)


class TwilioMessenger:

    def __init__(self):
        self.client = MessageClient()

    def send_message_to_admin(self, body):
        admin = self.client.administrators[0]["phone_number"]

        self.client.send_message(body, admin)

    def send_message_to_watcher(self, body, to):
        to = f"+1{to}"
        print(f"Sending message to {to}")

        if (
            to == os.environ["TWILIO_ADMINS_PHONE"]
            or to == os.environ["TWILIO_ADMINS_PHONE2"]
        ):
            self.client.send_message(body, to)
