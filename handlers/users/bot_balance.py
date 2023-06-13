from aiogram.dispatcher import FSMContext

from filters import IsPrivate
from loader import dp
from aiogram import types

from utils.db_api import quick_commands as commands

from states import Balance


@dp.message_handler(IsPrivate(), text='/balance')
async def change_balance(message: types.Message):
    user = await commands.select_user(message.from_user.id)
    await message.answer(f'balance - {user.balance}')


@dp.message_handler(IsPrivate(), text='/change_balance')
async def change_balance(message: types.Message):
    await message.answer('enter value: ')
    await Balance.amount.set()


@dp.message_handler(IsPrivate(), state=Balance.amount)
async def change_balance(message: types.Message, state: FSMContext):
    answer = message.text
    check_balance = await commands.check_balance(user_id=message.from_user.id, amount=answer)
    if check_balance == 'no money':
        await message.answer('You have no money')
    elif check_balance:
        await message.answer('Balance changed')
    elif not check_balance:
        await message.answer('Invalid value')
    else:
        await message.answer('Error: use command /start')
    await state.finish()
