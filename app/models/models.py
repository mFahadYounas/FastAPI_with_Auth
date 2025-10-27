from app.database import Base
from sqlalchemy import Column, Integer, String, Float
from app.schemas.users import UserSchema
from app.schemas.products import ProductsSchema
from pydantic import EmailStr


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)

    def to_user_schema(self) -> UserSchema:
        user = UserSchema(
            name=str(self.name), email=EmailStr(self.email), password=str(self.password)
        )
        return user


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    price = Column(Float, index=True)
    description = Column(String, index=True)

    def to_product_schema(self) -> ProductsSchema:
        product = ProductsSchema(
            product_name=str(self.product_name),
            price=float(self.price),
            description=str(self.description),
        )
        return product
