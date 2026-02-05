from fastapi import FastAPI
from app.api.v1.login import login_router
from app.api.v1.products import products_router
from app.api.v1.users import users_router
from app.api.v1.logout import logout_router
from app.api.v1.profile_pic import profile_pic_router
from starlette.middleware.sessions import SessionMiddleware
from app.database import init_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_: FastAPI):
    print("Starting app...")

    init_db()

    yield

    print("Stopping app...")


app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key="super-secret-key-of-great-secrecy")

app.include_router(login_router, tags=["Login"])
app.include_router(products_router, tags=["Products"], prefix="/products")
app.include_router(users_router, tags=["Users"], prefix="/users")
app.include_router(logout_router, tags=["Logout"])
app.include_router(profile_pic_router, tags=["Profile Picture"], prefix="/profile")
