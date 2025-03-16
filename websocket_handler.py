import websocket
import json
import threading

def connect_websocket(send_signals_to_users):
    ws_url = "wss://game9.apac.spribegaming.com/BlueBox/websocket"

    def on_message(ws, message):
        try:
            data = json.loads(message)
            crash_point = data.get("crash_point")  # Example data extraction logic
            if crash_point:
                send_signals_to_users(crash_point)
        except Exception as e:
            print(f"Error processing WebSocket message: {e}")

    def on_error(ws, error):
        print(f"WebSocket error: {error}")

    def on_close(ws, close_status_code, close_msg):
        print("WebSocket closed. Reconnecting in 5 seconds...")
        threading.Timer(5, lambda: connect_websocket(send_signals_to_users)).start()

    def on_open(ws):
        print("WebSocket connection established.")

    ws = websocket.WebSocketApp(
        ws_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

