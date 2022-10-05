from aiogram import types, Dispatcher
from config import bot, ADMINS, dp


async def pin(message: types.Message):
    if message.chat.type != 'private':
        if message.from_user.id not in ADMINS:
            await message.reply('Не достаточно уполномоченый!')
        elif message.reply_to_message:
            await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)

        else:
            await message.reply('Команда должна быть ответом на cообщение')

    else:
        await message.reply('пищи в группу')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(pin, commands=['pin'], commands_prefix='!/')
