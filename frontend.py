import requests
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/forgot", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("forgot-password.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/events", response_class=HTMLResponse)
async def events(request: Request):
    response = requests.request("GET", "http://127.0.0.1:9000/events")
    return templates.TemplateResponse("events.html", {"request": request, "events": response.json()['events']})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9001)
