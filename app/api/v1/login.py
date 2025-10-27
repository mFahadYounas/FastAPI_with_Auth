from fastapi import APIRouter, Depends
from app.schemas.login import LoginResponse
from app.ResponseBuilder import ResponseBuilder
from app.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

login_router = APIRouter()

fake_users = {
    "alice": {"username": "alice", "password": "secret"},
    "bob": {"username": "bob", "password": "secret"},
}


@login_router.post("/login", response_model=LoginResponse)
def login(request: OAuth2PasswordRequestForm = Depends()):
    user = fake_users.get(request.username)
    if not user or user["password"] != request.password:
        ResponseBuilder[LoginResponse].error(
            status=401, error_msg="Invalid username or password!"
        )

    access_token = create_access_token(data={"sub": request.username})
    response = LoginResponse(access_token=access_token, token_type="bearer")

    return response
