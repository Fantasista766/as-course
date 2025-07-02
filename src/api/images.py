from fastapi import APIRouter, BackgroundTasks, UploadFile

from src.exceptions import FileNotAnImageException, FileNotAnImageHTTPException
from src.services.images import ImageService


router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("/")
def upload_image(file: UploadFile, background_tasks: BackgroundTasks) -> None:
    try:
        ImageService().upload_image(file, background_tasks)
    except FileNotAnImageException:
        raise FileNotAnImageHTTPException
    return {"status": "OK", "detail": "Ваше изображение успешно загружено"}
