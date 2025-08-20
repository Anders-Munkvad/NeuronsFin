import io
from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq

# Load once at import (so container warms the model only once)
MODEL_ID = "Qwen/Qwen2.5-VL-3B-Instruct"

processor = AutoProcessor.from_pretrained(MODEL_ID)
model = AutoModelForVision2Seq.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto",   # uses GPU if available, otherwise CPU
)

def Qwen_response(image_bytes: bytes, prompt: str, max_new_tokens: int = 512) -> str:
    """Run multimodal inference with Qwen2.5-VL (Transformers)."""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    inputs = processor(text=prompt, images=image, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=max_new_tokens)

    return processor.batch_decode(output, skip_special_tokens=True)[0]
