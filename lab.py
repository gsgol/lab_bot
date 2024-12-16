import requests
import json
import os
from aiogram import Bot
import asyncio
import pandas as pd

BOT_TOKEN = "8028312611:AAEnBjNW-vSQlnBfilyq3laPZMhluJ_zq-8"

bot = Bot(token=BOT_TOKEN)


async def telegram_bot_sendmessage(bot_message, chat_id):
    await bot.send_message(chat_id=chat_id, text=bot_message)
    return 0


async def Chatbot(connection):
    cwd = os.getcwd()
    filename = cwd + "/chatgpt.txt"
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("1")
    else:
        print("File Exists")

    with open(filename) as f:
        last_update = f.read()

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update}"
    response = requests.get(url)
    data = json.loads(response.content)

    for result in data["result"]:
        try:
            if float(result["update_id"]) > float(last_update):

                last_update = str(int(result["update_id"]))
                chat_id = str(result["message"]["chat"]["id"])
                with open(filename, "w") as f:
                    f.write(last_update)

        except Exception as e:
            print(e)
            await telegram_bot_sendmessage("Произошла ошибка\n", chat_id)



async def main():
    while True:
        timertime = 5
        await Chatbot()
        await asyncio.sleep(timertime)


if __name__ == "__main__":
    asyncio.run(main())