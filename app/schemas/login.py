from pydantic import BaseModel, EmailStr
from . import common_config


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str

    model_config = common_config


class LoginSessionResponse(BaseModel):
    username: str
    email: EmailStr

    model_config = common_config
