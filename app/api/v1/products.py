from fastapi import APIRouter, Depends, Request
from app.schemas.api_response import APIResponse
from app.schemas.products import ProductsSchema
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Product
from app.ResponseBuilder import ResponseBuilder
from app.manage_redis import redis_client
from typing import cast

products_router = APIRouter()


@products_router.get("/", response_model=APIResponse[list[ProductsSchema]])
def get_products(
    request: Request, offset: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> APIResponse:
    if limit > 20:
        limit = 20
    session_id = request.session.get("session_id")
    print(session_id)
    if not session_id:
        return ResponseBuilder.error(
            status=401, error_msg="User unauthorized: No session_id"
        )

    session_data = redis_client.get(session_id)
    if not session_data:
        return ResponseBuilder.error(
            status=401, error_msg="User unauthorized: User not signed in"
        )

    products = (
        db.query(Product).order_by(Product.product_id).offset(offset).limit(limit).all()
    )
    return ResponseBuilder[list[Product]].success(products)


@products_router.post("/", response_model=APIResponse[ProductsSchema])
def post_product(
    new_product: ProductsSchema, db: Session = Depends(get_db)
) -> APIResponse:
    product = Product(
        product_name=new_product.product_name,
        price=new_product.price,
        description=new_product.description,
    )
    try:
        db.add(product)
        db.commit()
        db.refresh(product)
    except DatabaseError as error:
        print(error)
        db.rollback()
        return ResponseBuilder[ProductsSchema].error(
            status=500, error_msg="Database Error!"
        )

    return ResponseBuilder[Product].success(product)


@products_router.delete("/{id}", response_model=APIResponse[ProductsSchema])
def delete_product(id: int, db: Session = Depends(get_db)) -> APIResponse:
    product = db.query(Product).filter(Product.product_id == id).first()
    if not product:
        return ResponseBuilder[ProductsSchema].error(
            status=404, error_msg="Product not found!"
        )
    try:
        db.delete(product)
        db.commit()
    except DatabaseError:
        db.rollback()
        return ResponseBuilder[ProductsSchema].error(
            status=500, error_msg="Database Error!"
        )
    return ResponseBuilder[Product].success(product)


@products_router.put("/{id}", response_model=APIResponse[ProductsSchema])
def update_product(
    id: int, product_update: ProductsSchema, db: Session = Depends(get_db)
) -> APIResponse:
    product = db.query(Product).filter(Product.product_id == id).first()
    if not product:
        return ResponseBuilder[ProductsSchema].error(
            status=404, error_msg="Product not found!"
        )

    product_update = cast(Product, product_update)
    product.product_name = product_update.product_name
    product.description = product_update.description
    product.price = product_update.price

    try:
        db.commit()
        db.refresh(product)
    except DatabaseError:
        db.rollback()
        return ResponseBuilder[ProductsSchema].error(
            status=500, error_msg="Database Error!"
        )

    return ResponseBuilder[Product].success(product)
