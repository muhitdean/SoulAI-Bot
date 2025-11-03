import os
import telebot
from ai_module import AIModule

# Инициализация
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN)
ai = AIModule()

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = """
✨ *Добро пожаловать в SoulAI!* ✨

Я - твой эмпатичный AI-психолог с искусственным интеллектом 🧠

*Я умею:*
• Вести глубокие осмысленные диалоги
• Анализировать твое эмоциональное состояние  
• Помогать с психологическими проблемами
• Запоминать наш разговор и контекст

*Просто напиши мне о том, что тебя волнует...* 💫
    """
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

# Обработчик всех текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_all_messages(message):
    user_id = str(message.chat.id)
    user_message = message.text
    
    try:
        # Показываем что бот печатает
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Получаем умный ответ от AI
        response = ai.generate_response(user_id, user_message)
        
        # Отправляем ответ
        bot.send_message(message.chat.id, response)
        
    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка. Попробуй еще раз.")

print("🟢 SoulAI Telegram бот запущен!")
bot.polling(none_stop=True)
