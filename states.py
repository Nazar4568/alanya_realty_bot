from aiogram.fsm.state import StatesGroup, State


class LeadForm(StatesGroup):
    choosing_lang = State()
    choosing_intent = State()
    waiting_for_free_text = State()

    missing_property_type = State()
    missing_districts = State()
    missing_price_range = State()

    waiting_for_contact = State()