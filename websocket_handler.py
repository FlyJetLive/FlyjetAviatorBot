import websocket
import json
import threading

def connect_websocket(on_crash_point):
    def on_message(ws, message):
        try:
            data = json.loads(message)
            if 'crashPoint' in data:
                crash_point = float(data['crashPoint'])
                on_crash_point(crash_point)
        except Exception as e:
            print(f"❌ Error in WebSocket message processing: {e}")

    def on_error(ws, error):
        print(f"❗ WebSocket Error: {error}")

    def on_close(ws, close_status_code, close_msg):
        print("🔌 WebSocket Closed. Reconnecting in 5 seconds...")
        threading.Timer(5, lambda: connect_websocket(on_crash_point)).start()

    def on_open(ws):
        print("✅ WebSocket Connected Successfully!")

    WEBSOCKET_URL = "wss://game9.apac.spribegaming.com/BlueBox/websocket"
    ws = websocket.WebSocketApp(
        WEBSOCKET_URL,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()
