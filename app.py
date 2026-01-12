import os
import telebot
from flask import Flask
from threading import Thread

# Теперь код будет брать токен из настроек Render автоматически
TOKEN = os.getenv('8349153278:AAGP0SgBwqWZeY8cfw7Jf86My1MRkJSGd_8') 
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Project 640: Video Downloader is Active."

# Функция скачивания видео
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'max_filesize': 50 * 1024 * 1024, # Ограничение 50МБ для Telegram
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return 'video.mp4'

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "Проект 640 готов! Пришлите ссылку на видео (YouTube, VK, OK), и я попробую его скачать.")

@bot.message_handler(func=lambda m: "http" in m.text)
def handle_link(message):
    msg = bot.reply_to(message, "Начинаю загрузку видео, подождите...")
    try:
        video_path = download_video(message.text)
        with open(video_path, 'rb') as f:
            bot.send_video(message.chat.id, f)
        os.remove(video_path) # Удаляем файл после отправки
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"Ошибка при скачивании: {str(e)}", message.chat.id, msg.message_id)

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    Thread(target=run_web, daemon=True).start()
    print("SUCCESS: Downloader is starting...")
    bot.infinity_polling()
