from fastapi import FastAPI
from routes import router

# Initialize FastAPI application
app = FastAPI(title="Text-to-Image and Image-to-Text API")

# Include routes
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Text-to-Image and Image-to-Text API!!!"}