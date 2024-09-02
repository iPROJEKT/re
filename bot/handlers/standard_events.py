from typing import Callable, Type, Coroutine, Any, Optional

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from bot.core.state import EventState
from bot.core.utils import moscow_now
from bot.crud.crud_robot import (
    create_event,
    get_multi_model,
    get_multi_gaz,
    update_gaz,
    update_cryo,
    update_robot_component, get_all_diameter, get_all_wire_diameter, get_wire_name, get_gaz_name, get_tip_name,
    get_rolls_name, get_intestine_name, get_diffuser_name, get_mudguard_name, get_nozzle_name
)
from bot.crud.crud_user import get_user_by_id
from bot.models.base import AsyncSessionLocal, Base
from bot.models.defect_model import EventType
from bot.models.models import Wire, Gaz, Tip, Rolls, UserWAAMer, Intestine, Diffuser, Mudguard, Nozzle, MOSCOW_TZ

router = Router()


async def send_selection_menu(
    callback: CallbackQuery,
    model: Type[Base],
    item_text: Callable[[Base], str],
    callback_prefix: str,
    item_name: str,
):
    """
    Sends a selection menu with an inline keyboard for a given model.

    Args:
        callback (CallbackQuery): The CallbackQuery object representing the callback request.
        model (Type[Base]): SQLAlchemy model class used to retrieve items for the menu.
        item_text (Callable[[Base], str]):
        Function that takes a model instance and returns a string for the button text
        callback_prefix (str): Prefix used in the callback data for the buttons.
        item_name (str): Descriptive name for the menu, used in the prompt message.

    Returns:
        None
    """
    items = await get_multi_model(model=model)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=item_text(item), callback_data=f"{callback_prefix}_{item.id}")]
        for item in items
    ])
    await callback.message.edit_text(f"Выберите {item_name}:", reply_markup=markup)
    await callback.answer()


async def handle_item_selection(
    callback: CallbackQuery,
    state: FSMContext,
    item_key: str,
    state_name: str
):
    """
    Handles the selection of an item from the inline keyboard and prompts the user to enter a comment.

    Args:
        callback (CallbackQuery): The CallbackQuery object representing the callback request.
        state (FSMContext): The FSMContext object for managing conversation state.
        item_key (str): Key used to store the selected item's ID in the state.
        state_name (str): The state name to transition to, where the user will be prompted for a comment.

    Returns:
        None
    """
    item_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id
    await state.update_data({item_key: item_id, 'user_id': user_id})
    await callback.message.edit_text("Введите комментарий к событию:")
    await state.set_state(state_name)
    await callback.answer()


async def process_item_message(
        model_cost: Base,
        message: Message,
        state: FSMContext,
        update_function: Callable[[UserWAAMer, int, str, str, Optional[dict]], Coroutine[Any, Any, None]],
        event_message: str,
        item_key: str,
        component_field: str,
        update_time_field: str,
        extra_fields: Optional[dict] = None,
) -> None:
    user_message = message.text
    data = await state.get_data()
    item_id = data[item_key]
    user_id = data['user_id']
    user = await get_user_by_id(user_id)

    item_name = None
    if model_cost == Wire:
        item_name = await get_wire_name(item_id)
    elif model_cost == Tip:
        item_name = await get_tip_name(item_id)
    elif model_cost == Rolls:
        item_name = await get_rolls_name(item_id)
    elif model_cost == Intestine:
        item_name = await get_intestine_name(item_id)
    elif model_cost == Diffuser:
        item_name = await get_diffuser_name(item_id)
    elif model_cost == Mudguard:
        item_name = await get_mudguard_name(item_id)
    elif model_cost == Nozzle:
        item_name = await get_nozzle_name(item_id)

    async with AsyncSessionLocal() as session:
        if extra_fields:
            await update_function(
                user=user,
                component_id=item_id,
                component_field=component_field,
                update_time_field=update_time_field,
                extra_fields=extra_fields
            )
        else:
            await update_function(
                user=user,
                component_id=item_id,
                component_field=component_field,
                update_time_field=update_time_field,
            )

        additional_data = {
            "message": f"{event_message} на {item_name}",
            "user_message": user_message
        }
        await create_event(session, user.id, EventType.SETTING, additional_data, robot_id=user.number_robot)
        await message.answer(f"{event_message} обновлено и событие записано для {item_name}.")

    await state.clear()


