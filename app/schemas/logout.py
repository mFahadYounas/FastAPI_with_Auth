from pydantic import BaseModel, EmailStr
from . import common_config


class LogoutSessionResponse(BaseModel):
    username: str
    email: EmailStr

    model_config = common_config
