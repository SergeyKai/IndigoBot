from fastapi import APIRouter, Request
from fastapi import Path
from starlette.status import HTTP_303_SEE_OTHER
from starlette.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from src.bot.db.crud import UserCrud

router = APIRouter()

templates = Jinja2Templates('templates')


@router.get('/users/', name='list_users')
async def list_users(request: Request):
    users = await UserCrud().all()

    ctx = {
        'title': 'Пользователи',
        'request': request,
        'list_objects': users,
        'form_url': router.url_path_for('create_form'),
    }
    return templates.TemplateResponse('model_templates/model_list.html', ctx)


@router.get('/form-users/{direction_id}')
async def form_direction_detail(request: Request, direction_id: int = Path()):
    obj = await UserCrud().get(direction_id)
    ctx = {
        'request': request,
        'obj': obj,
    }
    return templates.TemplateResponse('model_templates/forms/users.html', ctx)


@router.post('/form-users/{direction_id}')
async def form_update_direction_detail(request: Request, direction_id: int = Path()):
    obj = await UserCrud().get(direction_id)
    data = await request.form()

    for attr, value in data.items():
        obj.__setattr__(attr, value)

    await UserCrud().update(obj)
    ctx = {
        'request': request,
        'obj': obj,
    }
    return RedirectResponse(url=router.url_path_for('list_users'), status_code=HTTP_303_SEE_OTHER)


@router.get('/form-users/', name='create_form')
async def form_users(request: Request):
    return templates.TemplateResponse('model_templates/forms/users.html', {'request': request})


@router.post('/form-users/')
async def form_create_users(request: Request):
    data = await request.form()
    obj = await UserCrud().create(**data)
    return RedirectResponse(url=router.url_path_for('list_users'), status_code=HTTP_303_SEE_OTHER)


@router.post('/delete-user/')
async def delete_users(request: Request):
    data = await request.form()
    obj_id = data.get('obj_id')
    await UserCrud().delete(int(obj_id))
    return RedirectResponse(url=router.url_path_for('list_users'), status_code=HTTP_303_SEE_OTHER)
