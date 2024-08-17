from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")

@app.get("/home/", response_class=HTMLResponse)
async def read_home(request: Request):
    # 템플릿 렌더링
    return templates.TemplateResponse("home3.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)