1. На каждой тачке отдельно вести БД
   - создать ревизию `alembic revision --autogenerate -m "message"`
   - накатить таблицы в бд `alembic upgrade head`

```
git config --local user.name "Дмитрий Нестеров"
git config --local user.email "proxxx766@gmail.com"
```

```
celery --app=src.tasks.celery_app:celery_instance worker -l INFO
celery --app=src.tasks.celery_app:celery_instance beat -l INFO

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
   -e POSTGRES_PASSWORD={password} \
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
docker run --name booking_nginx \
   --volume ./nginx.conf:/etc/nginx/nginx.conf \
   --volume /etc/letsencrypt:/etc/letsencrypt \
   --volume /var/lib/letsencrypt:/var/lib/letsencrypt \
   --network=my_network \
   -d -p 443:443 nginx
```

Запуск раннера
```
docker run -d --name gitlab-runner --restart always \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  -v /var/run/docker.sock:/var/run/docker.sock \
  gitlab/gitlab-runner:alpine
```

Регистрация раннера
```
docker run --rm -it \
    -v /srv/gitlab-runner/config:/etc/gitlab-runner \
    gitlab/gitlab-runner:alpine register
```