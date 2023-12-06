from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from aiogram.filters import CommandStart
import asyncio
import os

load_dotenv('.env')
token= os.getenv('TOKEN_API')
bot= Bot(token)

dp= Dispatcher()

@dp.message(CommandStart())
async def cmd_message(msg: types.Message):
    await msg.answer('Hellow world gt')


async def main():
    await dp.start_polling(bot)
    
    
    
if __name__=="__main__":
    asyncio.run(main())