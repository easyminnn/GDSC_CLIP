from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse
from io import BytesIO
from PIL import Image
import torch
from models import TextRequest, pipeline, clip_model, clip_processor, device
import logging

# Initialize router and logger
router = APIRouter()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@router.post("/text-to-image")
async def text_to_image(request: TextRequest):
    """
    Generate an image from text using Stable Diffusion.
    """
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty.")

        logger.info(f"Generating image for text: {request.text}")
        with torch.autocast(device):
            image = pipeline(request.text).images[0]

        img_bytes = BytesIO()
        image.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        logger.info("Image generated successfully.")
        return StreamingResponse(img_bytes, media_type="image/png")

    except HTTPException as e:
        logger.warning(f"HTTP exception: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")


@router.post("/image-to-text")
async def image_to_text(file: UploadFile = File(...)):
    """
    Generate a text description of an image using CLIP.
    """
    try:
        # Load the uploaded image
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded.")

        image = Image.open(BytesIO(await file.read())).convert("RGB")

        # Preprocess the image using CLIP
        inputs = clip_processor(images=image, return_tensors="pt", padding=True)

        # Generate text embeddings (you need predefined labels for matching)
        image_features = clip_model.get_image_features(**inputs)

        # Placeholder for label matching logic
        description = "Generated description placeholder (implement label comparison here)."

        logger.info("Image description generated successfully.")
        return JSONResponse(content={"description": description})

    except HTTPException as e:
        logger.warning(f"HTTP exception: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")


@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify server status.
    """
    try:
        # Perform basic checks
        logger.info("Performing health check...")

        # Optional: Check if models are loaded properly
        if not pipeline or not clip_model or not clip_processor:
            raise HTTPException(status_code=500, detail="Model initialization failed.")

        # Optional: Check device availability
        if device not in ["cuda", "cpu"]:
            raise HTTPException(status_code=500, detail="Invalid device configuration.")

        logger.info("Health check passed.")
        return JSONResponse(content={"status": "Healthy"})
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Server health check failed.")

