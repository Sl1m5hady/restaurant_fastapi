import uuid
from sqlalchemy import ForeignKey, String, Column, UUID, Float, Text
from sqlalchemy.orm import relationship, column_property
from restaurant_app.db.database import Base
from sqlalchemy.sql import func, select


class Dish(Base):
    __tablename__ = "dishes"

    # id = Column(UUID, primary_key=True)
    id = Column(
        "id",
        Text(length=36),
        default=lambda: str(uuid.uuid4()),
        primary_key=True,
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    submenu_id = Column(
        Text(length=36),
        ForeignKey("submenus.id"),
        # default=lambda: str(uuid.uuid4()),
    )
    submenu = relationship("Submenu", back_populates="dishes")


class Submenu(Base):
    __tablename__ = "submenus"
    # change for PostgreSQL
    id = Column(
        "id",
        Text(length=36),
        default=lambda: str(uuid.uuid4()),
        primary_key=True,
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    menu_id = Column(
        Text(length=36),
        ForeignKey("menus.id"),
        # default=lambda: str(uuid.uuid4())
    )
    dishes = relationship(
        "Dish", back_populates="submenu", cascade="all, delete"
    )
    menu = relationship("Menu", back_populates="submenus")
    dishes_count = column_property(
        select(func.count(Dish.id))
        .where(Dish.submenu_id == id)
        .correlate_except(Dish)
        .as_scalar()
    )


class Menu(Base):
    __tablename__ = "menus"

    id = Column(
        "id",
        Text(length=36),
        default=lambda: str(uuid.uuid4()),
        primary_key=True,
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    submenus = relationship(
        "Submenu", back_populates="menu", cascade="all, delete"
    )
    submenus_count = column_property(
        select(func.count(Submenu.id))
        .where(Submenu.menu_id == id)
        .correlate_except(Submenu)
        .as_scalar()
    )
    dishes_count = column_property(
        select(func.count(Dish.id))
        .where(
            Dish.submenu_id.in_(
                select(Submenu.id).where(Submenu.menu_id == id)
            )
        )
        .correlate_except(Dish)
        .as_scalar()
        # select(func.count(Dish.id)).where(
        #     Dish.submenu_id == id).correlate_except(Dish).as_scalar()
    )
