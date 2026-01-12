import os
import telebot
from flask import Flask
from threading import Thread
import yt_dlp

# Получаем токен из переменных окружения Render
TOKEN = os.getenv('8349153278:AAGP0SgBwqWZeY8cfw7Jf86My1MRkJSGd_8')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Project 640 is running!"

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'max_filesize': 50 * 1024 * 1024,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return 'video.mp4'
    except Exception as e:
        print(f"Error: {e}")
        return None

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "Проект 640 готов! Пришлите ссылку на видео.")

@bot.message_handler(func=lambda m: "http" in m.text)
def handle_link(message):
    bot.reply_to(message, "Скачиваю...")
    path = download_video(message.text)
    if path:
        with open(path, 'rb') as v:
            bot.send_video(message.chat.id, v)
        os.remove(path)
    else:
        bot.reply_to(message, "Ошибка загрузки.")

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    Thread(target=run).start()
    print("Bot started...")
    bot.infinity_polling()
