from openai import OpenAI
import base64
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from parent directory
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Safe to access the environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def GPT_4o_response(image_bytes: bytes, prompt: str) -> str:
    # Encode image to base64
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{encoded_image}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
        max_tokens=1024,
        temperature=0.2,
    )

    return response.choices[0].message.content
