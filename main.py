from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from transformers import pipeline
from transformers import AutoTokenizer
from awq import AutoAWQForCausalLM
import torch

app = FastAPI()

original_model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
quant_path = 'TinyLlama-1.1B-Chat-v1.0-awq'
quant_config = { "zero_point": True, "q_group_size": 128, "w_bit": 4, "version": "GEMV" }

model = AutoAWQForCausalLM.from_pretrained(
    original_model_id, safetensors=True, **{"torch_dtype": torch.float16, "low_cpu_mem_usage": True, "use_cache": False}, device_map="cuda:0"
)
tokenizer = AutoTokenizer.from_pretrained(original_model_id,
                                          torch_dtype="auto")

model.quantize(tokenizer, quant_config=quant_config)
# pipe_t2t = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
pipe_t2t = pipeline("text-generation",
                model=model,
                tokenizer=tokenizer,
                torch_dtype=torch.bfloat16,
                device_map="auto")

@app.get("/infer_tinyllama")
def tinyllama(input):
    output = pipe_t2t(input)
    return {"output": output[0]["generated_text"]}

app.mount("/", StaticFiles(directory="static", html=True), name="static")

def index() -> FileResponse:
    return FileResponse(path="/app/static/index.html", media_type="text/html")
