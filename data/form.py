from aiogram.fsm.state import State, StatesGroup 

class Form(StatesGroup):
    
    user_id = State()
    rider_id = State()
    fullName = State()
    username = State()
    phone = State()
    role = State()
    registration_date = State()
    location = State()
    destination = State()
    confirm_booking = State() 
    edit_profile = State()