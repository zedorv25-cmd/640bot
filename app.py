import os
import telebot
from flask import Flask
from threading import Thread
import yt_dlp

# Твой проверенный способ получения токена
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Project 640 IS FULLY ACTIVE"

# Функция для скачивания видео
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'max_filesize': 45 * 1024 * 1024, # Ограничение 45МБ для Telegram
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return 'video.mp4'
    except Exception as e:
        print(f"Download error: {e}")
        return None

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "Проект 640 готов! Пришли ссылку на видео, и я его скачаю.")

# Обработка ссылок
@bot.message_handler(func=lambda m: "http" in m.text)
def handle_link(message):
    msg = bot.reply_to(message, "Начинаю загрузку видео, подожди...")
    video_path = download_video(message.text)
    
    if video_path and os.path.exists(video_path):
        try:
            with open(video_path, 'rb') as video:
                bot.send_video(message.chat.id, video)
            os.remove(video_path) # Удаляем файл после отправки
        except Exception as e:
            bot.edit_message_text(f"Ошибка при отправке: {e}", message.chat.id, msg.message_id)
    else:
        bot.edit_message_text("Не удалось скачать видео. Возможно, оно слишком тяжелое или ссылка не поддерживается.", message.chat.id, msg.message_id)

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
