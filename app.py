import os
import telebot
from flask import Flask
from threading import Thread
import yt_dlp
import time

# 1. Получаем токен из настроек Render (у тебя там все верно)
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Project 640 IS ACTIVE"

# 2. Функция скачивания с использованием твоих куки
def download_video(url):
    # Имя файла в точности как на твоем скриншоте GitHub (image_c8eb86)
    COOKIE_FILE = 'www.youtube.com_cookies.txt' 
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'video.mp4',
        'cookiefile': COOKIE_FILE,
        'max_filesize': 48 * 1024 * 1024, # Лимит Telegram
        'quiet': False
    }
    
    try:
        if os.path.exists('video.mp4'):
            os.remove('video.mp4')
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return 'video.mp4'
    except Exception as e:
        print(f"Ошибка скачивания: {e}")
        return None

# 3. Обработка сообщений
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "Бот готов! Присылай ссылку на видео.")

@bot.message_handler(func=lambda m: "http" in m.text)
def handle_link(message):
    msg = bot.reply_to(message, "⏳ Начинаю загрузку через твои куки...")
    path = download_video(message.text)
    
    if path and os.path.exists(path):
        try:
            with open(path, 'rb') as video:
                bot.send_video(message.chat.id, video)
            os.remove(path)
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Ошибка отправки: {e}", message.chat.id, msg.message_id)
    else:
        bot.edit_message_text("❌ Не удалось скачать. Проверь размер видео или обнови файл куки в GitHub.", message.chat.id, msg.message_id)

# 4. Запуск сервера и анти-конфликт опрос
def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    Thread(target=run_flask).start()
    
    print("Бот запущен...")
    # Цикл с паузой помогает избежать ошибки 409 Conflict при перезагрузке Render
    while True:
        try:
            bot.polling(none_stop=True, interval=5)
        except Exception as e:
            print(f"Сбой: {e}")
            time.sleep(10)
