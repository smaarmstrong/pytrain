from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

app = FastAPI()


class Customer(BaseModel):
    name: str = Field(min_length=1)
    email: str
    # field_validator: email must contain "@"


class Item(BaseModel):
    sku: str = Field(min_length=1)
    qty: int
    unit_price: float
    # constraints: qty >= 1, unit_price > 0; sku uppercased by a validator


class Order(BaseModel):
    customer: Customer
    items: list[Item]
    coupon: str | None = None
    # items: at least one; coupon: None, "SAVE10" or "SAVE20"


# POST /orders — see prompt.md
