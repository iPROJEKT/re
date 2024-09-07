from aiogram import Router, F
from aiogram.types import Message

from bot.crud.crud_robot import get_multi_robot

router = Router()


@router.message(F.text == 'Узнать состояние роботов')
async def robot_state_menu(message: Message) -> None:
    """
    Responds to a request for the current state of robots.

    This handler fetches the robot data from the database using `get_multi_robot`,
    and then sends detailed information about each robot's state to the user.

    The information includes:
    - Robot cell number (номер ячейки)
    - Wire details (mark and diameter) (марка и диаметр проволоки)
    - Last wire replacement (последняя замена проволоки)
    - Main gas details (name and type) (основной газ: название и тип)
    - Last main gas replacement (последняя замена основного газа)
    - Additional gas details (name and type) (дополнительный газ: название и тип)
    - Last additional gas replacement (последняя замена дополнительного газа)
    - Tip details (diameter and type) (наконечник: диаметр и тип)
    - Last tip replacement (последняя замена наконечника)
    - Rollers details (color, cutout type, and wear dimension) (ролики: цвет, тип выреза и износ)
    - Diffuser details (material) (деффузор: материал)
    - Last diffuser replacement (последняя замена деффузора)
    - Mudguard details (thread) (брызговик: резьба)
    - Last mudguard replacement (последняя замена брызговика)
    - Nozzle details (form) (сопло: форма)
    - Last nozzle replacement (последняя замена сопла)
    """
    robots = await get_multi_robot()
    for robot in robots:
        await message.answer(
            f'Ячейка {robot.robot_number}\n'
            '\n'
            'Комплектация\n'
            '\n'
            f'Проволока: {robot.robot_wire.wire_mark} {robot.robot_wire.wire_diameter}\n'
            f'Последняя замена проволоки: {robot.robot_last_update_wire.strftime("%Y-%m-%d %H:%M")}\n'
            f'Газ основной: {robot.robot_gaz.gaz_name} {robot.robot_gaz.gaz_type_obj}\n'
            f'Последняя замена основного газа: {robot.robot_last_update_gaz.strftime("%Y-%m-%d %H:%M")}\n'
            f'Газ дополнительный: {robot.robot_add_gaz.gaz_name} {robot.robot_add_gaz.gaz_type_obj}\n'
            f'Последняя замена доп газа: {robot.robot_last_update_add_gaz.strftime("%Y-%m-%d %H:%M")}\n'
            f'Наконечник: {robot.robot_tip.tip_diameter} {robot.robot_tip.tip_type}\n'
            f'Последняя замена наконечника: {robot.robot_last_update_tip.strftime("%Y-%m-%d %H:%M")}\n'
            f'Ролики: {robot.robot_rolls.rolls_color} {robot.robot_rolls.rolls_cutout_type} { robot.robot_rolls.rolls_ware_dim}\n'
            f'Деффузор: {robot.robot_mudguard.mudguard_material}\n'
            f'Последняя замена деффузора: {robot.robot_last_update_diffuser.strftime("%Y-%m-%d %H:%M")}\n'
            f'Брызговик: {robot.robot_diffuser.diffuser_thread}\n'
            f'Последняя замена брызговика: {robot.robot_last_update_mudguard.strftime("%Y-%m-%d %H:%M")}\n'
            f'Сопло: {robot.robot_nozzle.nozzle_form}\n'
            f'Последняя замена сопла: {robot.robot_last_update_nozzle.strftime("%Y-%m-%d %H:%M")}\n'
            '\n'
            'ОЧИСТКИ\n'
            '\n'
            f'Очистка основного сопла: {robot.robot_clear_nozzle.strftime("%Y-%m-%d %H:%M")}\n'
            f'Очистка доп сопла:{robot.robot_clear_add_nozzle.strftime("%Y-%m-%d %H:%M")}\n'
            f'Очистка каналов:{robot.robot_clear_intestine.strftime("%Y-%m-%d %H:%M")}\n'

        )
