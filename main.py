from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from transformers import pipeline
from transformers import AutoTokenizer
from awq import AutoAWQForCausalLM
import torch

app = FastAPI()

pipe_t2t = pipeline("text2text-generation", model="google/flan-t5-large")
prefix = "answer the question: "
def preprocess_prompt(input_prompt):
     input_text = [prefix + input_prompt]
     
     return input_text




@app.get("/infer_t5")
def t5(input):
    output = pipe_t2t(preprocess_prompt(input))
    return {"output": output[0]["generated_text"]}

app.mount("/", StaticFiles(directory="static", html=True), name="static")

def index() -> FileResponse:
    return FileResponse(path="/app/static/index.html", media_type="text/html")
