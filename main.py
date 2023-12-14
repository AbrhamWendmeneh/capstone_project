import logging
from aiogram import types, Dispatcher, Bot, F, Router
from aiogram.filters import CommandStart, Command
import asyncio
import os
from aiogram.types import  Message
from aiogram.types import(ReplyKeyboardRemove,ReplyKeyboardMarkup, KeyboardButton)
from dotenv import load_dotenv
from handlers.user_profile_handler import handle_authentication
from aiogram.fsm.context import FSMContext
from .data.models import User
from .data.data_base import authenticate_user, get_user_data,register_user
from .data.form import Form
from .handlers.callbacks import generate_registration_menu, send_welcome_menu, send_booking
from .handlers.edit_profile_handler import edit_profile_menu



load_dotenv('.env')

token =  os.getenv('TOKEN_API')

bot =  Bot(token)

dp =  Dispatcher()

form_router =  Router()


# the first thing in the start command
@form_router.message(CommandStart())
async def cmd_start(msg: types.Message, state: FSMContext):
    
    user = msg.from_user
    authentication_status, user_data = await handle_authentication(msg)
    
    if authentication_status:
        
        role = user_data['role']
        
        if role == 'passenger':
            
            await msg.answer(f"Welcome back, {user_data['name']}! What would you like to do today?",reply_markup = send_welcome_menu(user,role))
            
            # await send_welcome_menu(user,role)
        elif role == 'driver':
            
            await msg.answer(f"Welcome back, {user_data['name']}! What would you like to do today?", reply_markup =  await send_welcome_menu(user, role))
            # await send_welcome_menu(user, role)
 
        # await send_welcome_menu(user)
        
    else:
        await state.set_state(Form.fullName)
        
        await msg.answer(f"Hi{user}, Welcome to Ethio Ride Bot 🚖!\nPlease register to continue.", reply_markup =  generate_registration_menu())
   
#  This is for the case of if the user clicks the cancel command
@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(msg: Message, state: FSMContext) -> None:
    
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await msg.answer(
        "Cancelled.",
        reply_markup = ReplyKeyboardRemove(),
    )

#  This is for the update profile command
@dp.message(Command('update_profile'))
async def update_cmd(msg: types.Message):
    
    user = msg.from_user
    await edit_profile_menu(user)
    await Form.edit_profile.set()

#  This for the case of the handle booking when the user clicks the keyboard button in the callback file
@form_router.message(Form.location)
async def handle_location(msg: types.Message, state = FSMContext):
    
    state.update_data(location = msg.location)
    state.set_data(Form.destination)
    location_reply =  ReplyKeyboardMarkup(
            keyboard = [[KeyboardButton(text = "share your location",request_location = True)]],resize_keyboard=True),
    
    await msg.answer("your location is shared", location_reply)  
    
@form_router.message(Form.destination)
async def handle_destination(msg: types.Message, state=FSMContext):
    
    location = state.get_data().get('location')
    destination = msg.text
    state.update_data(destination)
    state.set_state(Form.destination)
    destination_reply = ReplyKeyboardMarkup(
        keyboard = [[KeyboardButton(text = "this is your destination"),destination_reply]],resize_keyboard =  True
    )
    user_value = get_user_data()
    _,_, fullName, phone,_,_,_ = user_value
    await send_booking(dp, fullName, phone, location, destination)
    
    state.clear()


    

    
    





# @dp.message(Command("register"))
# async def register_cmd(msg: types.Message,  ):
#     role_val =  msg.get_args() or 'passenger'
#     await handle_registration(msg, role = role_val)
    
    
# @dp.message(Command('login'))
# async def login_cmd(msg: types.Message):
#     await handle_authentication(msg)
    

    
    
    
    
@form_router.message(Form.fullName)
async def handle_name(msg: types.Message, state:FSMContext):
    state.update(fullName =  msg.text)
    state.set_state(Form.username)
    username_reply =  ReplyKeyboardMarkup(
        keyboard = [[KeyboardButton(text = "share your username", request_use = True)]], resize_keyboard = True
    )
    await msg.answer('your name is successfully registered, please share your user name', reply_markup =  username_reply)

    
@form_router.message(Form.username)
async def take_username(msg: types.Message, state:FSMContext):
    state.update(username =  msg.text)
    state.set_state(Form.phone)
    phone_reply =  ReplyKeyboardMarkup(
        keyboard = [[KeyboardButton(text = "share your contact",request_contact =  True)]], resize_keyboard = True
    )
    
    await msg.answer('your use name is registered, please share your phone number', reply_markup = phone_reply)
    


@form_router.message(Form.phone)
async def handle_phone(msg: types.Message, state:FSMContext):
    state.update(phone =  msg.text)
    state.set_state(Form.role)
    role_reply =  ReplyKeyboardMarkup(
        keyboard = [[KeyboardButton(text = "passenger"),KeyboardButton(text = "driver"),]],resize_keyboard = True
    )
    await msg.answer("you shared your role, please share your..",reply_markup = role_reply)
 
 
@form_router.message(Form.role)
async def handle_role(msg: types.Message, state:FSMContext):
    state.update_data(role = msg.text)
    user_data =  await state.get_data()
    await register_user_in_database(user_data)
    await state.clear()
    await msg.answer(f"You are registered as a {user_data['role']}! Welcome to the community.")

    
    
async def register_user_in_database(user_data):
    user  = User(
        username =  user_data.get('username'),
        fullName = user_data.get('fullName'),
        phone = user_data.get('phone'),
        role = user_data.get('role')
    )
    if not await authenticate_user(user.phone):
        await register_user(user, user_data['role'])
    else:
        print('you have already account ')
    


    



async def main():
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
    
    
    
    
    
    
    
    
 
    

