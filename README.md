# CLIP Model with FastAPI and Streamlit

## Description
This project demonstrates the integration of OpenAI's **CLIP model** for multimodal learning. The backend, implemented using **FastAPI**, handles requests for text-to-image and image-to-text processing. The frontend, built with **Streamlit**, provides an intuitive user interface for interacting with the model.

### Features
- **Text-to-Image**: Input text and retrieve the most relevant image(s).
- **Image-to-Text**: Upload an image and retrieve the most relevant text description(s).
- **Health Check**: Verify server status via a `/health` endpoint.

---

## Setup

### Prerequisites
Ensure you have the following installed:
- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/clip-fastapi-streamlit.git
   cd clip-fastapi-streamlit

2. **Build and run the Docker containers**:

   ```bash
   docker-compose up --build
   
3. **Access the application**:

- Backend: Visit http://localhost:8000 for the FastAPI documentation (Swagger UI).
- Frontend: Visit http://localhost:8501 for the Streamlit application.

4. **Stop the application**: Press `Ctrl+C`` in the terminal or use the following command to stop and remove containers:

   ```bash
   docker-compose down


### Project Structure
project_root/
├── app/
│   ├── main.py             # FastAPI server
│   ├── models.py           # CLIP model logic
│   ├── utils.py            # Utility functions
│   ├── requirements.txt    # Backend dependencies
│   ├── .env                # Environment variables
├── frontend/
│   ├── app.py              # Streamlit application
│   ├── assets/             # Static files
├── Dockerfile              # Backend Dockerfile
├── docker-compose.yml      # Docker Compose configuration
└── README.md               # Project documentation
