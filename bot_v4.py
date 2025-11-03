import os
import telebot
from ai_module import AIModule

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN)
ai = AIModule()

@bot.message_handler(commands=['start'])
def start(message):
    welcome = "✨ Привет! Я SoulAI - твой психологический помощник. Просто напиши мне что-то... 💫"
    bot.send_message(message.chat.id, welcome)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        user_id = str(message.chat.id)
        response = ai.generate_response(user_id, message.text)
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, "Привет! Расскажи, как твои дела? 😊")

if __name__ == "__main__":
    print("🟢 Бот запущен!")
    bot.polling(none_stop=True)
