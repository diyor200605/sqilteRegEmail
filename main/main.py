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
    conn =sqlite3.connect('users.db')
    email = message.text.strip()
    cur = conn.cursor()

    cur.execute("SELECT * FROM user WHERE name = ?", (name, email ))
    user = cur.fetchall()

    if user:
        await message.answer('Вы уже зарегистрировались!')
    else:
        cur.execute("INSERT INTO users (telegram_id, name, email) VALUES (?, ?, ?)",
                    (message.from_user.id, name, email))
        conn.commit()
        await message.answer(f'Спасибо за регистрацию, {name} {email}!')
    conn.close()
    await state.clear()

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())