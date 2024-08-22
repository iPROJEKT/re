from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    name = State()
    surname = State()


class EventState(StatesGroup):
    waiting_for_user_message_wire = State()
    waiting_for_user_message_main_gas = State()
    waiting_for_user_message_auxiliary_gas = State()
    waiting_for_user_message_cryo_box = State()
    waiting_for_user_message_tip = State()
    waiting_for_user_message_roll = State()
    waiting_for_user_message_intestine = State()
    waiting_for_user_message_diffuser = State()
    waiting_for_user_message_mudguard = State()
    waiting_for_user_message_nozzle = State()
    waiting_for_user_message_defect = State()
    waiting_for_user_message_mechanical_fault = State()
    waiting_for_user_message_program_error = State()
    waiting_for_user_message_mode_deviation = State()
    waiting_for_user_message_gas_protection = State()


class CleaningState(StatesGroup):
    waiting_for_message = State()


class ErrorState(StatesGroup):
    waiting_for_error_message = State()
