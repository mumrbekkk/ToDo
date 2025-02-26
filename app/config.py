import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todo_list.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
