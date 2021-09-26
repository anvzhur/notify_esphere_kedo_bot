import logging

from aiogram import Dispatcher

from config import admins


async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            me = await dp.bot.get_me()

            await dp.bot.send_message(admin, "Бот Запущен:"+me.first_name)

        except Exception as err:
            logging.exception(err)
