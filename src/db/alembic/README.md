Generic single-database configuration.

## Generating migrations
Modify some model in `db.models`, and run `autogenerate` command. All commands should be run from root project folder
```
alembic revision --autogenerate -m "add summary column"
```
Adjust generated migration, if needed. Run upgrade command
```
alembic upgrade head
```