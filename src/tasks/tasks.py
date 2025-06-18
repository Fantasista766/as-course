from time import sleep

from src.tasks.celery_app import celery_instance


@celery_instance.task  # type: ignore
def test_task() -> None:
    sleep(5)
    print("GOOD JOB")
