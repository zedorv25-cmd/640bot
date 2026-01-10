import os
import telebot
from flask import Flask
from threading import Thread

# Забираем токен из настроек Render
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def index():
    return "640bot is running!"

def run_web():
    # Порт 10000 обязателен для бесплатного тарифа Render
    app.run(host='0.0.0.0', port=10000)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Проект 640 активирован. Бот готов к работе!")

if __name__ == "__main__":
    # Запуск веб-сервера в фоне
    Thread(target=run_web).start()
    # Запуск самого бота
    bot.infinity_polling()
