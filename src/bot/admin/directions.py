from fastapi import APIRouter, Request
from fastapi import Path
from starlette.status import HTTP_303_SEE_OTHER
from starlette.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from src.bot.db.crud import DirectionCrud

router = APIRouter()

templates = Jinja2Templates('templates')


@router.get('/directions/', name='list_directions')
async def list_directions(request: Request):
    directions = await DirectionCrud().all()

    ctx = {
        'title': 'Направления',
        'request': request,
        'list_objects': directions,
        'form_url': router.url_path_for('create_form'),
    }
    return templates.TemplateResponse('model_templates/model_list.html', ctx)


@router.get('/form-direction/{direction_id}')
async def form_direction_detail(request: Request, direction_id: int = Path()):
    obj = await DirectionCrud().get(direction_id)
    ctx = {
        'request': request,
        'obj': obj,
    }
    return templates.TemplateResponse('model_templates/forms/directions.html', ctx)


@router.post('/form-direction/{direction_id}')
async def form_update_direction_detail(request: Request, direction_id: int = Path()):
    obj = await DirectionCrud().get(direction_id)
    data = await request.form()

    for attr, value in data.items():
        obj.__setattr__(attr, value)

    await DirectionCrud().update(obj)
    ctx = {
        'request': request,
        'obj': obj,
    }
    return RedirectResponse(url=router.url_path_for('list_directions'), status_code=HTTP_303_SEE_OTHER)


@router.get('/form-direction/', name='create_form')
async def form_directions(request: Request):
    return templates.TemplateResponse('model_templates/forms/directions.html', {'request': request})


@router.post('/form-direction/')
async def form_create_directions(request: Request):
    data = await request.form()
    await DirectionCrud().create(**data)
    return RedirectResponse(url=router.url_path_for('list_directions'), status_code=HTTP_303_SEE_OTHER)


@router.post('/delete-direction/')
async def delete_directions(request: Request):
    data = await request.form()
    obj_id = data.get('obj_id')
    await DirectionCrud().delete(int(obj_id))
    return RedirectResponse(url=router.url_path_for('list_directions'), status_code=HTTP_303_SEE_OTHER)
