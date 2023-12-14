from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import hbold
from aiogram import types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import datetime
from main import get_driver_ids,form_router
from ..data.form import Form
from ..data.data_base import  get_accepted_driver_id, get_driver_details, get_history_details, get_users_role, insert_rides, is_ride_pending, update_accepted_driver_id, update_ride_status
# from aiogram.filters import

# MyCallback is a class that generates callback_data
class MyCallback:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def pack(self):
        return {'name': self.name, 'id': self.id}

def generate_menu(options):
    
    # Generate InlineKeyboardMarkup based on the options
    menu = InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton(text=option['text'], callback_data=MyCallback(**option['callback']).pack())] for option in options
    ])
    
    return menu

def generate_registration_menu():
    
    options = [{'text': 'Registration', 'callback': {'action_name': 'registration', 'action_id': '0', 'authenticated': False}}]
    
    menu = InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton(text = option['text'], callback_data=MyCallback(**option['callback']).pack())] for option in options
    ])
    
    return menu
    

async def send_welcome_menu(msg, role):
    
    if role == 'passenger':
        
        options = [
                    {'text': 'Profile', 'callback': {'action_name': 'profile', 'action_id': '0'}}, 
                    {'text': 'History', 'callback': {'action_name': 'history', 'action_id': '1'}}, 
                    {'text': 'Driver Matching', 'callback': {'action_name': 'match', 'action_id': '2'}},
                    {'text': 'Rate Driver', 'callback': {'action_name': 'rate', 'action_id': '3'}},
                    {'text': 'Book Ride', 'callback': {'action_name': 'ride', 'action_id': '4'}},
                    {'text': 'Edit Profile', 'callback': {'action_name': 'edit_profile', 'action_id': '11'}},
                ]
    
    elif role == 'driver':
        
        options = [
            {'text': 'List Books', 'callback': {'action_name': 'list_books', 'action_id': '5'}},
            {'text': 'Active Books', 'callback': {'action_name': 'active_books', 'action_id': '6'}},
            {'text': 'Set Status', 'callback': {'action_name': 'set_status', 'action_id': '7'}},
            {'text': 'View Book History', 'callback': {'action_name': 'view_history', 'action_id': '8'}},
            {'text': 'Edit Profile', 'callback': {'action_name': 'edit_profile', 'action_id': '9'}},
            {'text': 'Review', 'callback': {'action_name': 'review', 'action_id': '10'}},
        ]
        
    else:
        
        options = []

    menu = generate_menu(options)
    await msg.answer(f"{hbold('Welcome to Ride Healing Bot 🚖')}!\n\nSteer your ride! Where would you like to go?😎\nSelect from features ..  ", reply_markup=menu) 

# This is for the case of the sending accepted and rejected message for the users
async def get_driver_ids():
    return get_users_role('driver')

async def send_booking(msg: types.Message, dp , fullName, phone, location,destination):
    
    options = [
                    {'text': 'Accept', 'callback': {'action_name': 'accept',}}, 
                    {'text': 'Reject', 'callback': {'action_name': 'reject', }}, 
              ]
    menu = generate_menu(options)

    driver_ids= await get_driver_ids()
    
    for driver_id in driver_ids:
        await msg.bot.send_message(
                                    driver_id, 
                                    f"New ride request from 
                                    \n{fullName}
                                    \n{phone}
                                    \n{location}
                                    \n{destination}"
                                    ,reply_markup=menu
                                  )
    insert_rides(msg.from_user.id, location, destination,datetime.datetime.now(), None,'pending')
        # await dp.bot.send_message(driver_id, f"New ride request from user this is left for future case.", reply_markup=menu)

async def notify_passenger(msg: types.Message,passenger_id, driver_id):
    
    driver_details = get_driver_details(driver_id)
    
    if driver_details:
        
        fullName, phone = driver_details
        await msg.bot.send_message(f"Your ride has been accepted by {fullName} ({phone}).")
        
    else:
        # Handle the case where driver details are not found
        await msg.bot.send_message(passenger_id, "Sorry, we couldn't retrieve driver details.")
  
@form_router.callback_query_handler(lambda callback_query: 'action_name' in callback_query.data and callback_query.data['action_name'] == 'accept')
async def accept_ride_callback(callback_query):
    
    ride_id = callback_query.data['ride_id']
    driver_id = callback_query.from_user.id
    
    if await is_ride_pending(ride_id):
        
        await update_ride_status(ride_id, driver_id, "accepted")
        accepted_driver_id = get_accepted_driver_id(ride_id)
        
        if accepted_driver_id:
            
            update_accepted_driver_id(ride_id, driver_id)
            
        await notify_passenger(callback_query.from_user.id, driver_id)
        
        # To do 
        # Notify other drivers that the ride has been accepted
    else:
        await callback_query.answer("Sorry, this ride has already been accepted or rejected.")

@form_router.callback_query_handler(lambda callback_query: callback_query.data['action_name'] == 'history')
async def handle_history_callback(callback_query):
    
    user_id = callback_query.from_user.id
    history_details = get_history_details(user_id)
    
    if history_details:
        
        formatted_history = "\n".join([f"{start_location}to {destination}" for start_location, destination in history_details])
        await callback_query.message.answer(f"Your ride history:\n{formatted_history}")
        
    else:
        
        await callback_query.message.answer("No ride history available.")
        
        
# @form_router.callback_query(lambda callback_query:callback_query.data['action_name']=='rate')
# async def rate_driver_callback(callback_query):
#     user