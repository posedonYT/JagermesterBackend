from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, User, update_hourly_coins
from models import UserCreate, UserResponse, CoinsUpdate, ClickRequest
import datetime
import asyncio
import threading
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Функция для периодического обновления монет
def hourly_update_task():
    # Добавляем начальную задержку, чтобы убедиться, что таблицы созданы
    time.sleep(5)
    while True:
        try:
            update_hourly_coins()
        except Exception as e:
            print(f"Ошибка в фоновом задании hourly_update_task: {e}")
        # Спим час перед следующим обновлением
        time.sleep(3600)


# Запуск фонового потока для обновления монет
thread = threading.Thread(target=hourly_update_task, daemon=True)
thread.start()


@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.tg_id == user.tg_id).first()
    if db_user:
        return db_user

    current_time = int(datetime.datetime.now().timestamp())
    db_user = User(
        tg_id=user.tg_id,
        name=user.name,
        coins=0,
        coins_hours=100,
        coins_click=1,
        level=1,
        last_hourly_update=current_time
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/{tg_id}", response_model=UserResponse)
def get_user(tg_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.tg_id == tg_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Проверяем, нужно ли добавить часовые монеты
    current_time = int(datetime.datetime.now().timestamp())
    hours_passed = (current_time - db_user.last_hourly_update) // 3600

    if hours_passed > 0:
        db_user.coins += db_user.coins_hours * hours_passed
        db_user.last_hourly_update = current_time
        db.commit()
        db.refresh(db_user)

    return db_user


@app.post("/users/click/")
def add_click_coins(request: ClickRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.tg_id == request.tg_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.coins += db_user.coins_click
    db.commit()
    db.refresh(db_user)
    return {"status": "success", "coins": db_user.coins}


@app.get("/users/{tg_id}/coins")
def get_user_coins(tg_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.tg_id == tg_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Проверяем, нужно ли добавить часовые монеты
    current_time = int(datetime.datetime.now().timestamp())
    hours_passed = (current_time - db_user.last_hourly_update) // 3600

    if hours_passed > 0:
        db_user.coins += db_user.coins_hours * hours_passed
        db_user.last_hourly_update = current_time
        db.commit()
        db.refresh(db_user)

    return {"coins": db_user.coins}


@app.put("/users/{tg_id}/upgrade_click")
def upgrade_click(tg_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.tg_id == tg_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    upgrade_cost = db_user.coins_click * 10

    if db_user.coins < upgrade_cost:
        raise HTTPException(status_code=400, detail="Not enough coins")

    db_user.coins -= upgrade_cost
    db_user.coins_click += 1
    db.commit()
    db.refresh(db_user)

    return {"status": "success", "new_click_value": db_user.coins_click}


@app.put("/users/{tg_id}/upgrade_hourly")
def upgrade_hourly(tg_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.tg_id == tg_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    upgrade_cost = db_user.coins_hours * 5

    if db_user.coins < upgrade_cost:
        raise HTTPException(status_code=400, detail="Not enough coins")

    db_user.coins -= upgrade_cost
    db_user.coins_hours += 50
    db.commit()
    db.refresh(db_user)

    return {"status": "success", "new_hourly_value": db_user.coins_hours}