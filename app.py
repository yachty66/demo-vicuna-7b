from potassium import Potassium, Request, Response
from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM

MODEL_NAME_OR_PATH = "TheBloke/vicuna-7B-v1.3-GPTQ"
MODEL_BASENAME = "vicuna-7b-v1.3-GPTQ-4bit-128g.no-act.order"
DEVICE = "cuda:0"

app = Potassium("my_app")

@app.init
def init() -> dict:
    """Initialize the application with the model and tokenizer."""
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME_OR_PATH, use_fast=True)
    model = AutoGPTQForCausalLM.from_quantized(MODEL_NAME_OR_PATH,
        model_basename=MODEL_BASENAME,  
        use_safetensors=True,
        trust_remote_code=True,
        device=DEVICE,
        use_triton=False,
        quantize_config=None)
    context = {
        "model": model,
        "tokenizer": tokenizer
    }
    return context
    
@app.handler()
def handler(context: dict, request: Request) -> Response:
    """Handle a request to generate text from a prompt."""
    system = "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions."
    prompt = request.json.get("prompt")
    prompt_template = f"### System:\n{system}\n\n### User:\n{prompt}\n\n### Assistant:\n"
    temperature = request.json.get("temperature", 0.7)
    max_new_tokens = request.json.get("max_new_tokens", 512)
    model = context.get("model")
    tokenizer = context.get("tokenizer")
    input_ids = tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
    output = model.generate(inputs=input_ids, temperature=temperature, max_new_tokens=max_new_tokens)
    result = tokenizer.decode(output[0])
    return Response(json={"outputs": result}, status=200)

if __name__ == "__main__":
    app.serve()
