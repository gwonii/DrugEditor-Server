from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import shutil

app = FastAPI()

# Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")

@app.get("/home/", response_class=HTMLResponse)
async def read_home(request: Request):
    # 템플릿 렌더링
    return templates.TemplateResponse("home.html", {"request": request})

UPLOAD_DIRECTORY = "uploads/"
RESULTS_DIRECTORY = "results/"

# Ensure the upload and results directories exist
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

if not os.path.exists(RESULTS_DIRECTORY):
    os.makedirs(RESULTS_DIRECTORY)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_location = os.path.join(RESULTS_DIRECTORY, filename)
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

@app.get("/list-files/")
async def list_files():
    try:
        files = os.listdir(RESULTS_DIRECTORY)
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching file list: {str(e)}")

@app.post("/convert-files/")
async def convert_files():
    try:
        # Move files from UPLOAD_DIRECTORY to RESULTS_DIRECTORY
        for filename in os.listdir(UPLOAD_DIRECTORY):
            source = os.path.join(UPLOAD_DIRECTORY, filename)
            destination = os.path.join(RESULTS_DIRECTORY, filename)
            if os.path.isfile(source):
                shutil.move(source, destination)
        return {"info": "Files successfully converted and moved to results directory."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during file conversion: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)