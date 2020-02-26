from config.loader import loader

CELERY_BROKER_URL = loader.get('CELERY.BROKER_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
