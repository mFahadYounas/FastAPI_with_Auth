from fastapi import APIRouter, Depends, Request
from app.schemas.login import LoginResponse, LoginSessionResponse, LoginRequest
from app.schemas.api_response import APIResponse
from app.ResponseBuilder import ResponseBuilder
from app.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from app.manage_redis import redis_client
import json
from uuid import uuid4

login_router = APIRouter()

fake_users = {
    "alice": {"username": "alice", "password": "secret", "email": "alice@email.com"},
    "bob": {"username": "bob", "password": "secret", "email": "bob@email.com"},
}


@login_router.post("/login", response_model=LoginResponse)
def login(request: OAuth2PasswordRequestForm = Depends()):
    user = fake_users.get(request.username)
    if not user or user["password"] != request.password:
        return ResponseBuilder[LoginResponse].error(
            status=401, error_msg="Invalid username or password!"
        )

    access_token = create_access_token(data={"sub": request.username})
    response = LoginResponse(access_token=access_token, token_type="bearer")

    return response


@login_router.post("/sessionlogin", response_model=APIResponse[LoginSessionResponse])
def login_session(request: Request, credentials: LoginRequest):
    user = fake_users.get(credentials.username)
    if not user:
        return ResponseBuilder[LoginSessionResponse].error(
            status=401, error_msg="Invalid username!"
        )
    if user["password"] != credentials.password:
        return ResponseBuilder[LoginSessionResponse].error(
            status=401, error_msg="Invalid password!"
        )
    session_id = str(uuid4())
    session_data = {"username": credentials.username, "email": user["email"]}
    redis_client.setex(session_id, 3600, json.dumps(session_data))
    request.session["session_id"] = session_id
    response = LoginSessionResponse(username=credentials.username, email=user["email"])
    return ResponseBuilder[LoginSessionResponse].success(data=response)
