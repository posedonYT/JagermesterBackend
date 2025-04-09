from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    tg_id: int
    name: str


class UserResponse(BaseModel):
    id: int
    tg_id: int
    name: str
    coins: int
    coins_hours: int
    coins_click: int
    level: int

    class Config:
        from_attributes = True  # Заменено с orm_mode=True на from_attributes=True


class CoinsUpdate(BaseModel):
    tg_id: int
    amount: int

class ClickRequest(BaseModel):
    tg_id: int