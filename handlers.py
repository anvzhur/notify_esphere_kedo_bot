from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError

from kedopack import mainlib
from keyboards.default.menu import menu
from keyboards.inline.choice_buttons import choice
from load_all import bot, dp, db
from states.kedo_states import KedoStates


class DBCommands:
    pool: Connection = db
    ADD_NEW_USER_REFERRAL = "INSERT INTO users(chat_id, username, full_name, referral) " \
                            "VALUES ($1, $2, $3, $4) RETURNING id"
    ADD_NEW_USER = "INSERT INTO users(chat_id, username, full_name) VALUES ($1, $2, $3) RETURNING id"
    COUNT_USERS = "SELECT COUNT(*) FROM users"
    GET_ID = "SELECT id FROM users WHERE chat_id = $1"
    CHECK_REFERRALS = "SELECT chat_id FROM users WHERE referral=" \
                      "(SELECT id FROM users WHERE chat_id=$1)"
    SELECT_CHAT_ID = "SELECT chat_id FROM users WHERE kedo_user_id = $1"
    ADD_MONEY = "UPDATE users SET balance=balance+$1 WHERE chat_id = $2"
    ADD_EVENT_ID = "INSERT INTO lentamark(event_id) VALUES ($1)"
    GET_MAX_EVENT_ID = "SELECT MAX(event_id) FROM lentamark"
    UPDATE_USER_LINK = "UPDATE users SET kedo_user_id = $1 WHERE chat_id = $2"


    async def add_new_user(self, referral=None):
        user = types.User.get_current()

        chat_id = user.id
        username = user.username
        full_name = user.full_name
        args = chat_id, username, full_name

        if referral:
            args += (int(referral),)
            command = self.ADD_NEW_USER_REFERRAL
        else:
            command = self.ADD_NEW_USER

        try:
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            pass

    async def count_users(self):
        record: Record = await self.pool.fetchval(self.COUNT_USERS)
        return record

    async def get_id(self):
        command = self.GET_ID
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)

    async def check_referrals(self):
        user_id = types.User.get_current().id
        command = self.CHECK_REFERRALS
        rows = await self.pool.fetch(command, user_id)
        return ", ".join([
            f"{num + 1}. " + (await bot.get_chat(user["chat_id"])).get_mention(as_html=True)
            for num, user in enumerate(rows)
        ])

    async def select_chat_id(self, kedo_user_id):
        command = self.SELECT_CHAT_ID
        return await self.pool.fetchval(command, kedo_user_id)

    async def add_money(self, money):
        command = self.ADD_MONEY
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, money, user_id)

    async def update_user_link(self, user_kedo_id):
        command = self.UPDATE_USER_LINK
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_kedo_id, user_id)

    async def add_event_id(self, event_id):
        command = self.ADD_EVENT_ID
        return await self.pool.fetchval(command, event_id)

    async def get_max_event_id(self):
        record: Record = await self.pool.fetchval(self.GET_MAX_EVENT_ID)
        if record is None:
            record = 0
        return record


db = DBCommands()


@dp.message_handler(commands=["start"])
async def register_user(message: types.Message):
    chat_id = message.from_user.id
    id = await db.add_new_user()
    count_users = await db.count_users()
    text = ""
    if not id:
        id = await db.get_id()
    else:
        text += "Записал в базу! "

    bot_username = (await bot.me).username
    bot_link = f"https://t.me/{bot_username}?start={id}"
    text += f"""
Кол-во пользователей: {count_users}
1. Зарегистрируйтесь по ссылке из письма.
Инструкця по работе \nhttps://disk.yandex.ru/i/ATOEdoBkAnjMuA


2 Подключитесь к оповещениям в КЭДО, нажмите: /joinKEDO


"""

    await bot.send_message(chat_id, text, reply_markup=menu)


@dp.message_handler(commands=["joinKEDO"])
async def join_kedo(message: types.Message):
    await message.answer("Введите данные СНИЛС. Пример 1111111111", reply_markup=choice)
    await KedoStates.Reg.set()


@dp.callback_query_handler(text="cancel", state=KedoStates.Reg)
async def cancel_reg(call: CallbackQuery, state: FSMContext):
    await call.answer("Вы отменили режим регистрации!", show_alert=True)
    await state.reset_state()


@dp.message_handler(state=KedoStates.Reg)
async def join_kedo(message: types.Message, state: FSMContext):
    answer = message.text
    if answer.isdigit() == True:
        userID = mainlib.get_usr_id(answer)
        if userID != "":
            await db.update_user_link(userID)
            await message.answer("Данные обновлены", reply_markup=None)
            await state.reset_state()
        else:
            await message.answer("Пользователь с указанными данными не найден В КЭДО", reply_markup=choice)
    else:
        await message.answer(f'Необходимо ввести СНИЛС вместо {answer}    ', reply_markup=choice)
