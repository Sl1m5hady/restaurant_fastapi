from sqlalchemy.orm import Session
from restaurant_app.db import models
from restaurant_app.api import schemas


def get_menu(db: Session, menu_id: str):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()


def get_menu_list(db: Session):
    return db.query(models.Menu).all()


def create_menu(db: Session, menu: schemas.MenuCreate):
    db_menu = models.Menu(**menu.model_dump())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def destroy_menu(db: Session, menu_id: str):
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if db_menu:
        db.delete(db_menu)
        db.commit()
        return True


def update_menu(db: Session, menu_id: str, menu: schemas.MenuCreate):
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if db_menu:
        db_menu.title = menu.title
        db_menu.description = menu.description
        db.commit()
        db.refresh(db_menu)
        return db_menu


def get_submenu(db: Session, submenu_id: str, menu_id: str):
    return (
        db.query(models.Submenu)
        .filter(
            models.Submenu.id == submenu_id, models.Submenu.menu_id == menu_id
        )
        .first()
    )


def create_submenu(db: Session, submenu: schemas.SubmenuCreate, menu_id: str):
    menu = db.query(models.Menu).get(menu_id)
    if menu:
        db_submenu = models.Submenu(**submenu.model_dump(), menu_id=menu_id)
        db.add(db_submenu)
        db.commit()
        db.refresh(db_submenu)
        return db_submenu


def get_submenu_list(db: Session, menu_id: str):
    return db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id)


def destroy_submenu(db: Session, menu_id: str, submenu_id: str):
    db_submenu = (
        db.query(models.Submenu)
        .filter(
            models.Submenu.id == submenu_id, models.Submenu.menu_id == menu_id
        )
        .first()
    )
    if db_submenu:
        db.delete(db_submenu)
        db.commit()
        return True


def update_submenu(
    db: Session, menu_id: str, submenu_id: str, menu: schemas.SubmenuCreate
):
    db_submenu = (
        db.query(models.Submenu)
        .filter(
            models.Submenu.id == submenu_id, models.Submenu.menu_id == menu_id
        )
        .first()
    )
    if db_submenu:
        db_submenu.title = menu.title
        db_submenu.description = menu.description
        db.commit()
        db.refresh(db_submenu)
        return db_submenu


def create_dish(
    db: Session, dish: schemas.DishCreate, menu_id: str, submenu_id: str
):
    submenu = db.query(models.Submenu).get(submenu_id)
    if submenu:
        db_dish = models.Dish(**dish.model_dump(), submenu_id=submenu_id)
        db.add(db_dish)
        db.commit()
        db.refresh(db_dish)
        return db_dish


def get_dish(db: Session, menu_id: str, submenu_id: str, dish_id: str):
    return (
        db.query(models.Dish)
        .filter(
            models.Dish.id == dish_id, models.Dish.submenu_id == submenu_id
        )
        .first()
    )


def get_dish_list(db: Session, menu_id: str, submenu_id: str):
    return (
        db.query(models.Dish)
        .filter(models.Dish.submenu_id == submenu_id)
        .all()
    )


def destroy_dish(db: Session, menu_id: str, submenu_id: str, dish_id: str):
    db_dish = (
        db.query(models.Dish)
        .filter(
            models.Dish.id == dish_id, models.Dish.submenu_id == submenu_id
        )
        .first()
    )
    if db_dish:
        db.delete(db_dish)
        db.commit()
        return True


def update_dish(
    db: Session,
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    dish: schemas.DishCreate,
):
    db_dish = (
        db.query(models.Dish)
        .filter(
            models.Dish.id == dish_id, models.Dish.submenu_id == submenu_id
        )
        .first()
    )
    if db_dish:
        db_dish.title = dish.title
        db_dish.description = dish.description
        db_dish.price = dish.price
        db.commit()
        db.refresh(db_dish)
        return db_dish
