import os
import telebot
from flask import Flask
from threading import Thread
import yt_dlp
import time

# 1. Настройка доступа
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Project 640 IS FULLY OPERATIONAL"

# 2. Функция скачивания
def download_video(url):
    # Имя файла в точности как на твоем скриншоте из GitHub
    COOKIE_FILE = 'www.youtube.com_cookies.txt' 
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'video_mp4_file.mp4',
        'cookiefile': COOKIE_FILE,
        'max_filesize': 48 * 1024 * 1024, # Лимит 48 Мб
        'quiet': False,
        'no_warnings': False
    }
    
    try:
        # Очистка перед загрузкой
        if os.path.exists('video_mp4_file.mp4'):
            os.remove('video_mp4_file.mp4')
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return 'video_mp4_file.mp4'
    except Exception as e:
        print(f"Ошибка скачивания через yt-dlp: {e}")
        return None

# 3. Логика бота
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "Проект 640 готов к работе! Присылай ссылку на видео.")

@bot.message_handler(func=lambda m: "http" in m.text)
def handle_link(message):
    status_msg = bot.reply_to(message, "⏳ Пытаюсь скачать видео, используя твои куки...")
    
    video_path = download_video(message.text)
    
    if video_path and os.path.exists(video_path):
        try:
            with open(video_path, 'rb') as video:
                bot.send_video(message.chat.id, video)
            os.remove(video_path)
            bot.delete_message(message.chat.id, status_msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Ошибка при отправке файла: {e}", message.chat.id, status_msg.message_id)
    else:
        bot.edit_message_text("❌ Не удалось скачать. YouTube заблокировал запрос или файл слишком большой.", message.chat.id, status_msg.message_id)

# 4. Запуск сервера и бота
def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    # Запускаем Flask в отдельном потоке
    Thread(target=run_flask).start()
    
    # Запускаем бесконечный опрос бота с защитой от сбоев
    print("Бот запущен...")
    while True:
        try:
            bot.polling(none_stop=True, interval=3, timeout=20)
        except Exception as e:
            print(f"Ошибка подключения (409 или сеть): {e}")
            time.sleep(10)
