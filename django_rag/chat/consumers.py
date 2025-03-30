from typing import Dict
from channels.generic.websocket import JsonWebsocketConsumer


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def receive_json(self, request_data: Dict):
        message = request_data.get("message", "")

        response_obj = {"message": f"received {message}"}
        self.send_json(response_obj)
