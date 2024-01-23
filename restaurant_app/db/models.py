import uuid
from sqlalchemy import ForeignKey, String, Column, UUID, Float
from sqlalchemy.orm import relationship, column_property
from restaurant_app.db.database import Base
from sqlalchemy.sql import func, select


class Dish(Base):
    __tablename__ = "dish"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey("submenu.id"))
    submenu = relationship("Submenu", back_populates="dishes")


class Submenu(Base):
    __tablename__ = "submenu"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menu.id"))
    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship(
        "Dish", back_populates="submenu", cascade="all, delete-orphan"
    )
    dishes_count = column_property(
        select(func.count(Dish.id))
        .where(Dish.submenu_id == id)
        .correlate_except(Dish)
        .as_scalar()
    )


class Menu(Base):
    __tablename__ = "menu"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    submenus = relationship(
        "Submenu", back_populates="menu", cascade="all, delete-orphan"
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
    )
