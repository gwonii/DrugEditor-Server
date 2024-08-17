from fastapi import FastAPI, File, UploadFile, HTTPException
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
    return templates.TemplateResponse("home.html", {"request": request})

UPLOAD_DIRECTORY = "uploads/"

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_location = os.path.join(UPLOAD_DIRECTORY, filename)
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_location)

@app.delete("/delete/{filename}")
async def delete_file(filename: str):
    file_location = os.path.join(UPLOAD_DIRECTORY, filename)
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")
    
    os.remove(file_location)
    return {"info": f"file '{filename}' deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
