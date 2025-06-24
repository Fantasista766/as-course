1. На каждой тачке отдельно вести БД
   - создать ревизию `alembic revision --autogenerate -m "message"`
   - накатить таблицы в бд `alembic upgrade head`

```
celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B
```

```
docker image build -t booking_image .
```

```
docker network create my_network
```

```
docker run --name booking_db \
   -p 6432:5432  \
   -e POSTGRES_USER=postgres_user \
   -e POSTGRES_PASSWORD=postgres_password \
   -e POSTGRES_DB=booking \
   --network=my_network \
   --volume pg-booking-data:/var/lib/postresql/data \
   -d postgres:16
```

```
docker run --name booking_cache \
   -p 7379:6379 \
   --network=my_network \
   -d redis:7.4
```

```
docker run --name booking_back \
   -p 7777:8000 \
   --network=my_network \
   booking_image
```

```
docker run --name booking_celery_worker \
   --network=my_network \
   booking_image \
   celery --app=src.tasks.celery_app:celery_instance worker -l INFO
```

```
docker run --name booking_celery_beat \
   --network=my_network \
   booking_image \
   celery --app=src.tasks.celery_app:celery_instance worker -B
```