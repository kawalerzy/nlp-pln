### Running celery worker
```
# in src dir
celery worker -A distributed.celery_entrypoint.celery --loglevel=info
```
### DB Backup and restore
```
pg_dump -h localhost -p 5432 -Fc -o -U scrapper postgres > postgres.dump
pg_restore -h localhost -p 5433 -U scrapper -d postgres -v postgres.dump
```
### Running postgres and redis on docker
Change auth.json properties to smth like this:
```json
{
  "DB": {
    "HOST": "localhost",
    "PORT": "5433",
    "NAME": "postgres",
    "USER": "scrapper",
    "PASSWORD": "password"
  },
  "CELERY": {
    "BROKER_URL": "redis://localhost:6379"
  }
}
```
Run docker compose in separate terminal
```console
█▓▒░jakub@ubi█▓▒░ śro lut 26 09:16:55 
~/dev/nlp-pln/docker/ docker-compose up
```