
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import(ReplyKeyboardRemove,ReplyKeyboardMarkup, KeyboardButton)
from ..data.data_base import update_user_profile
from ..data.form import Form

async def edit_profile_menu(msg: types.Message):

    menu_markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Edit Username")],
            [KeyboardButton(text="Edit Full Name")],
            [KeyboardButton(text="Edit Phone")],
        ],
        resize_keyboard=True
    )
    await msg.answer("Choose what you want to edit:", reply_markup=menu_markup)

#  This is for the name section 
async def edit_full_name(msg: types.Message, state: FSMContext):
    
    await msg.answer("Enter your new full name:")
    await Form.edit_full_name.set()  

async def process_new_full_name(msg: types.Message, state: FSMContext):
    
    new_full_name = msg.text.strip()
    user_data = await state.get_data()
    username = user_data.get('username')
    success = await update_user_profile(username, fullName=new_full_name)

    if success:
        
        await msg.answer(f"Your full name has been updated to {new_full_name}.")
        
    else:
        
        await msg.answer("Failed to update your full name. Please try again.")
 
    await state.clear()
    
# This is for the phone section 
async def edit_phone(msg: types.Message, state: FSMContext):
    
    await msg.answer("Enter your new phone number")
    await Form.edit_phone.set()
    
async def process_new_phone_number(msg: types.Message, state:FSMContext):
    
    new_phone= msg.text
    user_data= await state.get_data()
    phone=user_data.get('phone')
    success = await update_user_profile(phone, fullName=new_phone)
    
    if success:
        
        await msg.answer(f"Your phone has been updated to {new_phone}.")
        
    else:
        
        await msg.answer("failed to update phone")
        
    await state.clear()
    
# This is for the role section 
async def edit_role(msg: types.Message, state: FSMContext):
    
    await msg.answer("Enter your new phone number")
    await Form.edit_phone.set()
    
async def process_new_role(msg: types.Message, state:FSMContext):
    
    new_role= msg.text
    user_data= await state.get_data()
    role=user_data.get('role')
    success = await update_user_profile(role, fullName=new_role)
    
    if success:
        
        await msg.answer(f"Your phone has been updated to {new_role}.")
        
    else:
        
        await msg.answer("failed to update phone")
        
    await state.clear()

    

    
    
# This is for username section 

# async def edit_username(msg: types.Message, state: FSMContext):
#     await msg.answer("Enter your new phone number")
#     await Form.edit_username.set()
    
# async def process_new_username(msg: types.Message, state:FSMContext):
#     new_username= msg.text
#     user_data= await state.get_data()
#     username=user_data.get('username')
#     success = await update_user_profile(username, fullName=new_username)
#     if success:
#         await msg.answer(f"Your username has been updated to {new_username}.")
#     else:
#         await msg.answer("failed to update username")
#     await state.clear()