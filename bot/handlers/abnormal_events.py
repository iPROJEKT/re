from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.core.state import ErrorState
from bot.crud.crud_robot import create_event
from bot.crud.crud_user import get_user_by_id
from bot.models.base import AsyncSessionLocal
from bot.models.defect_model import EventType

router = Router()


async def handle_event_selection(callback: CallbackQuery, state: FSMContext, event_type: str) -> None:
    event_id = callback.data.split("_")[1]
    await state.update_data({
        f'{event_type}_id': event_id,
        'user_id': callback.from_user.id,
        'event_type': event_type
    })
    await callback.message.edit_text("Событие выбрано. Пожалуйста, введите полное описание события.")
    await state.set_state(ErrorState.waiting_for_error_message)
    await callback.answer()


async def process_event(callback: CallbackQuery, state: FSMContext, event_type: str) -> None:
    data = await state.get_data()
    event_id = data[f'{event_type}_id']
    user_id = data['user_id']
    user_message = data.get('user_message', '')

    async with AsyncSessionLocal() as session:
        event_message = {
            'defect': 'Дефект',
            'mechanical_fault': 'Механическая неисправность',
            'program_error': 'Ошибка программы',
            'mode_deviation': 'Отклонение от режима',
            'gas_protection': 'Проблема газовой защиты'
        }.get(event_type, 'Событие')

        # Detailed message including the event ID and user message
        detailed_message = f"{event_message} на ID {event_id}. Дополнительная информация: {user_message}"

        additional_data = {
            "message": detailed_message,
            "user_message": user_message
        }
        await create_event(session, user_id, EventType.SETTING, additional_data)
        await callback.message.answer(f"{event_message} обновлено и событие записано.")

    await state.clear()


@router.callback_query(F.data == "defect_deformations")
async def handle_defect_deformations(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_event_selection(callback, state, 'defect_deformations')


@router.callback_query(F.data == "defect_porosity")
async def handle_defect_porosity(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_event_selection(callback, state, 'defect_porosity')


@router.callback_query(F.data == "defect_unfused")
async def handle_defect_unfused(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_event_selection(callback, state, 'defect_unfused')


@router.callback_query(F.data == "defect_undercuts")
async def handle_defect_undercuts(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_event_selection(callback, state, 'defect_undercuts')


@router.callback_query(F.data == "defect_cracks")
async def handle_defect_cracks(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_event_selection(callback, state, 'defect_cracks')


@router.callback_query(F.data == "defect_burnthrough")
async def handle_defect_burnthrough(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_event_selection(callback, state, 'defect_burnthrough')


@router.callback_query(F.data == "defect_tip")
async def handle_defect_tip(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_event_selection(callback, state, 'defect_tip')


@router.callback_query(F.data == "mechanical_fault_1")
async def handle_mechanical_fault_1(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_event_selection(callback, state, 'mechanical_fault_1')


@router.callback_query(F.data == "program_error_collision")
async def handle_program_error_collision(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_event_selection(callback, state, 'program_error_collision')


@router.callback_query(F.data == "program_error_geometry_mismatch")
async def handle_program_error_geometry_mismatch(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_event_selection(callback, state, 'program_error_geometry_mismatch')


@router.callback_query(F.data == "program_error_premature_end")
async def handle_program_error_premature_end(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_event_selection(callback, state, 'program_error_premature_end')


@router.callback_query(F.data == "program_error_controller_error")
async def handle_program_error_controller_error(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_event_selection(callback, state, 'program_error_controller_error')


@router.callback_query(F.data == "mode_deviation_welding_control")
async def handle_mode_deviation_welding_control(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_event_selection(callback, state, 'mode_deviation_welding_control')


@router.callback_query(F.data == "mode_deviation_stability_violation")
async def handle_mode_deviation_stability_violation(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_event_selection(callback, state, 'mode_deviation_stability_violation')


@router.callback_query(F.data == "mode_deviation_arc_ignition_error")
async def handle_mode_deviation_arc_ignition_error(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_event_selection(callback, state, 'mode_deviation_arc_ignition_error')


@router.callback_query(F.data == "protection_low_pressure")
async def handle_protection_low_pressure(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_event_selection(callback, state, 'protection_low_pressure')


@router.callback_query(F.data == "protection_low_flow")
async def handle_protection_low_flow(callback: CallbackQuery, state: FSMContext) -> None:
    await handle_event_selection(callback, state, 'protection_low_flow')


@router.message(ErrorState.waiting_for_error_message)
async def handle_user_message(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user_message = message.text

    data = await state.get_data()
    event_type = data['event_type']

    async with AsyncSessionLocal() as session:
        event_message = {
            # Дефекты
            'defect_deformations': 'Деформации',
            'defect_porosity': 'Поры',
            'defect_unfused': 'Несплавления',
            'defect_undercuts': 'Подрезы',
            'defect_cracks': 'Трещины',
            'defect_burnthrough': 'Прожиг',
            'defect_tip': 'Заплавленый наконечник',

            # Механические неисправности
            'mechanical_fault_1': 'Не запустился контроллер',
            'mechanical_fault_2': 'Неизвестная механическая неисправность',
            # Добавьте соответствующее описание для 'mechanical_fault_2' здесь

            # Ошибки программы
            'program_error_collision': 'Коллизия',
            'program_error_geometry_mismatch': 'Несоответствие геометрии',
            'program_error_premature_end': 'Преждевременное окончание УП',
            'program_error_controller_error': 'Ошибка контроллера',

            # Отклонения от режима
            'mode_deviation_welding_control': 'Контроль сварки',
            'mode_deviation_stability_violation': 'Нарушение стабильности',
            'mode_deviation_arc_ignition_error': 'Ошибка зажигания дуги',

            # Проблемы газовой защиты
            'protection_low_pressure': 'Низкое давление газа',
            'protection_low_flow': 'Низкий расход газа'
        }.get(event_type, 'Событие')

        detailed_message = f"{event_message}"
        cell = await get_user_by_id(user_id)
        additional_data = {
            "message": detailed_message,
            "user_message": user_message
        }
        await create_event(session, cell.id, EventType.DEFECT, additional_data, robot_id=cell.number_robot)
        await message.answer(f"{event_message} обновлено и событие записано.")

    await state.clear()
