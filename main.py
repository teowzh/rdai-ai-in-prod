from fastapi import FastAPI
from transformers import pipeline

app = FastAPI()
pipe_t2t = pipeline("text2text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

# @app.get("/")
# def read_root():
#     return {"Hello": "World!"}

@app.get("/infer_tinyllama")
def t5(input):
    output = pipe_t2t(input)
    return {"output": output[0]["generated_text"]}

app.mount("/", StaticFiles(directory="static", html=True), name="static")


def index() -> FileResponse:
    return FileResponse(path="/app/static/index.html", media_type="text/html")