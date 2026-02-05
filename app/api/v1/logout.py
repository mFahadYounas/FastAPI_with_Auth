from fastapi import APIRouter, Request
from app.ResponseBuilder import ResponseBuilder
from app.manage_redis import redis_client
from app.schemas.api_response import APIResponse
from app.schemas.logout import LogoutSessionResponse
import json

logout_router = APIRouter()


@logout_router.get("/logout", response_model=APIResponse[LogoutSessionResponse])
def logout_session(request: Request):
    session_id = request.session.get("session_id")
    if not session_id:
        return ResponseBuilder.error(status=401, error_msg="User not logged in!")
    session_data = redis_client.get(session_id)
    if not session_data:
        return ResponseBuilder.error(
            status=401, error_msg="User unauthorized: User not signed in"
        )
    redis_client.delete(session_id)
    user_data = json.loads(str(session_data))
    response = LogoutSessionResponse(
        username=user_data["username"], email=user_data["email"]
    )
    return ResponseBuilder[LogoutSessionResponse].success(response)
