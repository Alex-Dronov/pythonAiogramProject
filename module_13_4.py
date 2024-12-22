from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text = "Calories")
async def set_age(message):
    await message.answer('Введите свой возраст (полных лет):')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(user_age = message.text)
    await message.answer('Введите свой рост (см):')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(user_growth = message.text)
    await message.answer('Введите свой вес (кг):')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(user_weight = message.text)
    data = await state.get_data()
    result = (10 * int(data['user_weight'])) + (6.25 * int(data['user_growth'])) - (5 * int(data['user_age'])) + 5

    await message.answer(f'Необходимое Вам количество килокалорий в сутки: {result}')
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)