@router.callback_query(F.data == 'replacement_wire')
async def replacement_wire(callback: CallbackQuery) -> None:
    items = await get_all_diameter(model=Wire)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=str(diameter), callback_data=f"diam_{diameter}")]
        for diameter in items
    ])
    await callback.message.edit_text("Выберите диаметр проволоки:", reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith("diam_"))
async def select_wire(callback: CallbackQuery) -> None:
    diam = float(callback.data.split("_")[1])
    wire_diam = await get_all_wire_diameter(diam)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=str(wire.wire_mark), callback_data=f"wire_{wire.id}")]
        for wire in wire_diam
    ])
    await callback.message.edit_text("Выберите проволоку:", reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith("wire_"))
async def handle_wire_selection(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_item_selection(callback, state, 'wire_id', EventState.waiting_for_user_message_wire)


@router.message(EventState.waiting_for_user_message_wire)
async def process_wire_message(message: Message, state: FSMContext) -> None:
    await process_item_message(
        model_cost=Wire,
        message=message,
        state=state,
        update_function=update_robot_component,
        event_message="Замена проволоки",
        item_key='wire_id',
        component_field='robot_wire_id',
        update_time_field='robot_last_update_wire',
        extra_fields={'robot_last_update_wire': moscow_now(MOSCOW_TZ)}
    )


# Handlers for nozzles
@router.callback_query(F.data == "replacement_tip")
async def replacement_nozzle(callback: CallbackQuery) -> None:
    await send_selection_menu(
        callback,
        Tip,
        lambda tip: f'{tip.tip_diameter} {tip.tip_type}',
        'tip',
        'наконечник'
    )


@router.callback_query(F.data.startswith("tip_"))
async def handle_nozzle_selection(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_item_selection(callback, state, 'tip_id', EventState.waiting_for_user_message_tip)


@router.message(EventState.waiting_for_user_message_tip)
async def process_nozzle_message(message: Message, state: FSMContext) -> None:
    await process_item_message(
        model_cost=Tip,
        message=message,
        state=state,
        update_function=update_robot_component,
        event_message="Замена наконечника",
        item_key='tip_id',
        component_field='robot_tip_id',
        update_time_field='robot_last_update_tip',
    )


# Handlers for rollers
@router.callback_query(F.data == 'replacement_rollers')
async def replacement_rollers(callback: CallbackQuery) -> None:
    await send_selection_menu(
        callback,
        Rolls,
        lambda roll: f'{roll.rolls_color} {roll.rolls_cutout_type} {roll.rolls_ware_dim}',
        'rollers',
        'ролики'
    )


@router.callback_query(F.data.startswith("rollers_"))
async def handle_rollers_selection(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_item_selection(callback, state, 'roll_id', EventState.waiting_for_user_message_roll)


@router.message(EventState.waiting_for_user_message_roll)
async def process_rollers_message(message: Message, state: FSMContext) -> None:
    await process_item_message(
        model_cost=Rolls,
        message=message,
        state=state,
        update_function=update_robot_component,
        event_message="Замена роликов",
        item_key='roll_id',
        component_field='robot_rolls_id',
        update_time_field='robot_last_update_rolls',
    )


@router.callback_query(F.data == 'replacement_gas_bottle')
async def choose_gas_type(callback: CallbackQuery) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Основной газ", callback_data="gas_type_main")],
        [InlineKeyboardButton(text="Дополнительный газ", callback_data="gas_type_auxiliary")]
    ])
    await callback.message.edit_text("Выберите тип газа для замены:", reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith("gas_type_"))
async def choose_gas(callback: CallbackQuery, state: FSMContext) -> None:
    gas_type = "Основной" if callback.data == "gas_type_main" else "Дополнительный"
    await state.update_data(gas_type=gas_type)
    gases = await get_multi_gaz(gaz_type='Баллон') if gas_type == "Дополнительный" else await get_multi_model(Gaz)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'{gas.gaz_name} {gas.gaz_type_obj}', callback_data=f"gas_{gas.id}")]
        for gas in gases
    ])
    await callback.message.edit_text(f"Выберите марку {gas_type.lower()} газа для замены:", reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith("gas_"))
