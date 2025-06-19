1. На каждой тачке отдельно вести БД
   - создать ревизию `alembic revision --autogenerate -m "message"`
   - накатить таблицы в бд `alembic upgrade head`

```
celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B
```