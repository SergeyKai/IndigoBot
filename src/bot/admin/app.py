from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi import Path

from src.bot.db.crud import DirectionCrud

app = FastAPI()

templates = Jinja2Templates('templates')
app.mount('/static', StaticFiles(directory='static'), 'static')


@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get('/directions/')
async def list_directions(request: Request):
    directions = await DirectionCrud().all()

    ctx = {
        'request': request,
        'list_objects': directions,
    }
    return templates.TemplateResponse('model_templates/model_list.html', ctx)


@app.get('/form-direction/{direction_id}')
async def form_direction_detail(request: Request, direction_id: int = Path()):
    obj = await DirectionCrud().get(direction_id)
    ctx = {
        'request': request,
        'obj': obj,
    }
    return templates.TemplateResponse('model_templates/forms/directions.html', ctx)


@app.post('/form-direction/{direction_id}')
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
    return templates.TemplateResponse('model_templates/forms/directions.html', ctx)


@app.get('/form-direction/')
async def form_directions(request: Request):
    return templates.TemplateResponse('model_templates/forms/directions.html', {'request': request})


@app.post('/form-direction/')
async def form_create_directions(request: Request):
    data = await request.form()
    obj = await DirectionCrud().create(**data)
    return RedirectResponse(url='/directions/')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