async def handle_gas_selection(callback: CallbackQuery, state: FSMContext) -> None:
    gas_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id
    await state.update_data(gas_id=gas_id, user_id=user_id)
    await callback.message.edit_text("Введите комментарий к событию:")
    data = await state.get_data()
    gas_type = data.get('gas_type')
    if gas_type == "Основной":
        await state.set_state(EventState.waiting_for_user_message_main_gas)
    elif gas_type == "Дополнительный":
        await state.set_state(EventState.waiting_for_user_message_auxiliary_gas)
    await callback.answer()


@router.message(EventState.waiting_for_user_message_main_gas)
async def process_main_gas_message(message: Message, state: FSMContext) -> None:
    await process_gas_message(message, state, "Основной")


@router.message(EventState.waiting_for_user_message_auxiliary_gas)
async def process_auxiliary_gas_message(message: Message, state: FSMContext) -> None:
    await process_gas_message(message, state, "Дополнительный")


async def process_gas_message(message: Message, state: FSMContext, gas_type: str) -> None:
    user_message = message.text
    data = await state.get_data()
    gas_id = data['gas_id']
    user_id = data['user_id']
    user = await get_user_by_id(user_id)
    item_name = await get_gaz_name(gas_id)
    async with AsyncSessionLocal() as session:
        await update_gaz(user, gas_id, gas_type)
        additional_data = {"message": f"Замена {gas_type.lower()} газа на ID {item_name}", "user_message": user_message}
        await create_event(session, user.id, EventType.SETTING, additional_data, robot_id=user.number_robot)
        await message.answer(f"{gas_type} газ обновлен и событие записано.")
    await state.clear()


@router.callback_query(F.data == 'replacement_cryo_box')
async def replacement_cryo_box(callback: CallbackQuery) -> None:
    gases = await get_multi_gaz(gaz_type='Креобак')
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=gas.gaz_name, callback_data=f"cryo_box_gas_{gas.id}")]
        for gas in gases
    ])
    await callback.message.edit_text("Выберите марку газа для замены:", reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith("cryo_box_gas_"))
async def handle_cryo_box_selection(callback: CallbackQuery, state: FSMContext) -> None:
    parts = callback.data.split("_")
    if len(parts) != 4 or not parts[3].isdigit():
        await callback.answer("Неверный формат данных. Попробуйте снова.")
        return
    gas_id = int(parts[3])
    user_id = callback.from_user.id
    await state.update_data(gas_id=gas_id, user_id=user_id)
    await callback.message.edit_text("Введите комментарий к событию:")
    await state.set_state(EventState.waiting_for_user_message_cryo_box)
    await callback.answer()


@router.message(EventState.waiting_for_user_message_cryo_box)
async def process_cryo_box_message(message: Message, state: FSMContext) -> None:
    user_message = message.text
    data = await state.get_data()
    gas_id = data['gas_id']
    user_id = data['user_id']
    item_name = await get_gaz_name(gas_id)
    async with AsyncSessionLocal() as session:
        user = await get_user_by_id(user_id)
        await update_cryo(user, gas_id)
        additional_data = {"message": f"Замена креобака на газ ID {item_name}", "user_message": user_message}
        await create_event(session, user_id, EventType.SETTING, additional_data, robot_id=user.number_robot)
        await message.answer(f"Креобак обновлен и событие записано.")
    await state.clear()


