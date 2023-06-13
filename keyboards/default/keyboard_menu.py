from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='ten'),
            KeyboardButton(text='eleven'),
        ],
        [
            KeyboardButton(text='100'),
        ],
        [
            KeyboardButton(text='Inline menu'),
            KeyboardButton(text='Any text'),
            KeyboardButton(text='Like'),
        ]
    ],
    resize_keyboard=True
)
