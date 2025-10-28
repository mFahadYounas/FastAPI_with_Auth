from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse
from app.ResponseBuilder import ResponseBuilder
from app.schemas.api_response import APIResponse

profile_pic_router = APIRouter()


@profile_pic_router.post("/picture", response_model=APIResponse[dict])
def upload_profile_pic(file: UploadFile):
    if not file:
        return ResponseBuilder.error(status=400, error_msg="No file provided!")
    if file.content_type not in {"image/jpeg", "image/png"}:
        return ResponseBuilder.error(
            status=400, error_msg=f"Incorrect file type! Received: {file.content_type}"
        )
    max_file_size = 50000
    if file.size and file.size > max_file_size:
        return ResponseBuilder.error(
            status=400, error_msg=f"File too large! Should be less than {max_file_size}"
        )
    return ResponseBuilder[dict].success({"message": "File upload successful!"})


@profile_pic_router.get("/picture", response_class=FileResponse)
def get_profile_pic():
    return "./app/assets/Placeholder_image.jpg"
