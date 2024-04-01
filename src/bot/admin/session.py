from datetime import datetime

from fastapi import APIRouter, Request
from fastapi import Path
from starlette.status import HTTP_303_SEE_OTHER
from starlette.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from src.bot.db.crud import SessionCrud, DirectionCrud

router = APIRouter()

templates = Jinja2Templates('templates')


@router.get('/sessions/', name='list_sessions')
async def list_sessions(request: Request):
    sessions = await SessionCrud().all()

    ctx = {
        'title': 'События',
        'request': request,
        'list_objects': sessions,
        'form_url': router.url_path_for('create_form'),
    }
    return templates.TemplateResponse('model_templates/model_list.html', ctx)


@router.get('/form-sessions/{direction_id}')
async def form_direction_detail(request: Request, direction_id: int = Path()):
    obj = await SessionCrud().get(direction_id)
    ctx = {
        'request': request,
        'obj': obj,
        'directions': await DirectionCrud().all(),
    }
    return templates.TemplateResponse('model_templates/forms/sessions.html', ctx)


@router.post('/form-sessions/{session_id}')
async def form_update_direction_detail(request: Request, session_id: int = Path()):
    obj = await SessionCrud().get(session_id)
    form_data = await request.form()
    direction_id = int(form_data.get('direction_id'))

    date_str = form_data.get('date')
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

    time_str = form_data.get('time')
    time_obj = datetime.strptime(time_str, '%H:%M').time()

    data = {
        'title': form_data.get('title'),
        'date': date_obj,
        'direction': await DirectionCrud().get(pk=direction_id),
        'time': time_obj,
    }

    # obj.title = form_data.get('title')
    # obj.date = date_obj
    # obj.direction = await DirectionCrud().get(pk=direction_id)
    # obj.time = time_obj

    for attr, value in data.items():
        obj.__setattr__(attr, value)

    await SessionCrud().update(obj)
    return RedirectResponse(url=router.url_path_for('list_sessions'), status_code=HTTP_303_SEE_OTHER)


@router.get('/form-sessions/', name='create_form')
async def form_sessions(request: Request):
    ctx = {
        'request': request,
        'directions': await DirectionCrud().all(),
    }
    return templates.TemplateResponse('model_templates/forms/sessions.html', ctx)


@router.post('/form-sessions/')
async def form_create_sessions(request: Request):
    form_data = await request.form()
    direction_id = int(form_data.get('direction_id'))

    date_str = form_data.get('date')
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

    time_str = form_data.get('time')
    time_obj = datetime.strptime(time_str, '%H:%M').time()

    data = {
        'title': form_data.get('title'),
        'date': date_obj,
        'direction': await DirectionCrud().get(pk=direction_id),
        'time': time_obj,
    }
    await SessionCrud().create(**data)
    return RedirectResponse(url=router.url_path_for('list_sessions'), status_code=HTTP_303_SEE_OTHER)


@router.post('/delete-user/')
async def delete_sessions(request: Request):
    data = await request.form()
    obj_id = data.get('obj_id')
    await SessionCrud().delete(int(obj_id))
    return RedirectResponse(url=router.url_path_for('list_sessions'), status_code=HTTP_303_SEE_OTHER)
