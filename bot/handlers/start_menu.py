import logging
import random
from pathlib import Path

from aiogram.fsm.context import FSMContext
from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.core.const import START_MESSAGE_NOT_ALLOWED, START_MESSAGE, LIST_ANSWER
from bot.crud.crud_robot import get_all_user_name, get_brands_by_type, get_unique_types, update_consumable_count
from bot.crud.crud_user import get_user_by_id, is_admin
from bot.core.state import ShiftSupervisor, ConsumableStates
from bot.models.base import AsyncSessionLocal
from bot.models.models import Table

router = Router()


@router.message(F.text == 'Завершить сессию на роботе')
@router.message(F.text == 'В стартовое меню')
@router.message(CommandStart())
async def command_start(
        message: Message,
        state: FSMContext
) -> None:
    await state.clear()
    """
    Handles messages for session termination or starting a new session.

    Displays the main menu with different options based on user registration status.

    If the user is registered, shows the full menu with:
    - Register
    - Check robot status
    - Installation selection
    - Link to the table

    If the user is not registered, only shows options to:
    - Register
    - Check robot status
    """
    # Клавиатура для незарегистрированного пользователя
    unregistered_builder = ReplyKeyboardBuilder()
    unregistered_builder.row(KeyboardButton(text='Зарегистрироваться'))
    unregistered_builder.row(KeyboardButton(text='Узнать состояние роботов'))

    # Клавиатура для зарегистрированного пользователя
    user_builder = ReplyKeyboardBuilder()
    user_builder.row(KeyboardButton(text='Узнать состояние роботов'))
    user_builder.row(KeyboardButton(text='Выбор установки'))
    user_builder.row(KeyboardButton(text='Узнать состояние роботов'))

    # Клавиатура для администратора
    admin_builder = ReplyKeyboardBuilder()
    admin_builder.row(KeyboardButton(text='Узнать состояние роботов'))
    admin_builder.row(KeyboardButton(text='Выбор установки'))
    admin_builder.row(KeyboardButton(text='Администрирование'))
    admin_builder.row(KeyboardButton(text='Сайт с состояниями'))
    admin_builder.row(KeyboardButton(text='Добавление расходников'))

    # Проверка на администратора
    if await is_admin(message.from_user.id):
        await message.answer(
            START_MESSAGE,
            reply_markup=admin_builder.as_markup(resize_keyboard=True),
        )
    # Проверка на зарегистрированного пользователя
    elif await get_user_by_id(message.from_user.id):
        await message.answer(
            START_MESSAGE,
            reply_markup=user_builder.as_markup(resize_keyboard=True),
        )
    # Если пользователь не зарегистрирован
    else:
        await message.answer(
            START_MESSAGE_NOT_ALLOWED,
            reply_markup=unregistered_builder.as_markup(resize_keyboard=True),
        )


@router.message(F.photo)
async def photo(message: Message) -> None:
    """
    Responds to photo messages with a predefined image and caption.

    Sends a photo from the 'media' directory with a caption.
    """
    file_path = Path(__file__).parent.parent / 'media' / 'sh.jpg'

    if file_path.exists():
        await message.answer_photo(
            photo=types.FSInputFile(path=str(file_path)),
            caption='Смешно тебе, да? Я знаю что твоих рук дело'
        )
    else:
        await message.answer("Не удалось найти изображение.")


@router.message(F.video_note)
async def video_message(message: Message) -> None:
    """
    Responds to video notes with a predefined message.

    Sends a message indicating the user should get back to work.
    """
    await message.answer(
        'Ай красавец, иди работай'
    )


@router.message(F.video)
async def video(message: Message) -> None:
    """
    Responds to video messages with a predefined URL and a random choice from a list.

    Sends a message with a link to a Yandex Disk file and a random item from the `LIST_ANSWER`.
    """
    await message.answer(
        f'Заняться нечем?\n https://disk.yandex.ru/i/NbsdERZw36aCAw - завтра конспект по {random.choice(LIST_ANSWER)}'
    )


@router.message(F.content_type == 'voice')
async def audio_ans(message: Message) -> None:
    """
    Responds to voice messages with a predefined audio file.

    Sends an audio file from the 'media' directory.
    """
    file_path = Path(__file__).parent.parent / 'media' / 'WAAMmusic.mp3'

    if file_path.exists():
        await message.answer_audio(
            audio=types.FSInputFile(path=str(file_path))
        )
    else:
        await message.answer("Аудиофайл не найден.")


