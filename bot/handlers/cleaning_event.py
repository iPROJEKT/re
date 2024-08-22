from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.models.base import AsyncSessionLocal
from bot.crud.crud_clear import clear_robot_component
from bot.crud.crud_robot import create_event
from bot.crud.crud_user import get_user_by_id
from bot.models.defect_model import EventType

router = Router()


async def perform_cleaning_operation(component: str, user_id: int):
    async with AsyncSessionLocal() as session:
        user = await get_user_by_id(user_id)

        if component == 'central_nozzle':
            await clear_robot_component(user, 'robot_clear_nozzle')
            message = 'Очистка центрального сопла завершена.'
        elif component == 'additional_nozzle':
            await clear_robot_component(user, 'robot_clear_add_nozzle')
            message = 'Очистка дополнительного сопла завершена.'
        elif component == 'channels':
            await clear_robot_component(user, 'robot_clear_intestine')
            message = 'Очистка канала завершена.'

        await create_event(
            session=session,
            user_id=user.id,
            event_type=EventType.CLEANING,
            additional_data={
                'message': message,
                'user_message': ''
            },
            robot_id=user.number_robot
        )


@router.callback_query(F.data == 'cleaning_central_nozzle')
async def cleaning_central_nozzle(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    await perform_cleaning_operation('central_nozzle', user_id)
    await callback.message.answer('Успех')


@router.callback_query(F.data == 'cleaning_additional_nozzle')
async def cleaning_additional_nozzle(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    await perform_cleaning_operation('additional_nozzle', user_id)
    await callback.message.answer('Успех')


@router.callback_query(F.data == 'cleaning_channel')
async def cleaning_channels(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    await perform_cleaning_operation('channels', user_id)
    await callback.message.answer('Успех')
