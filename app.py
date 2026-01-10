import os
import telebot
from flask import Flask
from threading import Thread

# Устанавливаем токен напрямую как строку, чтобы Render его точно увидел
TOKEN = '8349153278:AAGP0SgBwqWZeY8cfw7Jf86My1MRkJSGd_8'

def create_bot():
    try:
        # Теперь здесь нет os.environ.get, только прямая передача токена
        return telebot.TeleBot(TOKEN)
    except Exception as e:
        print(f"!!! Error initializing bot: {e} !!!")
        return None

bot = create_bot()

# Flask-сервер для поддержания статуса Live в Render
app = Flask(__name__)

@app.route('/')
def index():
    return "Project 640 is Live. Web server is active."

def run_web():
    # Используем порт 10000, который требует Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Обработчики команд бота
if bot:
    @bot.message_handler(commands=['start'])
    def start_cmd(message):
        bot.reply_to(message, "Проект 640: Система запущена и работает корректно!")

    @bot.message_handler(func=lambda m: True)
    def echo_msg(message):
        bot.reply_to(message, f"Бот на связи! Вы написали: {message.text}")

# Запуск всего вместе
if __name__ == "__main__":
    # Запускаем веб-сервер в отдельном потоке
    web_thread = Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()
    
    if bot:
        print("Bot is starting polling...")
        # infinity_polling устойчив к временным разрывам связи
        bot.infinity_polling(timeout=20, long_polling_timeout=10)
    else:
        print("Bot failed to start.")
        web_thread.join()
