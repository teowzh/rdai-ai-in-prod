from fastapi import FastAPI

app = FastAPI()
app.mount("/", StaticFiles(directory="static", html=True), name="static")


def index() -> FileResponse:
    return FileResponse(path="/app/static/index.html", media_type="text/html")