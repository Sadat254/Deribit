import json
import ssl
import websocket
from websocket import create_connection, WebSocketConnectionClosedException
# import certif # I removed this unused import

class Deribitv2API:
    def __init__(self):
        self.msg = {
            "jsonrpc": "2.0",
            "method": "public/subscribe",
            "id": 42,
            "params": {
                "channels": ["quote.BTC-PERPETUAL"]
            }
        }
        self.list_of_notifications = []
        self.ws = None
        self.url = None

    def set_url(self, url):
        self.url = url

    def start_socket(self):
        while True:
            try:
                self.connect()
                self.listen()
            except WebSocketConnectionClosedException:
                self.end_socket_due_to_error("WebSocket connection closed")
            except Exception as e:
                self.end_socket_due_to_error(e)

    def connect(self):
        try:
            self.ws = create_connection(self.url, sslopt={"cert_reqs": ssl.CERT_NONE})
            if not self.ws:
                raise Exception("WebSocket connection failed")
            self.ws.send(json.dumps(self.msg))
        except WebSocketConnectionClosedException:
            self.end_socket_due_to_error("WebSocket connection closed")
        except Exception as e:
            self.end_socket_due_to_error(e)

    def listen(self):
        while True:
            try:
                data = self.ws.recv()
                self.list_of_notifications.append(json.loads(data))
            except WebSocketConnectionClosedException:
                self.end_socket_due_to_error("WebSocket connection closed")
            except Exception as e:
                self.end_socket_due_to_error(e)
                break

    def disconnect(self):
        if self.ws and self.ws.connected:
            self.ws.close()
        print("Socket Closed")

    def end_socket_due_to_error(self, e):
        print(f"Error: {e}. Closing websocket.")
        self.disconnect()

    def get_list_of_data(self):
        if len(self.list_of_notifications) > 1:
            self.list_of_notifications = self.list_of_notifications[-2:]
            return self.list_of_notifications[-1]
        return None

    def get_latest_notification(self):
        if len(self.list_of_notifications) > 0:
            return self.list_of_notifications[-1]
        return None

    def request(self, msg):
        ws = create_connection(self.url, sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.send(json.dumps(msg))
        response = json.loads(ws.recv())
        ws.close()
        return response