from fastapi import FastAPI
from app.api.v1.login import login_router
from app.api.v1.products import products_router
from app.api.v1.users import users_router
from app.api.v1.logout import logout_router
from starlette.middleware.sessions import SessionMiddleware
from app.database import init_db
from app.manage_redis import check_connectivity
import uvicorn

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super-secret-key-of-great-secrecy")

app.include_router(login_router, tags=["Login"])
app.include_router(products_router, tags=["Products"], prefix="/products")
app.include_router(users_router, tags=["Users"], prefix="/users")
app.include_router(logout_router, tags=["Logout"])


def main():
    init_db()
    if not check_connectivity():
        return
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
