# MESSAGING


from StockWatcher.lib.helpers.stockWatcher.Messaging.twilio_notifications.middleware import (
    MessageClient,
    load_twilio_config,
)

client = MessageClient()


class TwilioMessenger:
    def send_message_to_admin(self, body):
        admin = client.administrators[0]["phone_number"]

        client.send_message(body, admin)

    def send_message_to_watcher(self, body, to):
        client.send_message(body, f"+1{to}")
