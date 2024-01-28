import asyncio
import logging
import sys
from os import getenv
import sqlite3

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.enums.parse_mode import ParseMode
from checker import check


bot = Bot(token="6829339898:AAH2aKQVVqcR5S8KV2M-GqgGKmRHJ-hdnNI", parse_mode=ParseMode.HTML)
dp = Dispatcher()


async def display(message, results, text,change = 0):

    for i in results:
        p = i[1].splitlines()
        if change>0:
            s = f"+{change} $"
        if change<0:
            s = f"{change} $" 
        if change==0:
            s = ""
        
        cap = f"""🚗<a href='{i[-5]}'>{i[0]}</a>\n💸{i[2]}\n🚴‍♂️{i[3]}\n🇺🇸<a href='{i[4]}'>bidfax</a>\n{text} {s}"""
        photos = [
            types.InputMediaPhoto(media=p[0], parse_mode=ParseMode.HTML, 
                                  caption = cap,disable_web_page_preview=True,),
            types.InputMediaPhoto(media=p[1]),
            types.InputMediaPhoto(media=p[2]),
        ]
        await bot.send_media_group(message.chat.id, photos)
       
        await asyncio.sleep(2)


@dp.message(CommandStart())
async def start(message: Message):
    try:
        conn = sqlite3.connect("cars.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM toyota_sequoia")
        results = cursor.fetchall()

    except (Exception, sqlite3.Error) as error:
        print(error)
    finally:
        conn.close()

    #await display(message, results, "")



    while True:
        check()
        try:
            conn = sqlite3.connect("cars.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM toyota_sequoia WHERE is_new = 1")
            results_1 = list(cursor.fetchall())
            cursor.close()

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM toyota_sequoia WHERE is_sold = 1")
            results_2 = cursor.fetchall()
            cursor.close()

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM toyota_sequoia WHERE NOT is_higher = 0")
            results_3 = cursor.fetchall()
            cursor.close()

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM toyota_sequoia WHERE NOT is_lower = 0")
            results_4 = cursor.fetchall()
            cursor.close()

            if results_1:
                await display(message, results_1, "🆕NEW🆕")
            if results_2:
                await display(message, results_2, "🚫SOLD🚫")
            if results_3:
                await display(message, results_3, "⬆️HIGHER⬆️", results_3[0][-4])
            if results_4:
                await display(message, results_4, "⬇️LOWER⬇️", results_4[0][-3])



        except (Exception, sqlite3.Error) as error:
            print(error)
        finally:
            conn.close()
        await asyncio.sleep(480)







async def main() -> None:
   
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


