import re
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, CallbackQuery, InlineKeyboardMarkup,
    InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
)
from aiogram.fsm.context import FSMContext

from states import LeadForm
from locales import TEXTS, DISTRICTS
from services.llm_parser import parse_user_query
from database.engine import save_lead_to_db
from services.n8n_webhook import send_lead_to_n8n

router = Router()



def get_lang_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇺🇦 Українська", callback_data="lang_uk"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en"),
        ]
    ])


def get_intent_kb(lang: str) -> InlineKeyboardMarkup:
    t = TEXTS[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["btn_buy"], callback_data="intent_buy")],
        [InlineKeyboardButton(text=t["btn_sell"], callback_data="intent_sell")]
    ])


def get_free_text_kb(lang: str) -> InlineKeyboardMarkup:
    t = TEXTS[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["btn_manual_mode"], callback_data="mode_manual")]
    ])


def get_property_type_kb(lang: str) -> InlineKeyboardMarkup:
    t = TEXTS[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t["prop_apartment"], callback_data="prop_apartment"),
            InlineKeyboardButton(text=t["prop_house"], callback_data="prop_house"),
            InlineKeyboardButton(text=t["prop_villa"], callback_data="prop_villa"),
        ]
    ])


def get_districts_kb(lang: str, selected: list[str]) -> InlineKeyboardMarkup:
    t = TEXTS[lang]
    buttons = []
    row = []
    for d in DISTRICTS:
        mark = "✅ " if d in selected else ""
        row.append(InlineKeyboardButton(text=f"{mark}{d}", callback_data=f"dist_{d}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    if selected:
        buttons.append([InlineKeyboardButton(text=t["btn_done_districts"], callback_data="dist_done")])
    buttons.append([InlineKeyboardButton(text=t["btn_skip_districts"], callback_data="dist_skip")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_price_kb(lang: str) -> InlineKeyboardMarkup:
    t = TEXTS[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t["price_under_70k"], callback_data="price_0_70000"),
            InlineKeyboardButton(text=t["price_70k_120k"], callback_data="price_70000_120000"),
        ],
        [
            InlineKeyboardButton(text=t["price_120k_200k"], callback_data="price_120000_200000"),
            InlineKeyboardButton(text=t["price_over_200k"], callback_data="price_200000_1000000"),
        ]
    ])


def get_summary_edit_kb(lang: str) -> InlineKeyboardMarkup:
    t = TEXTS[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["btn_edit_lead"], callback_data="edit_lead")]
    ])


def get_contact_kb(lang: str) -> ReplyKeyboardMarkup:
    t = TEXTS[lang]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t["btn_share_contact"], request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )



