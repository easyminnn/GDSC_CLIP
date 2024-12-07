from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
from PIL import Image
import uvicorn
import os
import shutil
import io
from model import CLIPHandler 

app = FastAPI()

# Initialize the CLIP handler
clip_handler = CLIPHandler()

class TextRequest(BaseModel):
    text: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/text-to-image")
async def text_to_image(request: TextRequest, files: List[UploadFile] = File(...)):
    # Load images from the uploaded files
    images = []
    for file in files:
        image = Image.open(io.BytesIO(await file.read()))
        images.append(image)

    # Use the CLIP model to rank images against the provided text
    logits_per_image = clip_handler.process(images=images, text=[request.text])

    # Find the best-matching image
    best_match_idx = logits_per_image.argmax().item()
    best_match_image = images[best_match_idx]

    # Save the best image to BytesIO
    img_bytes = io.BytesIO()
    best_match_image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return StreamingResponse(img_bytes, media_type="image/png")

@app.post("/image-to-text")
async def image_to_text(file: UploadFile = File(...)):
    # Save file temporarily (optional for processing)
    with open(f"temp_{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Dummy implementation
    return {"message": f"Processed text for image: {file.filename}"}

"""
if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.getenv("FASTAPI_HOST"),
        port=int(os.getenv("FASTAPI_PORT", 8000)),
        reload=True
    )"""


## uvicorn main:app --reload --host 0.0.0.0 --port 8000
## streamlit run app.py