import os
import json
import random
import datetime
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from dotenv import load_dotenv

# Загрузка токена из .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Путь к файлу с пользователями
USER_DATA_FILE = "data/users.json"

# Загрузка или инициализация хранилища
if os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, "r") as f:
        user_data = json.load(f)
else:
    user_data = {}

@dp.message(CommandStart())
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Получить вопрос дня 🔮")]],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await message.answer(
        "Привет! Это Вопрос — Таро. Нажми кнопку ниже и получи своё предсказание дня 👁",
        reply_markup=keyboard
    )

@dp.message(lambda m: m.text and m.text.lower() in ["получить вопрос", "получить вопрос дня 🔮"])
async def get_prediction(message: types.Message):
    user_id = str(message.from_user.id)
    today = str(datetime.date.today())

    if user_id in user_data and user_data[user_id] == today:
        await message.answer("Ты уже получил своё послание. Возвращайся завтра 🌚")
        return

    image_folder = "data/images"
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith((".jpg", ".png"))]

    if not image_files:
        await message.answer("Нет доступных изображений.")
        return

    image_name = random.choice(image_files)
    image_path = os.path.join(image_folder, image_name)

    photo = FSInputFile(image_path)
    await bot.send_photo(message.chat.id, photo)

    user_data[user_id] = today
    with open(USER_DATA_FILE, "w") as f:
        json.dump(user_data, f)

@dp.message()
async def fallback(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Получить вопрос дня 🔮")]],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await message.answer("Нажми кнопку ниже, чтобы получить своё предсказание 👇", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())