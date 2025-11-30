import os
import telebot
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# ────────────────────── ТВОИ ТРИГГЕРЫ (оставляй как есть) ──────────────────────
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
    "азаль": "Я тут, всегда на страже",
    "ты так": "Я могу и обидеться",
    # добавь сюда все остальные свои триггеры, если есть
}

def contains_trigger(text):
    if not text:
        return None
    text_lower = text.lower().strip()
    for trigger, reply in triggers.items():
        if trigger in text_lower:
            return reply
    return None

@bot.message_handler(func=lambda message: True)
def reply(message):
    response = contains_trigger(message.text)
    if response:
        bot.reply_to(message, response)

# ────────────────────── Flask-приложение для Render ──────────────────────
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://azal-bot.onrender.com/' + TOKEN)
    return "Webhook set!", 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print("Бот запущен на Render!")
    app.run(host='0.0.0.0', port=port)
