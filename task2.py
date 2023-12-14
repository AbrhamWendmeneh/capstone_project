 
# Task 2: Implement a simple registration form using state machines

import logging
from aiogram import Bot, Dispatcher, types, Router, F, html
import asyncio
import os
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import(ReplyKeyboardRemove,ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton)





load_dotenv('.env')
token=os.getenv('TOKEN_API')
bot= Bot(token)
dp=Dispatcher()
# form_router = Router()

# @dp.message(CommandStart())
# async def cmd_start(msg: types.Message):
#     await msg.answer('hello from task 2')
  
 
@dp.message(CommandStart())
async def cmd_start(msg: types.Message):
    await msg.answer(
        "hey!"
    )
    
@dp.message(Command("hello_world"))
async def cmd_hello(msg: types.Message):
    inline_keyboard= InlineKeyboardMarkup(row_width=2)
    button_yes= InlineKeyboardButton("Yes", callback_data="yes")
    button_no= InlineKeyboardButton("No",callback_data="no")
    inline_keyboard.add(button_yes, button_no)
    
    await msg.answer("Are you happy today?", reply_markup= inline_keyboard)
    
@dp.callback_query(lambda c: c.data in ['yes', 'no'])
async def process_callback(call: types.CallbackQuery):
    choice= call.data
    if choice=='yes':
        response_text="Great!"
    elif choice=='no':
        response_text="Oh no!, what happened?"
    await bot.send_message(call.from_user.id, response_text)
    await call.answer()

async def main():
    # dp.include_router(form_router)
    await dp.start_polling(bot)
    
if __name__== "__main__":
    asyncio.run(main())