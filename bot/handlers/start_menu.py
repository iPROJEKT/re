import random
from pathlib import Path

from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.core.const import START_MESSAGE_NOT_ALLOWED, START_MESSAGE, LIST_ANSWER
from bot.crud.crud_user import get_user_by_id, is_admin

router = Router()


@router.message(F.text == 'Завершить сессию на роботе')
@router.message(F.text == 'В стартовое меню')
@router.message(CommandStart())
async def command_start(
        message: Message,
) -> None:
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
    builder_1 = ReplyKeyboardBuilder()
    builder = ReplyKeyboardBuilder()
    builder_1.row(KeyboardButton(text='Зарегистрироваться'))
    builder_1.row(KeyboardButton(text='Узнать состояние роботов'))
    builder.row(KeyboardButton(text='Выбор установки'))
    builder.row(KeyboardButton(text='Узнать состояние роботов'))
    builder.row(KeyboardButton(text='Администрирование Красносельского района'))
    builder.row(KeyboardButton(text='Сайт с состояниями'))

    if await get_user_by_id(message.from_user.id):
        await message.answer(
            START_MESSAGE,
            reply_markup=builder.as_markup(resize_keyboard=True),
        )
    else:
        await message.answer(
            START_MESSAGE_NOT_ALLOWED,
            reply_markup=builder_1.as_markup(resize_keyboard=True),
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


@router.message(F.text == 'Администрирование Красносельского района')
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
            'http://192.168.20.152:8080/admin/login\n'
            'И помни! Большая база - большой дроп'
            'Большая сила - большая ответственность'
        )
    else:
        await message.answer(
           'Запомини одну фразу: "Все будет, но не сразу"'
        )


@router.message(F.text == 'Сайт с состояниями')
async def web_site(m: Message):
    await m.answer(
        'http://192.168.20.152:8080/'
    )
