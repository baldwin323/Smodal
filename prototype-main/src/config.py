import os

class Config:
    DATABASE_URL = os.getenv('DATABASE_URL')
    SOCIAL_MEDIA_API_KEY = os.getenv('SOCIAL_MEDIA_API_KEY')
    PAYMENT_GATEWAY_API_KEY = os.getenv('PAYMENT_GATEWAY_API_KEY')

APP_CONFIG = Config()