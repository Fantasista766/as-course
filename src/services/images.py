from pathlib import Path
import shutil

from fastapi import BackgroundTasks, UploadFile

from src.exceptions import FileNotAnImageException
from src.services.base import BaseService
from src.tasks.tasks import resize_image


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".jfif"}


class ImageService(BaseService):
    def upload_image(self, file: UploadFile, background_tasks: BackgroundTasks) -> None:
        self.validate_file_extension(file)
        image_path = f"src/static/images/{file.filename}"
        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

        # resize_image.delay(image_path)  # type: ignore
        background_tasks.add_task(resize_image, image_path)

    def validate_file_extension(self, file: UploadFile) -> None:
        ext = Path(file.filename).suffix.lower()  # type: ignore
        if ext not in ALLOWED_EXTENSIONS:
            raise FileNotAnImageException
