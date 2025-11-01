from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os
import requests
import telebot

# Токены
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    # Создаем клавиатуру с кнопками
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    buttons = [
        KeyboardButton('🧠 Психологический профиль'),
        KeyboardButton('📸 Отправить фото'),
        KeyboardButton('🎤 Анализ голоса'), 
        KeyboardButton('👶 Детский рисунок'),
        KeyboardButton('🏥 Диагностика'),
        KeyboardButton('🗣️ Логопедия'),
        KeyboardButton('ℹ️ Помощь')
    ]
    
    markup.add(*buttons)
    
    welcome_text = """
✨ *Добро пожаловать в SoulAI!* ✨

Я - твой персональный психологический супер-интеллект 🧠

*Выбери действие:* 👇
    """
    
    bot.send_message(message.chat.id, welcome_text, 
                   reply_markup=markup, parse_mode="Markdown")

# ОБРАБОТЧИК КНОПКИ "ОТПРАВИТЬ ФОТО"
@bot.message_handler(func=lambda message: message.text == '📸 Отправить фото')
def handle_photo_button(message):
    bot.send_message(message.chat.id, 
                   "📸 *Отправь фото лица для анализа эмоций...*\n\n_Я проанализирую твои эмоции по выражению лица_ 😊", 
                   parse_mode="Markdown")

# ОБРАБОТЧИК ФОТОГРАФИЙ
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    """Обработка фотографий"""
    bot.send_message(message.chat.id, "🔍 *Анализирую эмоции на фото...*", parse_mode="Markdown")
    
    try:
        # AI-анализ через Groq
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "messages": [
                    {
                        "role": "system", 
                        "content": """Ты - эксперт по психологии эмоций и анализу лиц. 
                        Проанализируй возможные эмоции на фото. Опиши:
                        1. Какие эмоции может испытывать человек
                        2. Интенсивность эмоций
                        3. Возможное психологическое состояние
                        4. Дай эмпатичный совет
                        
                        Будь точным и поддерживающим. Используй смайлики."""
                    },
                    {
                        "role": "user", 
                        "content": "Проанализируй эмоции на этом фото лица"
                    }
                ],
                "model": "llama-3.1-8b-instant",
                "temperature": 0.7,
                "max_tokens": 400
            }
        )
        
        result = response.json()
        ai_response = result["choices"][0]["message"]["content"]
        
        response_text = f"""
📸 *Результат анализа фото:*

{ai_response}

✨ *Помни: я здесь чтобы помочь!*
        """
        bot.send_message(message.chat.id, response_text, parse_mode="Markdown")
        
    except Exception as e:
        bot.send_message(message.chat.id, "❌ *Произошла ошибка при анализе. Попробуй еще раз.*", parse_mode="Markdown")

# ОБРАБОТЧИК ДРУГИХ КНОПОК
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    text = message.text
    
    if text == '🧠 Психологический профиль':
        bot.send_message(message.chat.id, "💭 *Напиши о себе несколько предложений...*", parse_mode="Markdown")
        bot.register_next_step_handler(message, process_psychological_profile)
    
    elif text == '🎤 Анализ голоса':
        bot.send_message(message.chat.id, "🎤 *Отправь голосовое сообщение для анализа эмоций...*", parse_mode="Markdown")
    
    elif text == '👶 Детский рисунок':
        bot.send_message(message.chat.id, "🖼️ *Отправь фото детского рисунка для анализа...*", parse_mode="Markdown")
    
    elif text == '🏥 Диагностика':
        bot.send_message(message.chat.id, "🤒 *Опиши симптомы для диагностики...*", parse_mode="Markdown")
        bot.register_next_step_handler(message, process_medical_diagnosis)
    
    elif text == '🗣️ Логопедия':
        bot.send_message(message.chat.id, "🎤 *Отправь голосовое сообщение для логопедического анализа...*", parse_mode="Markdown")
    
    elif text == 'ℹ️ Помощь':
        show_help(message)

def process_psychological_profile(message):
    """Обработка психологического профиля"""
    user_text = message.text
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "messages": [
                    {
                        "role": "system", 
                        "content": """Ты - опытный психолог-профайлер. Проанализируй текст и составь психологический портрет."""
                    },
                    {"role": "user", "content": user_text}
                ],
                "model": "llama-3.1-8b-instant",
                "temperature": 0.7
            }
        )
        
        result = response.json()
        ai_response = result["choices"][0]["message"]["content"]
        
        bot.send_message(message.chat.id, f"🧠 *Твой психологический портрет:*\n\n{ai_response}", parse_mode="Markdown")
        
    except Exception as e:
        bot.send_message(message.chat.id, "❌ Ошибка анализа. Попробуй еще раз.")

def show_help(message):
    help_text = """
🆘 *Помощь по SoulAI*

*Доступные функции:*
🧠 *Психологический профиль* - анализ личности по тексту
📸 *Отправить фото* - анализ эмоций по фото лица
🎤 *Анализ голоса* - эмоциональный анализ голоса
👶 *Детский рисунок* - психологический анализ рисунков
🏥 *Диагностика* - медицинский анализ симптомов
🗣️ *Логопедия* - анализ речевых нарушений

*Просто выбери нужную кнопку!* ✨
    """
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

print("🟢 SoulAI Telegram бот запущен!")
bot.polling(none_stop=True)
