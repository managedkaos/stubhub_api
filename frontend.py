import requests
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/events.html", response_class=HTMLResponse)
async def events(request: Request):
    response = requests.request("GET", "http://127.0.0.1:8000/events")
    return templates.TemplateResponse("events.html", {"request": request, "events": response.json()['events']})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
