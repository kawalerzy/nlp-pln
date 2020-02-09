### Running celery worker

```
celery worker -A distributed.celery_entrypoint.celery --loglevel=info
```