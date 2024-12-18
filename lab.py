import os
import requests
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType, ReplyKeyboardMarkup, KeyboardButton
from PIL import Image, ImageEnhance
import pytesseract  # Для OCR
import cv2
import numpy as np
from spellchecker import SpellChecker
import re
import asyncio
import config

BOT_TOKEN = config.BOT_TOKEN

# Создаем объект бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

selected_language = "eng"

# Клавиатура для выбора языка
language_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
language_keyboard.add(KeyboardButton("English"), KeyboardButton("Русский"))

# Функция для предобработки изображения
def preprocess_image(image_path):
    # загрузка
    img = cv2.imread(image_path)

    # В ЧБ формат
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Усиление контраста CLAHE (Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced_img = clahe.apply(gray)

    # Шумоподавление
    denoised_img = cv2.medianBlur(enhanced_img, 3)

    # Бинаризация. улучшвет разделение текста от фона
    _, binarized = cv2.threshold(denoised_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Сохраняем
    cv2.imwrite(image_path, binarized)

    return image_path

# Функция для распознавания текста с изображения
def extract_text_from_image(image_path, lang='eng'):
    try:
        img = Image.open(image_path)
        # Распознаем текст
        text = pytesseract.image_to_string(img, lang=lang)
        return text.strip() if text.strip() else "Текст не найден на изображении."
    except Exception as e:
        return f"Ошибка при обработке изображения: {str(e)}"

# Постобработка текста
def postprocess_text(text):
    filter(None, text)

    #удаление лишних пробелов, символов
    normalized_text = re.sub(r'\s+', ' ', text)  # Удаление лишних пробелов
    normalized_text = re.sub(r'[^\w\s.,?!]', '', normalized_text)  # Удаление спецсимволов (кроме , . ? !)

    # извлечения конкретных данных ( дат и чисел)
    # numbers = re.findall(r'\d+', normalized_text)
    # extracted_numbers = " ".join(numbers)
    # dates = re.findall(r'\d{2}-\d{2}-\d{4}', normalized_text)
    # extracted_dates = " ".join(dates)

    return normalized_text #, extracted_numbers, extracted_dates

# Обработка команд
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Отправьте фото с текстом для распознавания, и я помогу вам. Выберите язык:", reply_markup=language_keyboard)

# Обработка выбора языка
@dp.message_handler(lambda message: message.text in ["English", "Русский"])
async def set_language(message: types.Message):
    global selected_language
    selected_language = 'eng' if message.text == "English" else 'rus'
    await message.reply(f"Вы выбрали язык: {message.text}. Теперь отправьте фото с текстом.")
    # Сохраняем выбранный язык в атрибут пользователя


# Обработка изображений
@dp.message_handler(content_types=ContentType.PHOTO)
async def handle_photo(message: types.Message):
    global selected_language
    # Скачиваем фото
    photo = message.photo[-1]  # Берем фото с максимальным разрешением
    file_info = await bot.get_file(photo.file_id)
    file_path = file_info.file_path
    downloaded_file = await bot.download_file(file_path)

    # Сохраняем изображение локально
    image_path = f"downloads/{photo.file_id}.jpg"
    os.makedirs("downloads", exist_ok=True)
    with open(image_path, "wb") as f:
        f.write(downloaded_file.read())

    # Предобработка
    preprocessed_image_path = preprocess_image(image_path)

    # Распознаем текст
    extracted_text = extract_text_from_image(preprocessed_image_path, selected_language)

    # Постобработка текста
    processed_text = postprocess_text(extracted_text)

    # Отправляем результат пользователю
    await message.reply(f"Распознанный и обработанный текст:\n{processed_text}")
    # await message.reply(f"Извлеченные числа: {numbers}")
    # await message.reply(f"Извлеченные даты: {dates}")


async def main():
    print("Бот запущен!")
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
