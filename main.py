from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from restaurant_app.api import schemas
from restaurant_app.db import models, crud
from restaurant_app.db.database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post(
    "/api/v1/menus",
    response_model=schemas.Menu,
    status_code=status.HTTP_201_CREATED,
)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    return crud.create_menu(db, menu=menu)


@app.get("/api/v1/menus", response_model=list[schemas.Menu])
def get_menus_list(db: Session = Depends(get_db)):
    menus = crud.get_menu_list(db=db)
    return menus


@app.get("/api/v1/menus/{menu_id}", response_model=schemas.Menu)
def get_menu(menu_id: str, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db=db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )
    return db_menu


@app.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    db_menu_deleted = crud.destroy_menu(db=db, menu_id=menu_id)
    if db_menu_deleted:
        return JSONResponse(
            content={"status": True, "message": "The menu has been deleted"}
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
    )


@app.patch("/api/v1/menus/{menu_id}", response_model=schemas.Menu)
def update_menu(
    menu_id: str, menu: schemas.MenuCreate, db: Session = Depends(get_db)
):
    db_menu = crud.update_menu(db, menu_id, menu)
    if not db_menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )
    return db_menu


@app.post(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=schemas.Submenu,
    status_code=status.HTTP_201_CREATED,
)
def create_submenu(
    submenu: schemas.SubmenuCreate, menu_id: str, db: Session = Depends(get_db)
):
    db_submenu = crud.create_submenu(db, submenu, menu_id=menu_id)
    if not db_submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Submenu not found"
        )
    return db_submenu


@app.get(
    "/api/v1/menus/{menu_id}/submenus", response_model=list[schemas.Submenu]
)
def get_submenus_list(menu_id: str, db: Session = Depends(get_db)):
    menus = crud.get_submenu_list(db=db, menu_id=menu_id)
    return menus


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.Submenu,
)
def get_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu(
        db=db, menu_id=menu_id, submenu_id=submenu_id
    )
    if not db_submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
        )
    return db_submenu


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(
    menu_id: str, submenu_id: str, db: Session = Depends(get_db)
):
    db_submenu_deleted = crud.destroy_submenu(
        db=db, menu_id=menu_id, submenu_id=submenu_id
    )
    if db_submenu_deleted:
        return JSONResponse(
            content={"status": True, "message": "The submenu has been deleted"}
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
    )


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.Submenu,
    status_code=status.HTTP_200_OK,
)
def update_submenu(
    menu_id: str,
    submenu_id: str,
    submenu: schemas.SubmenuCreate,
    db: Session = Depends(get_db),
):
    db_submenu = crud.update_submenu(db, menu_id, submenu_id, submenu)
    if not db_submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
        )
    return db_submenu


@app.post(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=schemas.Dish,
    status_code=status.HTTP_201_CREATED,
)
def create_dish(
    menu_id: str,
    submenu_id: str,
    dish: schemas.DishCreate,
    db: Session = Depends(get_db),
):
    db_dish = crud.create_dish(db, dish, menu_id, submenu_id)
    if not db_dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
        )
    return db_dish


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=schemas.Dish,
)
def get_dish(
    menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)
):
    db_dish = crud.get_dish(
        db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
    )
    if not db_dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="dish not found"
        )
    return db_dish


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=list[schemas.Dish],
)
def get_dishes_list(
    menu_id: str, submenu_id: str, db: Session = Depends(get_db)
):
    dishes = crud.get_dish_list(db=db, menu_id=menu_id, submenu_id=submenu_id)
    return dishes


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(
    menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)
):
    db_dish_deleted = crud.destroy_dish(
        db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
    )
    if db_dish_deleted:
        return JSONResponse(
            content={"status": True, "message": "The dish has been deleted"}
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="dish not found"
    )


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=schemas.Dish,
    status_code=status.HTTP_200_OK,
)
def update_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    dish: schemas.DishCreate,
    db: Session = Depends(get_db),
):
    db_dish = crud.update_dish(db, menu_id, submenu_id, dish_id, dish)
    if not db_dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
        )
    return db_dish
