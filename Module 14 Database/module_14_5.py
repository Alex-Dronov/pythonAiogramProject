from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from crud_functions import *

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Initializing Products database
initiate_db()

first_kb = ReplyKeyboardMarkup(resize_keyboard=True)
btn_calc = KeyboardButton(text='Расcчитать')
btn_info = KeyboardButton(text='Информация')
btn_buy  = KeyboardButton(text='Купить')
btn_reg  = KeyboardButton(text='Регистрация')
first_kb.row(btn_calc, btn_info)
first_kb.row(btn_buy, btn_reg)

inl_kbd = InlineKeyboardMarkup()
inl_btn_calc = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inl_btn_frml = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inl_kbd.row(inl_btn_calc, inl_btn_frml)

inl_kbd_prod = InlineKeyboardMarkup()
inl_btn_prod1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
inl_btn_prod2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
inl_btn_prod3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
inl_btn_prod4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
inl_kbd_prod.row(inl_btn_prod1, inl_btn_prod2, inl_btn_prod3, inl_btn_prod4)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState (StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State("1000")

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=first_kb)

@dp.message_handler(text=['Расcчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inl_kbd)

@dp.message_handler(text=['Регистрация'])
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer('Пользователь существует, введите другое имя (только латинский алфавит):')
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'] ,data['age'])
    await message.answer(f'Пользователь {data["username"]} успешно зарегистрирован')
    await state.finish()

@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    all_products = get_all_products()
    for prod in all_products:
        with open(f"Img/{prod[0]}.webp", "rb") as img:
            await message.answer_photo(img, f'Название: {prod[1]} | Описание: {prod[2]}| Цена: {prod[3]}',
                                       allow_sending_without_reply=True)
    await message.answer('Выберите продукт для покупки:', reply_markup=inl_kbd_prod)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст (полных лет):')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(user_age=message.text)
    await message.answer('Введите свой рост (см):')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(user_growth=message.text)
    await message.answer('Введите свой вес (кг):')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(user_weight=message.text)
    data = await state.get_data()
    result = (10 * int(data['user_weight'])) + (6.25 * int(data['user_growth'])) - (5 * int(data['user_age'])) + 5
    await message.answer(f'Ваша норма калорий в сутки: {result}')
    await state.finish()

@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
