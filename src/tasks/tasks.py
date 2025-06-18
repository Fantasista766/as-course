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
    sizes = [200, 500, 1000]
    output_dir = "src/static/images"

    img = Image.open(image_path)

    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    for size in sizes:
        img_resized = img.resize(  # type: ignore
            (size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS
        )

        new_file_name = f"{name}_{size}px{ext}"

        output_path = os.path.join(output_dir, new_file_name)

        img_resized.save(output_path)

    print(f"Изображние сохранено в размерах {sizes} в папке {output_dir}")
