from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Request, Response
from PIL import Image
from io import BytesIO
import logging, uuid

#from app.image_evaluation_Qwen import Qwen_response
#from app.compliance_prompt_Qwen import build_compliance_prompt_qwen
from app.extract_pdf import extract_brand_compliance
from app.compliance_prompt_gpt import build_compliance_prompt
from app.image_evaluation_gpt import GPT_4o_response

app = FastAPI()
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("neurons.api")

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

# API function to build a compliance prompt.
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

# The function that will get called in the frontend to evaluate brand compliance, given an image and a PDF
# Error handling in terms of uploading is mostly handled in the frontend, and its associated backend (C# code)
#    - Look at "image_evaluation.razor" for more information 

# Test: curl -X POST http://127.0.0.1:8000/evaluate_brand_compliance_wAPI -F "brand_kit=@C:\Users\ander\OneDrive - University of Copenhagen\Desktop\Neurons\Neurons_brand_kit.pdf" -F "image_file=@C:\Users\ander\OneDrive - University of Copenhagen\Desktop\Neurons\neurons_1.png"
@app.post("/evaluate_brand_compliance_wAPI")
async def evaluate_brand_compliance(
    request: Request,
    response: Response,
    brand_kit: UploadFile = File(...), # PDF
    image_file: UploadFile = File(...), # Image
    model_name: str = Form(...),
):
    # Small amount of logging
    request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
    response.headers["X-Request-ID"] = request_id

    try:
        brand_bytes = await brand_kit.read() # Bytes of brand compliance
        image_bytes = await image_file.read() # Bytes of image

        # Extract brand compliance from the pdf byes
        brand_data = extract_brand_compliance(brand_bytes)

        # Logic regarding choosing of model.
        # As of now, only the "ChatGPT-4o" is available, but it is obviously quite easy to implement others
        if model_name == "ChatGPT-4o":
            prompt = build_compliance_prompt(brand_data)
            model_output = GPT_4o_response(image_bytes, prompt)
        else:
            # client error: log as warning, include request_id
            log.warning(
                "Unknown model",
                extra={"request_id": request_id},
            )
            raise HTTPException(status_code=400, detail=f"Unknown model: {model_name}")

        result = {
            "prompt_used": prompt,
            "model_output": model_output,
            "status": "ok",                # status and request_id is ignored in the UI/frontend, however can be helpful for logging
            "request_id": request_id,      
        }

        # success log with light context
        log.info(
            "evaluate_brand_compliance ok",
            extra={
                "request_id": request_id,
            },
        )
        return result

    except HTTPException:
        raise
    except Exception as e:
        # unexpected error:
        log.exception(
            "evaluate_brand_compliance failed",
            extra={"request_id": request_id},
        )
        raise HTTPException(status_code=500, detail="Internal server error")