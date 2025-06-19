from celery import Celery  # type: ignore

from src.config import settings

celery_instance = Celery(
    "tasks", broker=settings.REDIS_URL, include=["src.tasks.tasks"]
)

celery_instance.conf.beat_schedule = {  # type: ignore
    "a": {
        "task": "booking_today_checkin",
        "schedule": 5,
    }
}
