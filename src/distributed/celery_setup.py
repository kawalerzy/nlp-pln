from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

from scraping.pilkanoznapl.tasks import celery


def configure_celery(celery_obj):
    celery_obj.conf.broker_url = CELERY_BROKER_URL
    celery_obj.conf.result_backend = CELERY_RESULT_BACKEND
    celery_obj.finalize()


def celery_entrypoint():
    configure_celery(celery_obj=celery)
    return celery
