from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM

MODEL_NAME_OR_PATH = "TheBloke/vicuna-7B-v1.3-GPTQ"
MODEL_BASENAME = "vicuna-7b-v1.3-GPTQ-4bit-128g.no-act.order"
DEVICE = "cuda:0"

def download_model() -> tuple:
    """Download the model and tokenizer."""
    model = AutoGPTQForCausalLM.from_quantized(MODEL_NAME_OR_PATH,
        model_basename=MODEL_BASENAME,  
        use_safetensors=True,
        trust_remote_code=True,
        device=DEVICE,
        use_triton=False,
        quantize_config=None)   
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME_OR_PATH, use_fast=True)
    return model, tokenizer

if __name__ == "__main__":
    download_model()
    