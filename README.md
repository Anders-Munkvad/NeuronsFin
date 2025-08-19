# NeuronsFin

## Introduction
...

## Project Structure

### Neurons (The API)

#### Project Files
- **extract_pdf.py**  
  Provides helper functions for extracting brand compliance information from PDF files using PyMuPDF (`fitz`).  
  Extracts: font styles, logo safe zone, logo colours, and full colour palette.

- **image_evaluation_gpt.py & image_evaluation_Qwen.py** 
  Logic regarding calling the multi-modal models GPT-4o and Qwen, respectively.

- **compliance_prompt_gpt.py & compliance_prompt_Qwen.py**  
  Builds the prompt given to the GPT-4o and Qwen model, based on extracted brand compliance from a given PDF.

- **main.py**  
  Defines the FastAPI backend. Exposes endpoints for:
  - Extracting brand compliance info from PDFs
  - Building structured compliance prompts
  - Evaluating brand compliance of images using an LLM



## Documentation
...

## Installation & Setup
...

## Running the Project
...

## Usage Examples
...

## Testing
...

