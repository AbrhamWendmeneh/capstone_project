 
# Task 2: Implement a simple registration form using state machines

import logging
from aiogram import Bot, Dispatcher, types, Router, F, html
import asyncio
import os
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import(ReplyKeyboardRemove,ReplyKeyboardMarkup, KeyboardButton)



class Form(StatesGroup):
    name = State()
    like_bots = State()
    language = State()

load_dotenv('.env')
token=os.getenv('TOKEN_API_2')
bot= Bot(token)
dp=Dispatcher()
form_router = Router()

# @dp.message(CommandStart())
# async def cmd_start(msg: types.Message):
#     await msg.answer('hello from task 2')
  
  
@form_router.message(CommandStart())
async def cmd_start(msg: types.Message, state: FSMContext):
    await state.set_state(Form.name)
    await msg.answer(
        "hi, what's your name?",
        reply_markup=ReplyKeyboardRemove()
    )

@form_router.message(Command("Cancel"))
@form_router.message(F.text.casefold()=="cancel")
async def cancel_handler(msg: types.Message, state: FSMContext):
    current_state= await state.get_state()
    if current_state is None:
        return
    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await msg.answer(
        "cacelled",
        reply_markup= ReplyKeyboardRemove()
    )
    
@form_router.message(Form.name)
async def process_name(msg: types.Message, state: FSMContext):
    await state.update_data(name= msg.text)
    await state.set_state(Form.like_bots)
    await msg.answer(
                        f"Nice to meet you, {html.quote(msg.text)}!\n Did you like to write bots?", 
                        
                        reply_markup=ReplyKeyboardMarkup(
                            
                            keyboard=[
                                        [ KeyboardButton(text='Yes'), 
                                        KeyboardButton(text='No')]
                                    ], 
                            resize_keyboard=True)
                    )

@form_router.message(Form.like_bots, F.text.casefold()=='yes')
async def process_like(msg: types.Message, state: FSMContext):
    await state.set_state(Form.language)
    await msg.reply(
        "That's nice, how many languages can you speak",
        reply_markup=ReplyKeyboardRemove()
    )
@form_router.message(Form.like_bots, F.text.casefold()=='no')
async def process_not_like(msg: types.Message, state: FSMContext):
    await state.set_state(Form.language)
    await msg.reply(
        "see you soon",
        reply_markup= ReplyKeyboardRemove()
    )
    
# This is for the case of the word which the user answer is not form the options given
@form_router.message(Form.like_bots)
async def unknown_text(msg: types.Message):
    await msg.reply(
        "I don't understand what you have written"
    )


async def main():
    dp.include_router(form_router)
    await dp.start_polling(bot)
    
if __name__== "__main__":
    asyncio.run(main())