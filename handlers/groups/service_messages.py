from aiogram import types

from filters import IsGroup
from loader import dp, bot
from utils.misc import rate_limit


@rate_limit(limit=0, key='groups')
@dp.message_handler(IsGroup(), content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def welcome_message(message: types.Message):
    # await message.reply(f'Hello, {message.from_user.full_name}')
    members = ', '.join([mess.get_mention(as_html=True) for mess in message.new_chat_members])
    await message.reply(f'Hello, {members}')


@rate_limit(limit=0, key='groups')
@dp.message_handler(IsGroup(), content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def left_chat_member(message: types.Message):
    # bot_obj = await bot.get_me()
    # bot_id = bot_obj.id
    # if user left
    if message.left_chat_member.id == message.from_user.id:
        await message.reply(f'{message.left_chat_member.get_mention(as_html=True)} left group')
    # if user deleted by another user
    else:
        await message.answer(f'{message.left_chat_member.get_mention(as_html=True)} deleted from chat \n'
                             f'by user {message.from_user.get_mention(as_html=True)}')

