import os
import telebot
from flask import Flask
from threading import Thread
import yt_dlp

# 1. Получаем токен из переменных окружения Render
TOKEN = os.getenv('8349153278:AAGP0SgBwqWZeY8cfw7Jf86My1MRkJSGd_8')

# Проверка наличия токена в логах для диагностики
if not TOKEN:
    print("CRITICAL ERROR: BOT_TOKEN is not set in Render Environment Variables!")
else:
    print(f"Token received successfully! Bot is starting...")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Project 640: Video Downloader is Active."

# 2. Функция скачивания видео
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'max_filesize': 50 * 1024 * 1024,  # Ограничение 50МБ для Telegram
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return 'video.mp4'
    except Exception as e:
        print(f"Download error: {e}")
        return None

# 3. Обработчики команд
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "Проект 640 готов! Пришлите ссылку на видео (YouTube, VK, OK), и я попробую его скачать.")

@bot.message_handler(func=lambda m: "http" in m.text)
def handle_link(message):
    msg = bot.reply_to(message, "Начинаю загрузку видео, подождите...")
    try:
        video_path = download_video(message.text)
        if video_path and os.path.exists(video_path):
            with open(video_path, 'rb') as video:
                bot.send_video(message.chat.id, video)
            os.remove(video_path) # Удаляем файл после отправки
        else:
            bot.edit_message_text("Не удалось скачать видео. Проверьте ссылку.", message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"Произошла ошибка: {e}", message.chat.id, msg.message_id)

# 4. Настройка Flask для Render (Keep-alive)
def run():
    # Render передает порт в переменной PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    print("Bot is polling...")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Polling error: {e}")
