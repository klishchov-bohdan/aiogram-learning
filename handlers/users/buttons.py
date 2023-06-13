from aiogram import types
from loader import dp


@dp.message_handler(text='ten')
async def buttons_ten(message: types.Message):
    await message.answer(f'You select a number, {message.text}')


@dp.message_handler(text='eleven')
async def buttons_ten(message: types.Message):
    await message.answer(f'You select a number, {message.text}')


@dp.message_handler(text='100')
async def buttons_ten(message: types.Message):
    await message.answer(f'You select a number, {message.text}')