from fastapi import APIRouter, BackgroundTasks, UploadFile

from src.services.images import ImageService


router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("/")
def upload_image(file: UploadFile, background_tasks: BackgroundTasks) -> None:
    ImageService().upload_image(file, background_tasks)
