from aiogram import types, Dispatcher, Bot
import asyncio
import os
from dotenv import load_dotenv



def main():
    load_dotenv('.env')
    token= os.getenv('TOKEN_API')
    bot= Bot(token)
