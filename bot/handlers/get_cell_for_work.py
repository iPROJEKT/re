from aiogram import Router, F
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from bot.crud.crud_user import get_user_by_id, cell_for_user


router = Router()


@router.message(F.text == 'Ячейка 1')
@router.message(F.text == 'Ячейка 2')
async def user_get_robot(message: Message) -> None:
    """
    Handles the user's selection of a cell (Ячейка 1 or Ячейка 2).

    Updates the user's cell information in the database and sends a menu to choose the type of events.
    """
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Штатные события")],
            [KeyboardButton(text="Нештатные события")],
            [KeyboardButton(text='В стартовое меню')]
        ],
        resize_keyboard=True
    )

    user_instance = await get_user_by_id(message.from_user.id)
    cell = 1 if message.text == 'Ячейка 1' else 2
    await cell_for_user(user_instance, cell)
    await message.answer("Выберите тип событий:", reply_markup=markup)


@router.message(F.text == "Штатные события")
async def process_standard_events(message: Message) -> None:
    """
    Displays a menu for standard events.

    Provides inline keyboard options for different categories of standard events such as replacements, cleaning,
    and setup.
    """
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Замены", callback_data="replacement")],
        [InlineKeyboardButton(text="Очистка", callback_data="cleaning")],
    ])
    await message.answer("Выберите категорию штатных событий:", reply_markup=markup)


@router.message(F.text == "Нештатные события")
async def process_non_standard_events(message: Message) -> None:
    """
    Displays a menu for non-standard events.

    Provides inline keyboard options for different categories of non-standard events such as defects,
    mechanical failures,
    program errors, mode deviations, and gas protection issues.
    """
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Дефекты", callback_data="defects")],
        [InlineKeyboardButton(text="Механические неисправности", callback_data="mechanical_failures")],
        [InlineKeyboardButton(text="Ошибка программы", callback_data="program_errors")],
        [InlineKeyboardButton(text="Отклонение от режима", callback_data="mode_deviation")],
        [InlineKeyboardButton(text="Нарушение газовой защиты", callback_data="gas_protection_issues")]
    ])
    await message.answer("Выберите категорию нештатных событий:", reply_markup=markup)


@router.callback_query(F.data == "replacement")
async def handle_replacement(callback: CallbackQuery) -> None:
    """
    Displays a menu for replacement events.

    Provides inline keyboard options for different types of replacements such as wire, gas bottle, cryo box, and more.
    """
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Замена проволоки", callback_data="replacement_wire")],
        [InlineKeyboardButton(text="Замена баллона", callback_data="replacement_gas_bottle")],
        [InlineKeyboardButton(text="Замена криобака", callback_data="replacement_cryo_box")],
        [InlineKeyboardButton(text="Замена наконечника", callback_data="replacement_tip")],
        [InlineKeyboardButton(text="Замена роликов", callback_data="replacement_rollers")],
        [InlineKeyboardButton(text="Замена каналов", callback_data="replacement_channels")],
        [InlineKeyboardButton(text="Замена диффузора", callback_data="replacement_diffuser")],
        [InlineKeyboardButton(text="Замена тефлонового брызговика", callback_data="replacement_mudguard")],
        [InlineKeyboardButton(text="Замена сопла", callback_data="replacement_nozzle")]
    ])
    await callback.message.edit_text("Выберите конкретную замену:", reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data == "cleaning")
async def handle_cleaning(callback: CallbackQuery) -> None:
    """
    Displays a menu for cleaning events.

    Provides inline keyboard options for different types of cleaning such as central nozzle, additional nozzle,
    and channel cleaning.
    """
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Очистка сопла центрального", callback_data="cleaning_central_nozzle")],
        [InlineKeyboardButton(text="Очистка сопла дополнительного", callback_data="cleaning_additional_nozzle")],
        [InlineKeyboardButton(text="Очистка канала (продувка)", callback_data="cleaning_channel")]
    ])
    await callback.message.edit_text("Выберите тип очистки:", reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data == "setup")
async def handle_setup(callback: CallbackQuery) -> None:
    """
    Displays a menu for setup events.

    Provides inline keyboard options for different types of setup such as UTool, UFRAME, and Register.
    """
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="UTool", callback_data="setup_utool")],
        [InlineKeyboardButton(text="UFRAME", callback_data="setup_uframe")],
        [InlineKeyboardButton(text="Register", callback_data="setup_register")]
    ])
    await callback.message.edit_text("Выберите настройку:", reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data == "defects")
async def handle_defects(callback: CallbackQuery) -> None:
    """
    Displays a menu for defect events.

    Provides inline keyboard options for different types of defects such as deformations, porosity, unfused areas,
    undercuts, cracks, and burnthrough.
    """
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Деформации", callback_data="defect_deformations")],
        [InlineKeyboardButton(text="Поры", callback_data="defect_porosity")],
        [InlineKeyboardButton(text="Несплавления", callback_data="defect_unfused")],
        [InlineKeyboardButton(text="Подрезы", callback_data="defect_undercuts")],
        [InlineKeyboardButton(text="Трещины", callback_data="defect_cracks")],
        [InlineKeyboardButton(text="Прожиг", callback_data="defect_burnthrough")],
        [InlineKeyboardButton(text="Заплавленый наконечник", callback_data="defect_tip")]
    ])
    await callback.message.edit_text("Выберите тип дефекта:", reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data == "mechanical_failures")
async def handle_mechanical_failures(callback: CallbackQuery) -> None:
    """
    Displays a menu for mechanical failure events.

    Provides inline keyboard options for different types of mechanical failures.
    """
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Не запустился контроллер", callback_data="mechanical_fault_1")],
    ])
    await callback.message.edit_text("Выберите тип механической неисправности:", reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data == "program_errors")
async def handle_program_errors(callback: CallbackQuery) -> None:
    """
    Displays a menu for program error events.

    Provides inline keyboard options for different types of program errors such as collision,
    geometry mismatch,
    premature end, and controller error.
    """
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Коллизия", callback_data="program_error_collision")],
        [InlineKeyboardButton(text="Несоответствие геометрии", callback_data="program_error_geometry_mismatch")],
        [InlineKeyboardButton(text="Преждевременное окончание УП", callback_data="program_error_premature_end")],
        [InlineKeyboardButton(text="Ошибка контроллера", callback_data="program_error_controller_error")]
    ])
    await callback.message.edit_text("Выберите тип ошибки программы:", reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data == "mode_deviation")
async def handle_mode_deviation(callback: CallbackQuery) -> None:
    """
    Displays a menu for mode deviation events.

    Provides inline keyboard options for different types of mode deviations such as welding control, stability
    violation, and arc ignition error.
    """
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Контроль сварки", callback_data="mode_deviation_welding_control")],
        [InlineKeyboardButton(text="Нарушение стабильности", callback_data="mode_deviation_stability_violation")],
        [InlineKeyboardButton(text="Ошибка зажигания дуги", callback_data="mode_deviation_arc_ignition_error")]
    ])
    await callback.message.edit_text("Выберите тип отклонения от режима:", reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data == "gas_protection_issues")
async def handle_gas_protection_issues(callback: CallbackQuery) -> None:
    """
    Displays a menu for gas protection issues.

    Provides inline keyboard options for different types of gas protection issues such as low pressure and low flow.
    """
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Низкое давление газа", callback_data="protection_low_pressure")],
        [InlineKeyboardButton(text="Низкий расход газа", callback_data="protection_low_flow")]
    ])
    await callback.message.edit_text("Выберите тип нарушения газовой защиты:", reply_markup=markup)
    await callback.answer()
