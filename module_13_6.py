from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

first_kb = ReplyKeyboardMarkup(resize_keyboard=True)
btn_calc = KeyboardButton(text='Расcчитать')
btn_info = KeyboardButton(text='Информация')
first_kb.row(btn_calc, btn_info)

inl_kbd = InlineKeyboardMarkup()
inl_btn_calc = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inl_btn_frml = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inl_kbd.row(inl_btn_calc, inl_btn_frml)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=first_kb)

@dp.message_handler(text=['Расcчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inl_kbd)

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
