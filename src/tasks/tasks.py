from time import sleep
import os

from PIL import Image

from src.tasks.celery_app import celery_instance


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
