 
# Task 2: Implement a simple registration form using state machines

import logging
from aiogram import Bot, Dispatcher, types, Router, F
import asyncio
import os
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import(ReplyKeyboardRemove,ReplyKeyboardMarkup, KeyboardButton)


class Form:
    name= State()
    liked_bot= State()
    language= State()
    
load_dotenv('.env')
token= os.getenv('TOKEN_API_2')
bot= Bot(token)
dp=Dispatcher()


    