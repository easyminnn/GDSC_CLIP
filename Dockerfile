# Use the official Python image
FROM python:3.12-slim-buster

# working directory in the container 
WORKDIR /app

#  copy the current directory contents into the container at /app
COPY app/ /app
COPY requirements.txt /app

# Install dependency packages
RUN pip install --no-cache-dir -r requirements.txt

# cre ate a new user
RUN useradd -m appuser
USER appuser

# Expose port 8000
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
