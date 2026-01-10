import telebot
import yt_dlp
import os
import threading
from flask import Flask

# Берем токен из настроек Render (сделаем это позже)
TOKEN = os.getenv('BOT_TOKEN', '8202704612:AAHrRai4R9yYJ8LxD4QNgwehS0o91w96FdI')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "640bot is running!"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🚀 Проект 640 успешно запущен на Render!")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    if "youtu" in message.text:
        bot.reply_to(message, "⏳ Обрабатываю видео...")
        # Тут будет логика скачивания
    else:
        bot.reply_to(message, "Пришли мне ссылку на YouTube!")

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # Запуск бота в отдельном потоке
    threading.Thread(target=run_bot, daemon=True).start()
    # Запуск веб-сервера (обязательно порт 10000 для Render)
    app.run(host='0.0.0.0', port=10000)
