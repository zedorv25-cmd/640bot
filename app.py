import os
import telebot
from flask import Flask
from threading import Thread

# 1. Получение токена с защитой от NoneType
# В логах была ошибка TypeError: 'NoneType' object is not iterable, 
# потому что TOKEN был пуст. Теперь мы это проверяем.
TOKEN = '8349153278:AAEz5jx0uavBacPJi6zaz7KC08-mQsnV8Ck'

def create_bot():
    if not TOKEN:
        # Эта надпись появится в логах Render красным, если переменная не подхватится
        print("!!! CRITICAL ERROR: BOT_TOKEN is missing in Environment Variables !!!")
        return None
    try:
        return telebot.TeleBot(TOKEN)
    except Exception as e:
        print(f"!!! Error initializing bot: {e} !!!")
        return None

bot = create_bot()

# 2. Flask-сервер для "обмана" Render
# Render ожидает активность на порту, иначе считает сервис упавшим.
app = Flask(__name__)

@app.route('/')
def index():
    return "640bot is Live. Web server is active."

def run_web():
    # Используем порт 10000, который требует Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 3. Обработчики команд бота
if bot:
    @bot.message_handler(commands=['start'])
    def start_cmd(message):
        bot.reply_to(message, "Проект 640: Система запущена и работает корректно!")

    @bot.message_handler(func=lambda m: True)
    def echo_msg(message):
        bot.reply_to(message, f"Бот на связи! Вы написали: {message.text}")

# 4. Запуск всего вместе
if __name__ == "__main__":
    # Запускаем веб-сервер в отдельном потоке, чтобы он не мешал боту
    web_thread = Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()
    
    if bot:
        print("Bot is starting polling...")
        # infinity_polling устойчив к временным разрывам связи
        bot.infinity_polling(timeout=20, long_polling_timeout=10)
    else:
        print("Bot failed to start due to missing token.")
        # Оставляем поток живым, чтобы Render не перезагружал сервис мгновенно
        web_thread.join()
