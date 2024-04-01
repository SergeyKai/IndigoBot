from fastapi import APIRouter, Request
from fastapi import Path
from starlette.status import HTTP_303_SEE_OTHER
from starlette.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from src.bot.db.crud import SessionCrud, SessionRecordCrud, UserCrud

router = APIRouter()

templates = Jinja2Templates('templates')


@router.get('/sessions_records/', name='list_sessions_records')
async def list_sessions_records(request: Request):
    sessions_records = await SessionRecordCrud().all()

    ctx = {
        'title': 'Записи на собыия',
        'request': request,
        'list_objects': sessions_records,
        'form_url': router.url_path_for('create_form'),
    }
    return templates.TemplateResponse('model_templates/model_list.html', ctx)


@router.get('/form-sessions_records/{session_record_id}')
async def form_session_record_detail(request: Request, session_record_id: int = Path()):
    obj = await SessionRecordCrud().get(session_record_id)
    ctx = {
        'request': request,
        'obj': obj,
        'users': await UserCrud().all(),
        'sessions': await SessionCrud().all(),
    }
    return templates.TemplateResponse('model_templates/forms/session_record.html', ctx)


@router.post('/form-sessions_records/{session_record_id}')
async def form_update_session_record_detail(request: Request, session_record_id: int = Path()):
    obj = await SessionRecordCrud().get(session_record_id)
    data = await request.form()

    for attr, value in data.items():
        obj.__setattr__(attr, value)

    await SessionRecordCrud().update(obj)
    return RedirectResponse(url=router.url_path_for('list_sessions_records'), status_code=HTTP_303_SEE_OTHER)


@router.get('/form-sessions_records/', name='create_form')
async def form_sessions_records(request: Request):
    ctx = {
        'request': request,
        'users': await UserCrud().all(),
        'sessions': await SessionCrud().all(),
    }
    return templates.TemplateResponse('model_templates/forms/session_record.html', ctx)


@router.post('/form-sessions_records/')
async def form_create_sessions_records(request: Request):
    form_data = await request.form()
    data = {
        'user': await UserCrud().get(int(form_data.get('user'))),
        'session': await SessionCrud().get(int(form_data.get('session'))),
    }
    obj = await SessionRecordCrud().create(**data)
    return RedirectResponse(url=router.url_path_for('list_sessions_records'), status_code=HTTP_303_SEE_OTHER)


@router.post('/delete-user/')
async def delete_sessions_records(request: Request):
    data = await request.form()
    obj_id = data.get('obj_id')
    await SessionRecordCrud().delete(int(obj_id))
    return RedirectResponse(url=router.url_path_for('list_sessions_records'), status_code=HTTP_303_SEE_OTHER)
