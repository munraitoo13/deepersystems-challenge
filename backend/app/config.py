from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    """Base configuration."""

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/mydatabase")
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    DEBUG = True
