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



# Predefined labels for matching
labels = ["a cat", "a dog", "a car", "a person", "a tree", "a house"]

@router.post("/image-to-text")
async def image_to_text(file: UploadFile = File(...)):
    """
    Generate a text description of an image using CLIP.
    """
    try:
        # Check if a file is uploaded
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded.")

        # Load the image
        image = Image.open(BytesIO(await file.read())).convert("RGB")

        # Preprocess the image
        inputs = clip_processor(images=image, return_tensors="pt", padding=True)

        # Get image features
        image_features = clip_model.get_image_features(**inputs)
        image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)  # Normalize features

        # Preprocess labels
        text_inputs = clip_processor(text=labels, return_tensors="pt", padding=True)
        text_features = clip_model.get_text_features(**text_inputs)
        text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)  # Normalize features

        # Compute similarity
        similarity = torch.matmul(image_features, text_features.T)

        # Find the best matching label
        best_match_idx = similarity.argmax().item()
        description = labels[best_match_idx]

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

