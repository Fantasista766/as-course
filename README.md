1. На каждой тачке отдельно вести БД
   - создать ревизию `alembic revision --autogenerate -m "message"`
   - накатить таблицы в бд `alembic upgrade head`
