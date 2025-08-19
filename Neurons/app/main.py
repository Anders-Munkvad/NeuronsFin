from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
from io import BytesIO
from fastapi import Form
import logging

#from app.image_evaluation_Qwen import Qwen_response
#from app.compliance_prompt_Qwen import build_compliance_prompt_qwen
from app.extract_pdf import extract_brand_compliance
from app.compliance_prompt_gpt import build_compliance_prompt
from app.image_evaluation_gpt import GPT_4o_response


logging.basicConfig(level=logging.INFO)
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Brand Compliance API is running"}

# API function to extract brand compliance information from the PDF.
# Testing can be done by requesting the following to the API: curl -X POST http://127.0.0.1:8000/extract_brand_compliance -F "file=@C:\Users\ander\OneDrive - University of Copenhagen\Desktop\Neurons\Neurons_brand_kit.pdf"
@app.post("/extract_brand_compliance")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()  # this gives you raw bytes
    results = extract_brand_compliance(contents)  # pass only the bytes
    return {"Requirements": results, "message": "Requirements"}

# Test: curl -X POST http://127.0.0.1:8000/extract_brand_compliance -F "file=@C:\Users\ander\OneDrive - University of Copenhagen\Desktop\Neurons\Neurons_brand_kit.pdf"
@app.post("/build_compliance_prompt")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()  # raw bytes from PDF
    compliance_data = extract_brand_compliance(contents)  # your updated version that handles bytes
    prompt = build_compliance_prompt(compliance_data)     # build string prompt from dict
    return {
        "Prompt": prompt,
        "message": "Brand compliance prompt successfully generated."
    }

# Test: curl -X POST http://127.0.0.1:8000/evaluate_brand_compliance_wAPI -F "brand_kit=@C:\Users\ander\OneDrive - University of Copenhagen\Desktop\Neurons\Neurons_brand_kit.pdf" -F "image_file=@C:\Users\ander\OneDrive - University of Copenhagen\Desktop\Neurons\neurons_1.png"
@app.post("/evaluate_brand_compliance_wAPI")
async def evaluate_brand_compliance(
    brand_kit: UploadFile = File(...),
    image_file: UploadFile = File(...),
    model_name: str = Form(...)
):
    brand_bytes = await brand_kit.read()
    image_bytes = await image_file.read()

    brand_data = extract_brand_compliance(brand_bytes)

    prompt = None
    response = None

    if model_name == "ChatGPT-4o":
        prompt = build_compliance_prompt(brand_data)
        response = GPT_4o_response(image_bytes, prompt)
    # elif model_name == "Qwen-3b":
    #     prompt = build_compliance_prompt_qwen(brand_data)
    #     response = Qwen_response(image_bytes, prompt)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown model: {model_name}")

    result = {
        "prompt_used": prompt,
        "model_output": response
    }

    # Log to console to see what is being returned
    logging.info(f"Returning API response: {result}")

    return result