from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Message', callback_data='message'),
                                        InlineKeyboardButton(text='Link', url='https://google.com/'),
                                    ],
                                    [
                                        InlineKeyboardButton(text='Alert', callback_data='alert'),
                                    ],
                                    [
                                        InlineKeyboardButton(text='Replace menu buttons', callback_data='buttons2'),
                                    ]
                                ])
