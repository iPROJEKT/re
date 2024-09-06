from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.utils import get_common_context

router = APIRouter()


templates = Jinja2Templates(directory="app/templates")


@router.get("/cell-2", response_class=HTMLResponse)
async def cell_2_page(request: Request):
    context = await get_common_context(number=2)
    return templates.TemplateResponse(
        request=request,
        name="cell_2.html",
        context=context
    )