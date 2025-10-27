from fastapi import FastAPI
from app.api.v1.login import login_router
from app.api.v1.products import products_router
from app.api.v1.users import users_router
from app.database import init_db
import uvicorn

app = FastAPI()

app.include_router(login_router, tags=["Login"])
app.include_router(products_router, tags=["Products"], prefix="/products")
app.include_router(users_router, tags=["Users"], prefix="/users")


def main():
    init_db()
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
