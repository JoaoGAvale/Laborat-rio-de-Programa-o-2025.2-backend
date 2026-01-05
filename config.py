import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        "postgresql://usuario:senha@localhost:5432/meubanco"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hora
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")