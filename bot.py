import os
import telebot
from flask import Flask, request

# Берём токен из переменных окружения Render
TOKEN = os.getenv("TOKEN")  # ←←← именно так ты добавляла на Render

bot = telebot.TeleBot(TOKEN)

# ────────────────────── ТВОИ ТРИГГЕРЫ ──────────────────────
triggers = {
    "версия": "Версия игры от 1.20 и выше. Также в тг-канале есть все варианты и версии мода на бедрок.",
    "версию": "Версия игры от 1.20 и выше. Также в тг-канале есть все варианты и версии мода на бедрок.",
    "не появился": "Мирная сложность или использовать яйцо спавна, так же нужно проверить тот ли мод установлен и находится он в папке модов.",
    "не появляется": "Мирная сложность или использовать яйцо спавна, так же нужно проверить тот ли мод установлен и находится он в папке модов.",
    "не спавнится": "Мирная сложность или использовать яйцо спавна, так же нужно проверить тот ли мод установлен и находится он в папке модов.",
    "где мод": "Все моды есть в тг-канале! Харе лениться и пролистайте его!",
    "где скачать": "Все моды есть в тг-канале! Харе лениться и пролистайте его!",
    "азаль": "Я тут, всегда на страже",
    "привет": "Привет, красавчик.",
    "ты так": "Я могу и обидеться",
    # добавляй сюда сколько угодно
}

def contains_trigger(text):
    if not text:
        return None
    text_lower = text.lower()
    for trigger, reply in triggers.items():
        if trigger in text_lower:
            return reply
    return None

@bot.message_handler(func=lambda message: True)
def reply(message):
    response = contains_trigger(message.text)
    if response:
        bot.reply_to(message, response)

# ────────────────────── Flask для Render ──────────────────────
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().as_text()
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid content-type', 403

@app.route('/')
def index():
    bot.remove_webhook()
    bot.set_webhook(url="https://azal-bot.onrender.com/" + TOKEN)
    return "Webhook установлен!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("Бот запущен!")
    app.run(host="0.0.0.0", port=port)
