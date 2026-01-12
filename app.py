import os
import telebot
from flask import Flask
from threading import Thread

# Берем токен из переменных окружения Render
TOKEN = os.getenv('8349153278:AAGP0SgBwqWZeY8cfw7Jf86My1MRkJSGd_8')

# Проверка токена в логах (выведет первые 5 символов для теста)
if TOKEN:
    print(f"Token found! Starts with: {TOKEN[:5]}...")
else:
    print("ERROR: BOT_TOKEN not found in Environment Variables!")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Project 640: Video Downloader is Active."

# Функция скачивания видео
def download_video(url):
    # Здесь ваш существующий код для yt_dlp
    pass 

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "Проект 640 готов! Пришлите ссылку на видео (YouTube, VK, OK), и я попробую его скачать.")

# Запуск Flask для Render (чтобы сервис не засыпал)
def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    print("Bot is polling...")
    bot.infinity_polling()
