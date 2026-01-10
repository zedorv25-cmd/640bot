import os
import telebot
from flask import Flask
from threading import Thread

# 1. Безопасное получение токена
# Убедитесь, что в Render переменная называется именно BOT_TOKEN
TOKEN = os.environ.get('8349153278:AAEz5jx0uavBacPJI6zaz7KCO8-mQsnV8Ck')

# Проверка на наличие токена, чтобы избежать ошибки "NoneType"
if not TOKEN:
    print("CRITICAL ERROR: BOT_TOKEN is not set in Environment Variables!")
    bot = None
else:
    bot = telebot.TeleBot(TOKEN)

# 2. Настройка Flask (нужна для Render, чтобы сервис был "Live")
app = Flask(__name__)

@app.route('/')
def home():
    return "Project 640 Status: Running"

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    # Render требует порт 10000 для Free тарифа
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 3. Логика Telegram бота
if bot:
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "Проект 640 запущен! Бот успешно прошел все этапы деплоя.")

    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        bot.reply_to(message, f"Получено сообщение: {message.text}")

# 4. Запуск приложения
if __name__ == "__main__":
    # Запускаем Flask в отдельном потоке
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    if bot:
        print("Starting bot polling...")
        # infinity_polling автоматически перезапускается при временных сбоях сети
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    else:
        # Если бота нет, просто держим поток Flask живым
        flask_thread.join()
