from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates('templates')
app.mount('/static', StaticFiles(directory='static'), 'static')

@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
