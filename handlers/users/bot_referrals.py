from aiogram import types
from aiogram.utils.deep_linking import get_start_link

from loader import dp
from utils.db_api import quick_commands as commands


@dp.message_handler(text='/ref')
async def command_ref(message: types.Message):
    ref_link = await get_start_link(payload=message.from_user.id)
    count_refs = await commands.count_refs(message.from_user.id)
    await message.answer(f'hello {message.from_user.full_name}\n'
                         f'You have {count_refs} referrals\n'
                         f'You referral link:\n'
                         f'{ref_link}')
