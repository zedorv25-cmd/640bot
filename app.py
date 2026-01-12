import os
import telebot
from flask import Flask
from threading import Thread

# БЕРЕМ ТОКЕН ТОЛЬКО ИЗ НАСТРОЕК RENDER
TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Project 640 IS ACTIVE"

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "Работает! Присылай ссылку.")

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
