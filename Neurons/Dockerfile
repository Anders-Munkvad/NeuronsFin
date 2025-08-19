# ./fastapi/Dockerfile
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# system deps needed by pillow / pymupdf
RUN apt-get update && apt-get install -y \
    libmagic1 \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# copy requirements first
COPY requirements.txt .

# install app requirements from PyPI
RUN pip install --no-cache-dir -r requirements.txt

# install CPU-only torch wheel
#RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# copy app code
COPY app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
