from time import sleep
import asyncio
import os

from PIL import Image

from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


@celery_instance.task  # type: ignore
def test_task() -> None:
    sleep(5)
    print("GOOD JOB")


@celery_instance.task  # type: ignore
def resize_image(image_path: str):
    widths = [100, 500, 1280, 1920, 3840]
    output_dir = "src/static/images"

    img = Image.open(image_path)

    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    for width in widths:
        img_resized = img.resize(  # type: ignore
            (width, int(img.height * (width / img.width))), Image.Resampling.LANCZOS
        )

        new_file_name = f"{name}_{width}px{ext}"

        output_path = os.path.join(output_dir, new_file_name)

        img_resized.save(output_path)

    print(f"Изображние сохранено в размерах {widths} в папке {output_dir}")


def get_db_manager():
    return DBManager(session_factory=async_session_maker_null_pool)


async def get_bookings_with_today_checkin_helper():
    print(f"IMRHER")
    async with get_db_manager() as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


@celery_instance.task(name="booking_today_checkin")  # type: ignore
def send_emails_to_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())
