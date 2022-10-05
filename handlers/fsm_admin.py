from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, ADMINS
from keyboard.client_cb import menu_markup, cancel_markup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database import bot_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    type = State()
    price = State()
    description = State()


async def fsm_start(message: types.Message):
    if message.chat.type == 'private':
        await FSMAdmin.photo.set()
        await message.answer(f'Давай начнем {message.from_user.username}?')
        await message.answer(f'Фото блюда: 🖼️', reply_markup=cancel_markup)
    else:
        await message.answer('Пиши в лс!!')




async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer('Название блюда:', reply_markup=cancel_markup)


async def load_name(message: types.Message, state: FSMContext):
    try:
        if len(message.text) > 20:
            raise ValueError
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.answer('Нужно теперь выбрать тип', reply_markup=menu_markup)
    except:
        await message.answer('Слишком длинное название!!')

async def load_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = message.text
    await FSMAdmin.next()
    await message.answer('Цена блюда:', reply_markup=cancel_markup)


async def load_price(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
        if price <= 0:
            raise ValueError
        if price > 1000:
            raise AttributeError
        async with state.proxy() as data:
            data['price'] = price
        await FSMAdmin.next()
        skip_button = KeyboardButton("SKIP")
        skip_markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
        ).add(skip_button)
        await message.answer('Описание блюда', reply_markup=skip_markup)
    except TypeError:
        await message.answer('Пиши нормально')
    except ValueError:
        await message.answer("Такой цены не бывает")
    except AttributeError:
        await message.answer("Тогда у нас не будет денег")


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        await bot.send_photo(message.from_user.id, data['photo'],
                       caption=f"Вот твое блюдо:\n{data['name']}, {data['type']} стоит: {data['price']}\n"
                               f"{data['description']}")
    await bot_db.sql_command_insert(state)
    await state.finish()


async def cancel_menu_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Ну и пошел ты')


async def delete_data(message: types.Message):
    if not message.from_user.id in ADMINS:
        await message.reply('Ты не админ!')
    else:
        dishes = await bot_db.sql_command_all()
        for dish in dishes:
            await bot.send_photo(message.from_user.id, dish[0],
                                 caption=f"Вот твое блюдо:\n{dish[1]}, {dish[2]} стоит: {dish[3]}\n"
                                         f"{dish[4]}",
                                 reply_markup=InlineKeyboardMarkup().add(
                                     InlineKeyboardButton(
                                         f"delete {dish[1]}",
                                         callback_data=f"delete {dish[1]}"
                                     )
                                 ))


async def complete_delete(call: types.CallbackQuery):
    await bot_db.sql_command_delete(call.data.replace("delete ", ""))
    await call.answer(text="Удален из БД", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


def register_handlers_fsm_admin(dp: Dispatcher):
    dp.register_message_handler(cancel_menu_reg, state='*', commands=['cancel'], commands_prefix='\!.')
    dp.register_message_handler(cancel_menu_reg,
                                Text(equals='cancel', ignore_case=True),state='*')
    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo, content_types=['photo'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_type, state=FSMAdmin.type)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(delete_data, commands=['del'])
    dp.register_callback_query_handler(complete_delete,
                                       lambda call: call.data and call.data.startswith("delete "))