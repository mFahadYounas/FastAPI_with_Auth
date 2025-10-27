from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import DatabaseError
from app.database import get_db
from app.models.models import User
from app.schemas.users import UserSchema
from typing import cast
from app.ResponseBuilder import ResponseBuilder
from app.schemas.api_response import APIResponse

users_router = APIRouter()


@users_router.get("/", response_model=APIResponse[list[UserSchema]])
def get_users(
    offset: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> APIResponse:
    if limit > 20:
        limit = 20
    results = db.query(User).order_by(User.user_id).offset(offset).limit(limit).all()
    return ResponseBuilder[list[User]].success(results)


@users_router.post("/", response_model=APIResponse[UserSchema])
def post_user(new_user: UserSchema, db: Session = Depends(get_db)) -> APIResponse:
    user = User(
        name=new_user.name,
        email=new_user.email,
        password=new_user.password,
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except DatabaseError:
        db.rollback()
        return ResponseBuilder[UserSchema].error(
            status=500, error_msg="Database Error!"
        )

    return ResponseBuilder[User].success(user)


@users_router.delete("/{id}", response_model=APIResponse[UserSchema])
def delete_user(id: int, db: Session = Depends(get_db)) -> APIResponse:
    user = db.query(User).filter(User.user_id == id).first()
    if not user:
        return ResponseBuilder[UserSchema].error(
            status=404, error_msg="User not found!"
        )
    try:
        db.delete(user)
        db.commit()
    except DatabaseError:
        db.rollback()
        return ResponseBuilder[UserSchema].error(
            status=500, error_msg="Database Error!"
        )
    return ResponseBuilder[User].success(user)


@users_router.put("/{id}", response_model=APIResponse[UserSchema])
def update_user(
    id: int, user_update: UserSchema, db: Session = Depends(get_db)
) -> APIResponse:
    user = db.query(User).filter(User.user_id == id).first()
    if not user:
        return ResponseBuilder[UserSchema].error(
            status=404, error_msg="User not found!"
        )

    user_update = cast(User, user_update)
    user.email = user_update.email
    user.name = user_update.name
    user.password = user_update.password
    try:
        db.commit()
        db.refresh(user)
    except DatabaseError:
        db.rollback()
        return ResponseBuilder[UserSchema].error(
            status=500, error_msg="Database Error!"
        )
    return ResponseBuilder[User].success(user)
