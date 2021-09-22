from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/joinKEDO", ),
        ]
    ],
    resize_keyboard=True
)
