from sqlalchemy import Column, Integer, String, create_engine, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger, unique=True, nullable=False)
    name = Column(String, nullable=False)
    coins = Column(Integer, default=0)
    coins_hours = Column(Integer, default=100)
    coins_click = Column(Integer, default=1)
    level = Column(Integer, default=1)
    last_hourly_update = Column(Integer, default=0)  # Timestamp последнего обновления


# Создание движка базы данных и инициализация таблиц
engine = create_engine("sqlite:///clicker.db")
Base.metadata.create_all(engine)  # Убедимся, что таблицы созданы сразу

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def update_hourly_coins():
    db = SessionLocal()
    try:
        current_time = int(datetime.datetime.now().timestamp())
        one_hour_ago = current_time - 3600

        users = db.query(User).filter(User.last_hourly_update <= one_hour_ago).all()

        for user in users:
            hours_passed = (current_time - user.last_hourly_update) // 3600
            if hours_passed > 0:
                user.coins += user.coins_hours * hours_passed
                user.last_hourly_update = current_time

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Ошибка при обновлении часовых монет: {e}")
    finally:
        db.close()