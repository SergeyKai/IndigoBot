from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from directions import router as directions_router
from users import router as users_router

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), 'static')

app.include_router(directions_router)
app.include_router(users_router)

templates = Jinja2Templates('templates')


@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
