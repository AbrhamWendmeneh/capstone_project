 
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
from typing import Dict,Any





class Form(StatesGroup):
    fullName= State()
    gender= State()
    age=State()
    email=State()
    
load_dotenv('.env')
token=os.getenv('TOKEN_API_2')
bot= Bot(token)
dp=Dispatcher()
form_router = Router()
    
@form_router.message(CommandStart())
async def cmd_start(msg: types.Message, state_val: FSMContext):
    await state_val.set_state(Form.fullName)
    await msg.answer(
                    "hi, This is simple form for regitration, and write your name.",
                     reply_markup=ReplyKeyboardRemove()
                    )
    
    
@form_router.message(Command("Cancel"))
@form_router.message(F.text.casefold()=="cancel")
async def cancel_handler(msg: types.Message, state_val: FSMContext):
    current_state= await state_val.get_state()
    if current_state is None:
        return
    logging.info("Cancelling state %r", current_state)
    await state_val.clear()
    await msg.answer(
        "cacelled",
        reply_markup= ReplyKeyboardRemove()
    )
    
# This is to take values
@form_router.message(Form.fullName)
async def take_name(msg: types.Message, state_val:FSMContext):
    await state_val.update_data(fullName= msg.text)
    await state_val.set_state(Form.gender)
    await msg.answer(
                    f"hey,could you please choose your gender",
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=[
                                    [
                                        KeyboardButton(text="male"),
                                        KeyboardButton(text="Female")
                                        
                                    ]
                                ], resize_keyboard=True
                    )
                    )

#  This is for the case of the gender
@form_router.message(Form.gender)
async def take_gender(msg: types.Message, state_val:FSMContext):
    await state_val.update_data(gender= msg.text)
    await state_val.set_data(Form.age)
    await msg.answer(
        "could you please enter your age")
    
    

    
@form_router.message(Form.age)
async def take_age(msg: types.Message, state_val:FSMContext):
    await state_val.update_data(age=msg.text)
    await state_val.set_data(Form.email)
    await msg.answer(
        "could you please enter your email")
    
    
@form_router.message(Form.email)
async def take_email(msg: types.Message, state_val:FSMContext):
    result=await state_val.update_data(email= msg.text)
    await form_summary(msg= msg, result=result)
    
async def form_summary(msg: types.Message, result: Dict[str,Any]):
    fullName= result['fullName']
    gender= result['gender']
    age= result['age']
    email= result['email']
    
    summray= "Registration summary"
    summray+=f"your name {fullName.text}"
    summray+= f"your gender{ gender.text}"
    summray+=f"your age{ age.text}"
    summray+=f"your email address{email.text}"
    
    await msg.answer(summray, reply_markup= ReplyKeyboardRemove)
    
   
    
    
async def main():
    dp.include_router(form_router)
    await dp.start_polling(bot)
    
    
    
if __name__== "__main__":
    asyncio.run(main())
    