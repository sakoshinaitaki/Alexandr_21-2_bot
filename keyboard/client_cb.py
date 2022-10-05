from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel_button = KeyboardButton("Cancel")
cancel_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
).add(cancel_button)

menu_salad = KeyboardButton('Салат 🥗')
menu_soup = KeyboardButton('Суп 🥣')
menu_hot = KeyboardButton('Горячее 🍳')
menu_desert = KeyboardButton('Десерт 🍩')
menu_drink = KeyboardButton('Напиток 🍺')

menu_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
).add(menu_salad, menu_soup, menu_hot, menu_desert, menu_drink).row(cancel_button)