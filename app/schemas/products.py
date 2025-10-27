from pydantic import BaseModel


class ProductsSchema(BaseModel):
    product_name: str
    price: float
    description: str

    class Config:
        from_attributes = True
