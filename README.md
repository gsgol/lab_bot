# lab_bot
## Бот на вход принимает фото, обрабатывет его с помощью модели pytesseract и выводит текст с фотографии




[Пользователь]
    |
    | (Выбор языка)
    |
    v
    |
    |  (Отправка фото)
    |
    v
[Telegram API]
    |
    |  (Получение сообщения с фото)
    |
    v
  [Бот]
    |
    |  (Скачивание изображения)
    |
    v
[Предобработка изображения] -----> [Tesseract Распознавание текста]
                                               |
 (Преобразование изображения)                  | 
 (Уменьшение, контраст, шум)                   |
                                               v
                                    [Обработка текста, проверка орфографии]  
                                               |
                                               |
                                               |
                                               v
                                     [Вывод ответа пользователю]
                                                |
                                                |  (Отправка текста)
                                                |
                                                v
                                         [Пользователь]
