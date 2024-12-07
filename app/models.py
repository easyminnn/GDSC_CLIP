from pydantic import BaseModel
from transformers import CLIPProcessor, CLIPModel
from diffusers import StableDiffusionPipeline
import torch

# Define the text-to-image request model
class TextRequest(BaseModel):
    text: str

# Define the img/to/txt response model
class ImageToTextResponse(BaseModel):
    description: str

# Initialize Diffusion
device = "cuda" if torch.cuda.is_available() else "cpu"
pipeline = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
).to(device)

# Initialize CLIP
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Export
__all__ = ["TextRequest", "ImageToTextResponse", "pipeline", "clip_model", "clip_processor", "device"]
