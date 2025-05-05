from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, Boolean
from sqlalchemy.orm import relationship, sessionmaker, Session, declarative_base
from jose import jwt, JWTError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from typing import Optional, List
import datetime as dt
from contextlib import asynccontextmanager

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Таблица ролей
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(50), unique=True, nullable=False)

# Таблица пользователей
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    role = relationship("Role")
    is_active = Column(Boolean, default=True)

# Таблица меню
class Menu(Base):
    __tablename__ = "menu"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)

# Таблица заказов
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_order = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    table_number = Column(Integer, nullable=False)
    guest_count = Column(Integer, nullable=False)

# Таблица позиций заказа
class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    dish_id = Column(Integer, ForeignKey("menu.id"), nullable=False)
    amount = Column(Integer, nullable=False, default=1)

def initialize_database():
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        if not db.query(Role).first():
            roles = ["Администратор", "Официант", "Повар"]
            for role_name in roles:
                db.add(Role(role=role_name))
            db.commit()
        
        if not db.query(Menu).first():
            menu_items = [
                {"title": "Борщ", "type": "Еда", "price": 200},
                {"title": "Стейк", "type": "Еда", "price": 1700},
                {"title": "Кофе", "type": "Напиток", "price": 100},
                {"title": "Пирожок", "type": "Еда", "price": 50}
            ]
            for item in menu_items:
                db.add(Menu(**item))
            db.commit()
            
        if not db.query(User).filter(User.nickname == "admin").first():
            admin_role = db.query(Role).filter(Role.role == "Администратор").first()
            if admin_role:
                db.add(User(nickname="admin", password="admin", role_id=admin_role.id))
                db.commit()
    finally:
        db.close()

    Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database on startup
    initialize_database()
    yield
    # Clean up on shutdown would go here

# Модели данных
class AuthRequest(BaseModel):
    nickname: str
    password: str

class NewOrder(BaseModel):
    table_number: int
    guest_count: int
    items: List[int]
    user_id: int

class RegisterUserSchema(BaseModel):
    login: str
    password: str
    roles: List[str]

class UserCreate(BaseModel):
    nickname: str
    password: str
    roles: str

class UserUpdate(BaseModel):
    is_active: bool

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/add_user")
def add_user(user: UserCreate):
    db = SessionLocal()
    try:
        db_user = User(nickname=user.nickname, password=user.password, role=user.roles)
        db.add(db_user)
        db.commit()
        return {"message": "Пользователь добавлен", "id": db_user.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@app.patch("/update_user/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        db_user.is_active = user.is_active
        db.commit()
        return {"message": "Статус обновлён"}
    finally:
        db.close()

@app.get("/users")
def get_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return [
            {
                "id": user.id,
                "nickname": user.nickname,
                "role": user.role,
                "status": "Активен" if user.is_active else "Неактивен"
            }
            for user in users
        ]
    finally:
        db.close()

async def get_role_id_from_roles(role_name: str, db: Session):
    role = db.query(Role).filter(Role.role == role_name).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role.id

@app.post("/auth")
async def auth(request_data: AuthRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.nickname == request_data.nickname).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if user.password != request_data.password:
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {
        "token": "example-token",
        "user": request_data.nickname
    }

@app.post("/users/register")
async def register_user(user_data: RegisterUserSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.nickname == user_data.login).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    role_id = await get_role_id_from_roles(user_data.roles[0], db)

    new_user = User(
        nickname=user_data.login,
        password=user_data.password,
        role_id=role_id
    )
    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}

@app.get("/users/list")
async def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": user.id, "login": user.nickname, "roles": user.role.role} for user in users]

@app.post("/orders/")
async def create_order(order: NewOrder, db: Session = Depends(get_db)):
    new_order = Order(
        date_order=dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        user_id=order.user_id,
        table_number=order.table_number,
        guest_count=order.guest_count
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for dish_id in order.items:
        order_item = OrderItem(
            order_id=new_order.id,
            dish_id=dish_id,
            amount=1
        )
        db.add(order_item)
    
    db.commit()

    return {"message": "Order created successfully", "order_id": new_order.id}

@app.get("/orders/")
async def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    result = []
    for order in orders:
        order_data = {
            "id": order.id,
            "date_order": order.date_order,
            "table_number": order.table_number,
            "guest_count": order.guest_count,
            "items": []
        }
        items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        for item in items:
            dish = db.query(Menu).filter(Menu.id == item.dish_id).first()
            order_data["items"].append({
                "dish_id": item.dish_id,
                "dish_name": dish.title if dish else "Unknown",
                "price": dish.price if dish else 0,
                "amount": item.amount
            })
        result.append(order_data)
    return result

@app.get("/menu/")
async def get_menu(db: Session = Depends(get_db)):
    menu_items = db.query(Menu).all()
    return [{"id": item.id, "title": item.title, "type": item.type, "price": item.price} for item in menu_items]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)