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
    #return templates.TemplateResponse("index.html", {"request": request, "id": id})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
