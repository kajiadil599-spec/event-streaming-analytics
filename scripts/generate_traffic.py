import requests
import time
import random

API_URL = "http://127.0.0.1:8000/api/v1/events"
CLIENTS = ["mobile_app_ios", "web_portal_v2", "iot_sensor_alpha", "spammer_bot"]
EVENT_TYPES = ["page_view", "button_click", "checkout_init", "error_log"]

print("🚀 Starting real-time traffic generator... Press Ctrl+C to stop.")

while True:
    client_id = random.choices(CLIENTS, weights=[40, 40, 15, 5])[0]
    
    # If it's the spammer bot, send a rapid burst to trigger rate limiting
    burst_count = 15 if client_id == "spammer_bot" else 1

    for _ in range(burst_count):
        payload = {
            "client_id": client_id,
            "event_type": random.choice(EVENT_TYPES),
            "payload": {"latency_ms": random.randint(10, 250), "session_id": str(random.randint(1000, 9999))}
        }
        try:
            res = requests.post(API_URL, json=payload)
            if res.status_code == 202:
                print(f"✅ [202 ACCEPTED] Event ingested for {client_id}")
            elif res.status_code == 429:
                print(f"⚠️ [429 RATE LIMITED] Blocked excess burst from {client_id}")
        except Exception as e:
            print(f"❌ Connection error: {e}")

    time.sleep(random.uniform(0.1, 0.5))
