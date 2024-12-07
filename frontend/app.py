import streamlit as st
import requests
from PIL import Image
from io import BytesIO

backend_url = "http://localhost:8000"

st.title("GDSC_AI Image and Text Processor")

# Sidebar for navigation
page = st.sidebar.selectbox("Choose a page:", ["Text-to-Image", "Image-to-Text", "Health Check"])

if page == "Text-to-Image":
    st.header("Text to Image")
    text_input = st.text_input("Enter a text prompt:")
    if st.button("Generate Image"):
        response = requests.post(f"{backend_url}/text-to-image", json={"text": text_input})
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error("이미지 로드에 실패했어요.")

elif page == "Image-to-Text":
    st.header("Image to Text")
    uploaded_file = st.file_uploader("Upload an image:", type=["png", "jpg", "jpeg"])
    if st.button("Process Image"):
        if uploaded_file is not None:
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(f"{backend_url}/image-to-text", files=files)
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                st.error("Failed to process image.")
        else:
            st.error("Please upload an image.")

elif page == "Health Check":
    st.header("Server Health Check")
    response = requests.get(f"{backend_url}/health")
    if response.status_code == 200:
        st.success(f"Server Status: {response.json()['status']}")
    else:
        st.error("Server is not healthy.")
