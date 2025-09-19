from imports import os, load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "dev_fallback_change_me")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
ALGORITHM = "HS256"