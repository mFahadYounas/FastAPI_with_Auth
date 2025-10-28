from pydantic import BaseModel, EmailStr
from . import common_config


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

    model_config = common_config
