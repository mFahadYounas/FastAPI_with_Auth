from pydantic import BaseModel, EmailStr


class LogoutSessionResponse(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
