from aiogram.types import ContentType, Message, InputFile, MediaGroup

from keyboards.inline import ikb_menu
from loader import dp


@dp.message_handler(content_types=ContentType.PHOTO)
async def send_photo_file_id(message: Message):
    await message.reply(message.photo[-1].file_id)


@dp.message_handler(content_types=ContentType.AUDIO)
async def send_audio_file_id(message: Message):
    await message.reply(message.audio.file_id)


@dp.message_handler(text='/photo')
async def send_photo(message: Message):
    chat_id = message.from_user.id
    photo_bytes = InputFile(path_or_bytesio='media/desktop-1920x1080.jpg')
    await dp.bot.send_photo(chat_id=chat_id, photo=photo_bytes, caption='Description photo', reply_markup=ikb_menu)


@dp.message_handler(text='/audio')
async def send_audio(message: Message):
    chat_id = message.from_user.id
    audio_bytes = InputFile(path_or_bytesio='media/audio.mp3')
    await dp.bot.send_audio(chat_id=chat_id, audio=audio_bytes, caption='Description audio', reply_markup=ikb_menu)


@dp.message_handler(text='/album')
async def send_album(message: Message):
    photo_bytes = InputFile(path_or_bytesio='media/desktop-1920x1080.jpg')
    photo_file_id = 'AgACAgIAAxkBAAPGZINAQhvu16Usji5gu9x05O439iEAAo7IMRs6wxlItI_WFtc1AlQBAAMCAAN5AAMvBA'
    audio_bytes = InputFile(path_or_bytesio='media/audio.mp3')
    album = MediaGroup()
    album.attach_photo(photo=photo_bytes)
    album.attach_photo(photo=photo_file_id, caption='Description album')
    # album.attach_audio(audio=audio_bytes) # cant mix with other media types
    await message.answer_media_group(media=album)
