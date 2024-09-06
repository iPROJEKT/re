from typing import Dict, Any

from bot.crud.crud_for_web import get_robot, standart_event, not_standart_event, change_wire, change_tip_c, def_cou


async def get_common_context(number: int) -> Dict[str, Any]:
    current_data = await get_robot(number)
    sandart_event = await standart_event(number)
    no_standart_event = await not_standart_event(number)

    wire_data = await change_wire(number) * 16
    wire_data_int = await change_wire(number)
    tip_data = await change_tip_c(number)
    defect = await def_cou(number)

    context = {
        'defff': defect,
        'cell_number': str(number),
        'standatr_event': sandart_event,
        'not_standart_event': no_standart_event,
        'wire': current_data.robot_wire.wire_mark,
        'wire_time': current_data.robot_last_update_wire.strftime('%Y-%m-%d %H:%M'),
        'main_gaz': current_data.robot_gaz.gaz_name,
        'main_gaz_time': current_data.robot_last_update_gaz.strftime('%Y-%m-%d %H:%M'),
        'add_gaz': current_data.robot_add_gaz.gaz_name,
        'add_gaz_time': current_data.robot_last_update_add_gaz.strftime('%Y-%m-%d %H:%M'),
        'tip': current_data.robot_tip.tip_diameter,
        'tip_type': current_data.robot_tip.tip_type,
        'tip_time': current_data.robot_last_update_tip.strftime('%Y-%m-%d %H:%M'),
        'roll': current_data.robot_rolls.rolls_color,
        'roll_type': current_data.robot_rolls.rolls_cutout_type,
        'roll_dim': current_data.robot_rolls.rolls_ware_dim,
        'mudguard': current_data.robot_mudguard.mudguard_material,
        'mudguard_time': current_data.robot_last_update_diffuser.strftime('%Y-%m-%d %H:%M'),
        'thread': current_data.robot_diffuser.diffuser_thread,
        'thread_time': current_data.robot_last_update_mudguard.strftime('%Y-%m-%d %H:%M'),
        'nozzle': current_data.robot_nozzle.nozzle_form,
        'nozzle_time': current_data.robot_last_update_nozzle.strftime('%Y-%m-%d %H:%M'),
        'wire_data': wire_data,
        'tip_data': tip_data,
        'wire_data_int': wire_data_int
    }
    return context
