import random

from aiogram import types
from aiogram.utils import executor
from config import bot, dp
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f'Салам братишка {message.from_user.first_name}')


@dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton('NEXT', callback_data='button_call_1')
    markup.add(button_call_1)

    question = 'Перевод маймыл'
    answers = ['Таджик бапеш', 'Кыргызстан алга', 'Абизяна', 'Нурбол']

    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        open_period=10,
        reply_markup=markup


    )

@dp.callback_query_handler(lambda call: call.data == 'button_call_1')
async def quiz_2(call: types.CallbackQuery):

    question = 'Страна с самой большой площадью'
    answers = ['Россия', 'Китай', "Канада", 'Индия']

    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        open_period=10


    )
@dp.message_handler(commands=['mem'])
async def mem(message: types.message):
    photos = ['media/maimul.jpg', 'media/mamal.jpg', 'media/mamil.jfif', 'media/mmamul.jfif']
    random_photos = random.choice(photos)
    photo = open(random_photos, 'rb')
    await bot.send_photo(message.from_user.id, photo)


@dp.message_handler(content_types=['text', 'photo'])
async def echo(message: types.Message):
    try:
        a = int(message.text)
        await bot.send_message(message.from_user.id, a*a)

    except:



        await bot.send_message(message.from_user.id, message.text)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)