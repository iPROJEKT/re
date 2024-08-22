from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.core.state import UserState
from bot.crud.crud_user import create_user

from bot.handlers.start_menu import command_start

router = Router()


@router.message(F.text == 'Зарегистрироваться')
async def create_user_state_first(
    message: Message,
    state: FSMContext
) -> None:
    await state.set_state(UserState.name)
    await message.answer(
        "Напиши свое Имя",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(UserState.name)
async def create_user_state_name(
    message: Message,
    state: FSMContext
) -> None:
    if len(message.text.split()) != 1 or not message.text.isalpha():
        await message.answer(
            "Нужно только имя",
            reply_markup=ReplyKeyboardRemove(),
        )
        return
    await state.update_data(name=message.text)
    await state.set_state(UserState.surname)
    await message.answer(
        "Напиши свою Фамилию",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(UserState.surname)
async def create_user_state_surname(
    message: Message,
    state: FSMContext
) -> None:
    if len(message.text.split()) != 1 or not message.text.isalpha():
        await message.answer(
            "Нужна только фамилия",
            reply_markup=ReplyKeyboardRemove(),
        )
        return
    await state.update_data(surname=message.text)
    data = await state.get_data()
    await create_user(
        telegram_user_id=message.from_user.id,
        name=data.get('name'),
        surname=data.get('surname')
    )
    await state.clear()
    await message.answer(
        "Регистрация прошла успешно",
        reply_markup=ReplyKeyboardRemove(),
    )
    await command_start(message)
