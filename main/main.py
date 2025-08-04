import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage


token = '8322636445:AAF1zCHudUB-A4BrDd8_m7u8OTNskZBb8GY'
bot = Bot(token=token)

dp = Dispatcher(storage=MemoryStorage())



class Register(StatesGroup):
    name = State()
    email = State()
    phone = State()

def init_db():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            name TEXT, email TEXT
        )
    """)
    conn.commit()
    conn.close()

@dp.message(CommandStart())
async def cmd_str(message: Message, state: FSMContext):
    await message.answer('Привет! Введите свое имя для регистрации!')
    await state.set_state(Register.name)


@dp.message(Register.name)
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(name=name)
    await message.answer('Введите ваш email:')
    await state.set_state(Register.email)

@dp.message(Register.email)
async def process_email(message: Message, state: FSMContext):
    email = message.text.strip()
    await state.update_data(email=email)
    await message.answer('Теперь введите свой номер телефона')
    await state.set_state(Register.phone)


@dp.message(Register.phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    data = await state.get_data()
    name = data['name']

    conn =sqlite3.connect('users.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE phone = ?", (phone, ))
    user = cur.fetchone()

    if user:
        await message.answer('Вы уже зарегистрировались!')
    else:
        cur.execute("INSERT INTO users (telegram_id, name, email, phone) VALUES (?, ?, ?, ?)",
                    (message.from_user.id, name, email, phone))
        conn.commit()
        await message.answer(f'Спасибо за регистрацию, {name} {email} {phone}!')
    conn.close()
    await state.clear()

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())