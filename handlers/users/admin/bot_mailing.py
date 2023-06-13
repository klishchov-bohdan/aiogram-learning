from asyncio import sleep

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from filters import IsPrivate
from loader import dp
from aiogram import types

from utils.db_api import quick_commands as commands
from states import BotMailing

from data.config import admins_id


@dp.message_handler(IsPrivate(), text='/mailing', chat_id=admins_id)
async def start_mailing(message: types.Message):
    await message.answer(f'enter mailing text')
    await BotMailing.text.set()


@dp.message_handler(IsPrivate(), state=BotMailing.text, chat_id=admins_id)
async def mailing_text(message: types.Message, state: FSMContext):
    answer = message.text
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Add photo', callback_data='add_photo'),
                                          InlineKeyboardButton(text='Next', callback_data='next'),
                                          InlineKeyboardButton(text='Cancel', callback_data='cancel')
                                      ]
                                  ])
    await state.update_data(text=answer)
    await message.answer(text=answer, reply_markup=markup)
    await BotMailing.state.set()


@dp.callback_query_handler(text='next', state=BotMailing.state, chat_id=admins_id)
async def start(call: types.CallbackQuery, state: FSMContext):
    users = await commands.select_all_users()
    data = await state.get_data()
    text = data.get('text')
    await state.finish()
    for user in users:
        try:
            await dp.bot.send_message(chat_id=user.user_id, text=text)
            await sleep(0.33)
        except Exception:
            pass
    await call.message.answer('Mailing complete')


@dp.callback_query_handler(text='add_photo', state=BotMailing.state, chat_id=admins_id)
async def add_photo(call: types.CallbackQuery):
    await call.message.answer('Enyter photo: ')
    await BotMailing.photo.set()


@dp.message_handler(IsPrivate(), state=BotMailing.photo, content_types=types.ContentType.PHOTO, chat_id=admins_id)
async def mailing_text(message: types.Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Next', callback_data='next'),
                                          InlineKeyboardButton(text='Cancel', callback_data='cancel')
                                      ]
                                  ])
    await message.answer_photo(photo=photo, caption=text, reply_markup=markup)


@dp.callback_query_handler(text='next', state=BotMailing.photo, chat_id=admins_id)
async def start(call: types.CallbackQuery, state: FSMContext):
    users = await commands.select_all_users()
    data = await state.get_data()
    photo = data.get('photo')
    text = data.get('text')
    await state.finish()
    for user in users:
        try:
            await dp.bot.send_photo(chat_id=user.user_id, photo=photo, caption=text)
            await sleep(0.33)
        except Exception:
            pass
    await call.message.answer('Mailing complete')


@dp.message_handler(IsPrivate(), state=BotMailing.photo, chat_id=admins_id)
async def no_photo(message: types.message):
    markup = InlineKeyboardMarkup(row_width=2,
                                  InlineKeyboardButton=[
                                      [
                                          InlineKeyboardButton(text='Cancel', callback_data='cancel')
                                      ]
                                  ])
    await message.answer('Enter photo', reply_markup=markup)


@dp.callback_query_handler(text='cancel', state=[BotMailing.text, BotMailing.photo, BotMailing.state], chat_id=admins_id)
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Mailing canceled')
