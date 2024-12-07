# 사용 예시
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 환경 변수 가져오기
MODEL_NAME = os.getenv("CLIP_MODEL_NAME")  # Default to a common CLIP model
FASTAPI_HOST = os.getenv("FASTAPI_HOST")  # Localhost as default
FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", 8000))  # Default to 8000
