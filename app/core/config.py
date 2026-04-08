import os


class Settings:
    app_name: str = "ScamShield AI"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./scamshield.db")


settings = Settings()
