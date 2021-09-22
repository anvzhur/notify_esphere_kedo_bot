import logging
import asyncio

from aiogram import Dispatcher


async def send_message_to_kdp(dp: Dispatcher, message_text):
    from config import kdp_list
    await asyncio.sleep(1)
    for kdp_chat_id in kdp_list:
        await send_message_to(dp, kdp_chat_id, message_text)


async def send_message_to(dp: Dispatcher, chatid, message_text):
    try:
        await asyncio.sleep(0.1)
        await dp.bot.send_message(chatid, message_text)

    except Exception as err:
        logging.exception(err)