@router.callback_query(F.data == 'replacement_channels')
async def replacement_channels(callback: CallbackQuery) -> None:
    await send_selection_menu(
        callback,
        Intestine,
        lambda intestine: f'{intestine.intestine_color} {intestine.intestine_diameter} {intestine.intestine_length}',
        'channels',
        'наплавляющий канал'
    )


@router.callback_query(F.data.startswith("channels_"))
async def handle_channels_selection(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_item_selection(callback, state, 'channels_id', EventState.waiting_for_user_message_intestine)


@router.message(EventState.waiting_for_user_message_intestine)
async def process_channels_message(message: Message, state: FSMContext) -> None:
    await process_item_message(
        model_cost=Intestine,
        message=message,
        state=state,
        update_function=update_robot_component,
        event_message="Замена направляющего канала",
        item_key='channels_id',
        component_field='robot_intestine_id',
        update_time_field='robot_last_update_intestine',
    )


@router.callback_query(F.data == 'replacement_diffuser')
async def replacement_diffuser(callback: CallbackQuery) -> None:
    await send_selection_menu(
        callback,
        Diffuser,
        lambda diffuser: f'{diffuser.diffuser_thread}',
        'diffuser',
        'Диффузор'
    )


@router.callback_query(F.data.startswith("diffuser_"))
async def handle_diffuser_selection(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_item_selection(callback, state, 'diffuser_id', EventState.waiting_for_user_message_diffuser)


@router.message(EventState.waiting_for_user_message_diffuser)
async def process_diffuser_message(message: Message, state: FSMContext) -> None:
    await process_item_message(
        model_cost=Diffuser,
        message=message,
        state=state,
        update_function=update_robot_component,
        event_message="Замена диффузора",
        item_key='diffuser_id',
        component_field='robot_diffuser_id',
        update_time_field='robot_last_update_diffuser',
    )


@router.callback_query(F.data == 'replacement_mudguard')
async def replacement_mudguard(callback: CallbackQuery) -> None:
    await send_selection_menu(
        callback,
        Mudguard,
        lambda mudguard: f'{mudguard.mudguard_material}',
        'mudguard',
        'Брызговик'
    )


@router.callback_query(F.data.startswith("mudguard_"))
async def handle_mudguard_selection(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_item_selection(callback, state, 'mudguard_id', EventState.waiting_for_user_message_mudguard)


@router.message(EventState.waiting_for_user_message_mudguard)
async def process_mudguard_message(message: Message, state: FSMContext) -> None:
    await process_item_message(
        model_cost=Mudguard,
        message=message,
        state=state,
        update_function=update_robot_component,
        event_message="Замена брызговика",
        item_key='mudguard_id',
        component_field='robot_mudguard_id',
        update_time_field='robot_last_update_mudguard',
    )


@router.callback_query(F.data == 'replacement_nozzle')
async def replacement_nozzle(callback: CallbackQuery) -> None:
    await send_selection_menu(
        callback,
        Nozzle,
        lambda nozzle: f'{nozzle.nozzle_form}',
        'nozzle',
        'Брызговик'
    )


@router.callback_query(F.data.startswith("nozzle_"))
async def handle_mudguard_selection(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_item_selection(callback, state, 'nozzle_id', EventState.waiting_for_user_message_nozzle)


@router.message(EventState.waiting_for_user_message_nozzle)
async def process_mudguard_message(message: Message, state: FSMContext) -> None:
    await process_item_message(
        model_cost=Nozzle,
        message=message,
        state=state,
        update_function=update_robot_component,
        event_message="Замена сопла",
        item_key='nozzle_id',
        component_field='robot_nozzle_id',
        update_time_field='robot_last_update_nozzle',
    )
