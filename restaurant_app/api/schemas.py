from pydantic import BaseModel, field_validator
from uuid import UUID


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    pass


class Menu(MenuBase):
    id: UUID
    description: str
    title: str
    submenus_count: int
    dishes_count: int

    class Cofig:
        orm_mode = True


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    pass


class Submenu(SubmenuBase):
    id: UUID
    description: str
    title: str
    dishes_count: int

    class Config:
        orm_mode = True


class DishBase(BaseModel):
    title: str
    description: str
    price: float


class DishCreate(DishBase):
    pass


class Dish(DishBase):
    id: UUID
    description: str
    title: str
    price: float

    class Config:
        orm_mode = True

    @field_validator("price")
    def get_str_price(cls, price: float):
        return f"{price:.2f}"
