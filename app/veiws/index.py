from fastapi import APIRouter, Request 
from fastapi.responses import HTMLResponse 
from fastapi.templating import Jinja2Templates 
 
from bot.crud.crud_for_web import get_robot, standart_event, not_standart_event 
 
router = APIRouter() 
 
 
templates = Jinja2Templates(directory="app/templates") 
 
 
@router.get("/", response_class=HTMLResponse) 
async def hello_world(request: Request): 
    return templates.TemplateResponse(request=request, name="index.html") 
 
 
@router.get("/cell-1", response_class=HTMLResponse) 
async def cell_1_page(request: Request): 
    current_data = await get_robot(number=1) 
    sandart_event = await standart_event(number=1) 
    no_standart_event = await not_standart_event(number=1) 
    return templates.TemplateResponse( 
        request=request, 
        name="cell_1.html", 
        context={ 
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
        } 
    )


@router.get("/cell-2", response_class=HTMLResponse)
async def cell_2_page(request: Request):
    current_data = await get_robot(number=2) 
    sandart_event = await standart_event(number=2) 
    no_standart_event = await not_standart_event(number=2) 
    return templates.TemplateResponse( 
        request=request, 
        name="cell_2.html", 
        context={ 
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
            'nozzle_time':current_data.robot_last_update_nozzle.strftime('%Y-%m-%d %H:%M'), 
        } 
    )