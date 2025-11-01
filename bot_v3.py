import os
import telebot
import requests

# Получаем переменные окружения
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# ⚠️ ДОБАВЬ ЭТУ ПРОВЕРКУ ⚠️
print(f"TELEGRAM_TOKEN: {'***' + TELEGRAM_TOKEN[-10:] if TELEGRAM_TOKEN else 'NOT SET!'}")
print(f"GROQ_API_KEY: {'***' + GROQ_API_KEY[-10:] if GROQ_API_KEY else 'NOT SET!'}")

if not TELEGRAM_TOKEN:
    print("❌ КРИТИЧЕСКАЯ ОШИБКА: TELEGRAM_TOKEN не установлен!")
    print("Добавь TELEGRAM_TOKEN в Environment Variables в Render!")
    exit(1)

if not GROQ_API_KEY:
    print("❌ КРИТИЧЕСКАЯ ОШИБКА: GROQ_API_KEY не установлен!")
    print("Добавь GROQ_API_KEY в Environment Variables в Render!")
    exit(1)

print("✅ Environment Variables загружены успешно!")
