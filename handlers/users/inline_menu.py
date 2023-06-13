from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.inline import ikb_menu, ikb_menu2
from keyboards.default import kb_test
from loader import dp


@dp.message_handler(text='Inline menu')
async def show_inline_menu(message: types.Message):
    await message.answer('Inline buttons below', reply_markup=ikb_menu)


@dp.callback_query_handler(text='message')
async def send_message(call: CallbackQuery):
    await call.message.answer('buttons changed', reply_markup=kb_test)


@dp.callback_query_handler(text='alert')
async def send_alert(call: CallbackQuery):
    await call.answer('buttons changed', show_alert=True)


@dp.callback_query_handler(text='buttons2')
async def send_alert(call: CallbackQuery):
    await call.message.edit_reply_markup(ikb_menu2)
