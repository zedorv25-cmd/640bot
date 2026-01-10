import os
import telebot
from flask import Flask
from threading import Thread

# 1. Получаем токен из переменных окружения (Environment Variables)
TOKEN = os.getenv('8349153278:AAER_oCh59Z0EIDK8P-WTlSlqx6AATa_F2E')
bot = telebot.TeleBot(TOKEN)

# 2. Создаем мини-сервер, чтобы Render был доволен
app = Flask(__name__)

@app.route('/')
def index():
    return "Бот проекта 640 запущен и работает!"

def run_web_server():
    # Render автоматически подставляет порт 10000
    app.run(host='0.0.0.0', port=10000)

# 3. Основная логика бота
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Привет! Проект 640 на связи. Бот успешно запущен на Render.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Вы сказали: {message.text}")

# 4. Запуск
if __name__ == "__main__":
    # Запускаем веб-сервер в отдельном потоке
    Thread(target=run_web_server).start()
    # Запускаем бота
    print("Бот начинает опрос (polling)...")
    bot.infinity_polling()
