from pydantic import BaseModel
from . import common_config


class ProductsSchema(BaseModel):
    product_name: str
    price: float
    description: str

    model_config = common_config
