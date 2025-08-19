# Project Structure & Brief description/documentation

## Neurons (The API)

### Project Files
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

## Neurons_Blazor (Blazor Web Application)
The most important part of the code is the **image_evaluation.razor**. This is a Blazor front-end page that provides a user interface for testing brand compliance evaluation. It connects directly to the FastAPI backend and allows users to upload assets, choose a model, and view evaluation results.

**Main Features**
- **Upload controls** (left column):
  - Upload an **image** (preview is displayed).
  - Upload a **brand kit PDF** (validated on upload).
  - Select a **model** (default: `ChatGPT-4o`, others selectable (NOTE: If they are implemented in the backend, i.e., the API)).
  - Start evaluation with an **Evaluate Brand Compliance** button.
- **Evaluation output** (right column):
  - Shows progress with a loading spinner while the API is called.
  - Displays either an instructional message (before evaluation) or the **model’s output** (after evaluation).
  - Handles and displays errors if something goes wrong.

**Implementation details**
- Built with **MudBlazor** components for a modern UI (cards, alerts, file uploads, buttons).
- Uses **`HttpClientFactory`** to call the FastAPI backend (`/evaluate_brand_compliance_wAPI`).
- Sends both the uploaded **image** and **brand kit PDF** as multipart form data, along with the selected model name.
- Uses **state flags** (`imageOk`, `pdfOk`, `isLoading`, `BothOk`) to enable/disable UI actions and provide user feedback.
- Responses from the backend are deserialized into an `ImageEvaluationResponse` model and displayed in the UI.

**User Flow**
1. Upload an image → see preview.
2. Upload a brand kit (PDF).
3. Select a model.
4. Click *Evaluate Brand Compliance*.
5. See evaluation result (or errors) in the results panel.

## Running the Project

This project uses **Docker Compose** for setup and deployment.

1. Make sure you have **Docker** and **Docker Compose** installed.
2. Clone the repository and navigate to the project root (where `docker-compose.yml` is located).
3. Build and start the containers:

   ```bash
   docker compose up --build

## Usage Examples
...

## Testing
...

