import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os
# Backend URL
from dotenv import load_dotenv

load_dotenv()
backend_url = os.environ.get("VAST_AI_BACKEND_URL")

# Streamlit App Title
st.title("GDG AI Image and Text Processor")

# Sidebar for Navigation
page = st.sidebar.selectbox("Choose a page:", ["Text-to-Image", "Image-to-Text", "Health Check"])

if page == "Text-to-Image":
    st.header("Text to Image")
    text_input = st.text_input("Enter a text prompt:")
    if st.button("Generate Image"):
        if text_input.strip():
            response = requests.post(f"{backend_url}/text-to-image", json={"text": text_input})
            if response.status_code == 200:
                # Load and display the image
                image = Image.open(BytesIO(response.content))
                st.image(image, caption="Generated Image", use_column_width=True)
            else:
                st.error(f"Image generation failed: {response.status_code} - {response.text}")
        else:
            st.error("Please enter a valid text prompt.")

elif page == "Image-to-Text":
    st.header("Image to Text")
    uploaded_file = st.file_uploader("Upload an image:", type=["png", "jpg", "jpeg"])
    if st.button("Process Image"):
        if uploaded_file is not None:
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(f"{backend_url}/image-to-text", files=files)
            if response.status_code == 200:
                # Display the description
                description = response.json().get("description", "No description returned.")
                st.success(f"Description: {description}")
            else:
                st.error(f"Image processing failed: {response.status_code} - {response.text}")
        else:
            st.error("Please upload an image to process.")

elif page == "Health Check":
    st.header("Server Health Check")
    response = requests.get(f"{backend_url}/health")
    if response.status_code == 200:
        st.success(f"Server Status: {response.json().get('status', 'Unknown')}")
    else:
        st.error(f"Server health check failed: {response.status_code} - {response.text}")
