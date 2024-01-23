# Restaurant
Мое первое приложение на FastAPI

## Инструкция по запуску проекта

Клонировать репозиторий  

Создать виртуальное окружение
```
python3.11 -m venv venv 
``` 
Активировать окружение
```
source venv/bin/activate
```
Установить зависимости проекта:
```
pip install -r requirements.txt
```
Запустить контейнер с базой
```
docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres
```
Запустить проект:
```
uvicorn main:app --reload
```