async def route_next_missing_field(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    t = TEXTS[lang]

    if not data.get("property_type"):
        await state.set_state(LeadForm.missing_property_type)
        await message.answer(t["ask_property_type"], reply_markup=get_property_type_kb(lang))
        return

    if data.get("districts") is None:
        await state.set_state(LeadForm.missing_districts)
        await state.update_data(temp_districts=[])
        await message.answer(t["ask_districts"], reply_markup=get_districts_kb(lang, []))
        return

    if data.get("min_price") is None or data.get("max_price") is None:
        await state.set_state(LeadForm.missing_price_range)
        await message.answer(t["ask_price"], reply_markup=get_price_kb(lang))
        return

    await state.set_state(LeadForm.waiting_for_contact)

    intent_label = t["btn_buy"] if data.get("intent") == "buy" else t["btn_sell"]
    prop_map = {
        "apartment": t["prop_apartment"],
        "house": t["prop_house"],
        "villa": t["prop_villa"]
    }
    prop_label = prop_map.get(data.get("property_type"), data.get("property_type"))
    districts_list = data.get("districts", [])
    districts_str = ", ".join(districts_list) if districts_list else "Any"
    price_str = f"€{data['min_price']:,} – €{data['max_price']:,}"

    summary = t["summary_card"].format(
        intent=intent_label,
        prop_type=prop_label,
        districts=districts_str,
        price=price_str
    )
    await message.answer(summary, reply_markup=get_summary_edit_kb(lang))
    await message.answer(t["ask_contact_prompt"], reply_markup=get_contact_kb(lang))



@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(LeadForm.choosing_lang)
    await message.answer(TEXTS["ru"]["welcome"], reply_markup=get_lang_kb())


@router.callback_query(LeadForm.choosing_lang, F.data.startswith("lang_"))
async def process_lang(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split("_")[1]
    await state.update_data(lang=lang)
    await state.set_state(LeadForm.choosing_intent)
    await callback.message.edit_text(TEXTS[lang]["choose_intent"], reply_markup=get_intent_kb(lang))
    await callback.answer()


@router.callback_query(LeadForm.choosing_intent, F.data.startswith("intent_"))
async def process_intent(callback: CallbackQuery, state: FSMContext):
    intent = callback.data.split("_")[1]
    data = await state.get_data()
    lang = data.get("lang", "ru")

    await state.update_data(intent=intent)
    await state.set_state(LeadForm.waiting_for_free_text)
    await callback.message.edit_text(
        TEXTS[lang]["free_text_prompt"],
        reply_markup=get_free_text_kb(lang)
    )
    await callback.answer()


@router.callback_query(LeadForm.waiting_for_free_text, F.data == "mode_manual")
async def process_manual_mode(callback: CallbackQuery, state: FSMContext):
    await state.update_data(
        raw_query="Заполнено по шагам (без ИИ)",
        property_type=None,
        districts=None,
        min_price=None,
        max_price=None
    )
    await callback.message.delete()
    await route_next_missing_field(callback.message, state)
    await callback.answer()


@router.message(LeadForm.waiting_for_free_text, F.text)
async def process_free_text(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")

    status_msg = await message.answer(TEXTS[lang]["analyzing"])
    extracted = await parse_user_query(message.text)
    await status_msg.delete()

    await state.update_data(
        raw_query=message.text,
        property_type=extracted.property_type,
        districts=extracted.districts,
        min_price=extracted.min_price_eur,
        max_price=extracted.max_price_eur
    )
    await route_next_missing_field(message, state)


@router.callback_query(LeadForm.missing_property_type, F.data.startswith("prop_"))
async def process_missing_prop(callback: CallbackQuery, state: FSMContext):
    prop_type = callback.data.split("_")[1]
    await state.update_data(property_type=prop_type)
    await callback.message.delete()
    await route_next_missing_field(callback.message, state)
    await callback.answer()


@router.callback_query(LeadForm.missing_districts, F.data.startswith("dist_"))
async def process_missing_districts(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    data = await state.get_data()
    lang = data.get("lang", "ru")
    selected: list = data.get("temp_districts", [])

    if action == "skip":
        await state.update_data(districts=["Any"])
        await callback.message.delete()
        await route_next_missing_field(callback.message, state)
    elif action == "done":
        await state.update_data(districts=selected if selected else ["Any"])
        await callback.message.delete()
        await route_next_missing_field(callback.message, state)
    else:
        if action in selected:
            selected.remove(action)
        else:
            selected.append(action)
        await state.update_data(temp_districts=selected)
        await callback.message.edit_reply_markup(reply_markup=get_districts_kb(lang, selected))
    await callback.answer()


@router.callback_query(LeadForm.missing_price_range, F.data.startswith("price_"))
async def process_missing_price_btn(callback: CallbackQuery, state: FSMContext):
    _, min_p, max_p = callback.data.split("_")
    await state.update_data(min_price=int(min_p), max_price=int(max_p))
    await callback.message.delete()
    await route_next_missing_field(callback.message, state)
    await callback.answer()


@router.message(LeadForm.missing_price_range, F.text)
async def process_missing_price_text(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")

    clean_text = message.text.lower().replace("к", "000").replace("k", "000").replace(" ", "")
    numbers = [int(n) for n in re.findall(r"\d+", clean_text)]

    if not numbers:
        await message.answer(TEXTS[lang]["price_error"], reply_markup=get_price_kb(lang))
        return

    if len(numbers) == 1:
        min_p, max_p = numbers[0], numbers[0]
    else:
        min_p, max_p = min(numbers[0], numbers[1]), max(numbers[0], numbers[1])

    await state.update_data(min_price=min_p, max_price=max_p)
    await route_next_missing_field(message, state)


@router.callback_query(LeadForm.waiting_for_contact, F.data == "edit_lead")
async def process_edit_lead(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")

    await state.set_data({"lang": lang})
    await state.set_state(LeadForm.choosing_intent)

    await callback.message.delete()
    await callback.message.answer("🔄", reply_markup=ReplyKeyboardRemove())
    await callback.message.answer(TEXTS[lang]["choose_intent"], reply_markup=get_intent_kb(lang))
    await callback.answer()


@router.message(LeadForm.waiting_for_contact)
async def process_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")

    phone = message.contact.phone_number if message.contact else message.text
    await state.update_data(
        phone=phone,
        username=message.from_user.username,
        telegram_id=message.from_user.id
    )

    final_data = await state.get_data()
    saved_lead = await save_lead_to_db(final_data)
    await send_lead_to_n8n(saved_lead)

    await message.answer(TEXTS[lang]["thank_you"], reply_markup=ReplyKeyboardRemove())
    await state.clear()