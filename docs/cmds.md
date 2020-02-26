### Running celery worker

```
# in src dir
celery worker -A distributed.celery_entrypoint.celery --loglevel=info
```