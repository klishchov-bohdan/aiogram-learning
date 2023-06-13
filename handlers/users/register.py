from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from filters import IsPrivate
from keyboards.default import kb_menu
from loader import dp

from states import Register


@dp.message_handler(IsPrivate(), Command('register'))
async def register(message: types.Message):
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

    clue_button = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f'{message.from_user.first_name}')
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer('Hello, you start registration\nEnter your name', reply_markup=clue_button)
    await Register.test1.set()


@dp.message_handler(state=Register.test1)
async def state1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(test1=answer)
    await message.answer(f'{answer}, age?')
    await Register.test2.set()


@dp.message_handler(state=Register.test2)
async def state2(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(test2=answer)
    data = await state.get_data()
    name = data.get('test1')
    age = data.get('test2')
    await message.answer(f'Registration completed\n'
                         f'Your name: {name}\n'
                         f'Your age: {age}', reply_markup=kb_menu)
    await state.finish()
