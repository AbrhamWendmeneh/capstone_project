from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from aiogram.filters import CommandStart, Command
import asyncio
import os

load_dotenv('1.env')
token= os.getenv('TOKEN_API')
bot= Bot(token)

dp= Dispatcher()

@dp.message(CommandStart())
async def cmd_message(msg: types.Message):
    await msg.answer('hey how are you?')  
    
@dp.message(Command("help"))
async def cmd_help(msg: types.Message):
    await msg.answer('How can I help you boss')
    
@dp.message(Command('hello_world'))
async def hello_world(msg: types.Message):
    await msg.answer('Hello world!')
    


async def main():
    await dp.start_polling(bot)
    
    
    
if __name__=="__main__":
    asyncio.run(main())