@router.message(F.text == 'Выбор установки')
async def user_get_robot(message: Message) -> None:
    """
    Presents the user with a choice of robot cells.

    Displays options to select between cell 1 and cell 2.
    """
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text='Ячейка 1'))
    builder.row(KeyboardButton(text='Ячейка 2'))
    await message.answer(
        'Выбирай',
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@router.message(F.text == 'Администрирование')
async def user_get_robot(message: Message) -> None:
    """
    Presents the user with a choice of robot cells based on their admin status.

    If the user is an administrator, they are provided with a link to the admin login page.
    Otherwise, a message indicating that they do not have immediate access is displayed.

    :param message: Message
        The message object containing details about the user and the incoming message text.
    :return: None
    """
    user_is_admin = await is_admin(message.from_user.id)
    print(user_is_admin)
    if user_is_admin:
        await message.answer(
            'http://192.168.20.184:8080/admin/login\n'
            'И помни! Большая база - большой дроп'
            'Большая сила - большая ответственность'
        )
    else:
        await message.answer(
           'Запомини одну фразу: "Все будет, но не сразу"'
        )


@router.message(F.text == 'Сайт с состояниями')
async def web_site(message: Message):
    await message.answer(
        'http://192.168.20.184:8080/'
    )


@router.message(F.text == 'Начальник смены')
async def shift_supervisor(message: Message, state: FSMContext):
    all_user = await get_all_user_name()
    builder = ReplyKeyboardBuilder()
    for user in all_user:
        builder.row(KeyboardButton(text=f'{user.name} {user.surname}'))
    await state.set_state(ShiftSupervisor.shift_supervisor)
    await message.answer(
        'Выбери своего Равшана',
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@router.message(ShiftSupervisor.shift_supervisor)
async def state_shift_supervisor(message: Message, state: FSMContext):
    await state.update_data(shift_supervisor=message.text)
    data = await state.get_data()

    # Допустим, данные сохраняются в таблицу смены
    shift_supervisor_name = data.get('shift_supervisor')

    # Добавление данных в базу через SQLAlchemy
    new_record = Table(shift_responsible=shift_supervisor_name)

    async with AsyncSessionLocal() as session:  # Используем асинхронную сессию
        async with session.begin():
            session.add(new_record)  # Добавляем запись
        await session.commit()  # Сохраняем изменения

    await message.answer(f'Начальник смены {shift_supervisor_name} успешно выбран.')
    await state.clear()
    await command_start(message)


@router.message(F.text == 'Добавление расходников')
async def add_consumable(message: Message, state: FSMContext):
    """
    Старт диалога добавления расходников.
    Пользователь выбирает тип расходника.
    """
    component_types = await get_unique_types()

    builder = ReplyKeyboardBuilder()
    for component_type in component_types:
        builder.row(KeyboardButton(text=component_type))
    builder.row(KeyboardButton(text="В стартовое меню"))

    await message.answer("Выберите тип расходника:", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(ConsumableStates.choose_type)


@router.message(ConsumableStates.choose_type)
async def choose_brand(message: Message, state: FSMContext):
    """
    Пользователь выбирает марку расходника в зависимости от типа.
    """
    component_type = message.text
    await state.update_data(consumable_type=component_type)

    brands = await get_brands_by_type(component_type)
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="В стартовое меню"))
    if brands:
        for brand, sub in brands:
            builder.row(KeyboardButton(text=f"{brand} {sub}"))

        await message.answer(
            f"Вы выбрали {component_type}. Теперь выберите марку:",
            reply_markup=builder.as_markup(
                resize_keyboard=True
            )
        )
        await state.set_state(ConsumableStates.choose_brand)
    else:
        await message.answer("Неверный выбор. Пожалуйста, выберите тип расходника.")
        await state.set_state(ConsumableStates.choose_type)


@router.message(ConsumableStates.choose_brand)
async def update_quantity(message: Message, state: FSMContext):
    """
    Пользователь вводит новое количество для выбранного расходника.
    """
    logging.info(f"Current state: {await state.get_state()}")  # Логирование состояния
    data = await state.get_data()
    component_type = data['consumable_type']

    selected_brand = message.text
    # Ограничиваем split только двумя частями
    mark, sub = selected_brand.split(maxsplit=1)

    await state.update_data(selected_brand=selected_brand)
    await message.answer(
        f"Вы выбрали {selected_brand}. Введите новое количество:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(ConsumableStates.update_quantity)


@router.message(ConsumableStates.update_quantity)
async def process_quantity_update(message: Message, state: FSMContext):
    """
    Обработка нового количества и обновление записи в базе данных.
    После этого переходим на выбор типа расходника (хендлер add_consumable).
    """
    new_quantity = message.text

    if new_quantity.isdigit():
        new_quantity = int(new_quantity)
        data = await state.get_data()
        component_type = data['consumable_type']
        mark, sub = data['selected_brand'].split(maxsplit=1)

        # Обновляем количество в базе данных
        updated_item = await update_consumable_count(component_type, mark, sub, new_quantity)

        if updated_item:
            await message.answer(
                f"Количество для {mark} {sub} обновлено до {new_quantity}.",
                reply_markup=types.ReplyKeyboardRemove()  # Убираем клавиатуру
            )
        else:
            await message.answer(
                f"Ошибка при обновлении количества для {mark} {sub}.",
                reply_markup=types.ReplyKeyboardRemove()  # Убираем клавиатуру в случае ошибки
            )
        await state.clear()  # Очищаем состояние после обновления

        # После обновления возвращаем пользователя к выбору типа расходника
        await add_consumable(message, state)

    else:
        await message.answer("Пожалуйста, введите корректное число.")
        await state.set_state(ConsumableStates.update_quantity)
