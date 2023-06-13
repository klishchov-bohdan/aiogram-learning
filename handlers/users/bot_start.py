from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from loader import dp

from filters import IsPrivate, IsSubscribed
from utils.db_api import quick_commands as commands
from utils.misc import rate_limit


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), IsSubscribed(), CommandStart())
async def command_start(message: types.Message):
    args = message.get_args()
    new_args = await commands.check_args(args, message.from_user.id)
    try:
        user = await commands.select_user(message.from_user.id)
        if user.status == 'active':     # if not banned
            await message.answer(f'hello, <b>{user.first_name}</b>\n'
                                 f'you <s>already</s> <i>registered</i>')
            # <b>bold</b>
            # <i>cursive</i>
            # <s>cross out</s>
            # <u>underline</u>
            # <a href='...'>link</a>
            # <code>copy on click</code>
        elif user.status == 'banned':
            await message.answer('you banned')
    except Exception:
        await commands.add_user(user_id=message.from_user.id,
                                first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name,
                                username=message.from_user.username,
                                referral_id=int(new_args),
                                status='active',
                                balance=0.0)
        try:
            await dp.bot.send_message(chat_id=int(new_args), text=f'{message.from_user.full_name} registered with your referral link')
        except Exception:
            pass
        await message.answer('you registered successfully')


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='/ban')
async def get_ban(message: types.Message):
    await commands.update_user_status(message.from_user.id, 'banned')
    await message.answer('You banned')


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='/unban')
async def get_unban(message: types.Message):
    await commands.update_user_status(message.from_user.id, 'active')
    await message.answer('You unbanned')


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='/profile')
async def get_unban(message: types.Message):
    user = await commands.select_user(message.from_user.id)
    await message.answer(f'id: {user.user_id}\n'
                         f'first name: {user.first_name}\n'
                         f'last name: {user.last_name}\n'
                         f'username: {user.username}\n'
                         f'status: {user.status}')
