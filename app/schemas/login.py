from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True


class LoginSessionResponse(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
