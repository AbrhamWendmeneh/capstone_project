
from aiogram import types
from ..data.data_base import create_users_table, register_user, authenticate_user, get_user_data
create_users_table()

async def handle_registration(msg: types.Message, role:str):
    
    user= msg.from_user
    
    if not authenticate_user(user.phone):
        
        register_user(user, role)
        await msg.reply(f"Regsitration successful You are now a {role}")
        
    else:
        
        await msg.reply("you are already registered")
    
async def handle_authentication(msg: types.Message):
    
    user = msg.from_user
    authentication_status = authenticate_user(user.phone)
    
    if authentication_status:
        
        print('Authentication successful')
        user_data = get_user_data(user.phone)
        return True, user_data
        # await msg.reply("Authentication successful")
        
    else:
        
        print("Authentication failed, please Register First")
        return False,None
        
        # await msg.reply("Authentication failed, please Register First")
        
        
# async def handle_logout(msg: types.Message):
#     user= msg.from_user
