#!/bin/sh
set -e

# Прогоняем миграции
alembic upgrade head

# Выполняем то, что передали в CMD или из docker run
exec "$@"
