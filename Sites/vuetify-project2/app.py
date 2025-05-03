from fastapi import FastAPI, Request, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from jose import jwt, ExpiredSignatureError, JWTError
import databases
import sqlalchemy
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from datetime import timedelta, datetime
from typing import Optional, List

SECRET_KEY = "123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATABASE_URL = "sqlite:///./database.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = SessionLocal()

# Таблица ролей
class RolesTable(sqlalchemy.Table):
    roles = sqlalchemy.Table(
        "roles",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("role", sqlalchemy.String(length=50), unique=True, nullable=False)
    )

# Таблица пользователей
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

# Таблица процесса приготовления
class CookingProcess(Base):
    __tablename__ = "cooking_process"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_item_id = Column(Integer, ForeignKey("order_items.id"), nullable=False)
    status = Column(String(50), nullable=False, default='waiting')

# Таблица смен сотрудников
class Shift(Base):
    __tablename__ = "shifts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


Base.metadata.create_all(engine)

class RegisterUserSchema(BaseModel):
    login: str
    password: str
    roles: List[str]

metadata.create_all(engine)

app = FastAPI()

origins = ["http://localhost:3000"]  # Адрес вашего фронтенда

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

async def get_db():
    try:
        await database.connect()
        yield database
    finally:
        await database.disconnect()

class AuthRequest(BaseModel):
    nickname: str
    password: str

# Модель данных для нового заказа
class NewOrder(BaseModel):
    table_number: int
    guest_count: int
    items: List[int]  # Список ID блюд и напитков

# Маршрут для получения списка заказов
@app.get("/orders/")
async def get_orders():
    query = Order.__table__.select()
    rows = await database.fetch_all(query)
    return [dict(row._mapping) for row in rows]

@app.post("/orders/")
async def create_order(order: dict):
    new_order = {
        "date_order": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": order.get("user_id"),
        "table_number": order.get("table_number"),
        "guest_count": order.get("guest_count")
    }

    query = Order.__table__.insert().values(**new_order)
    inserted_order = await database.execute(query)

    if "items" in order:
        for item in order["items"]:
            query = OrderItem.__table__.insert().values(
                order_id=inserted_order,
                dish_id=item["dish_id"],
                amount=item.get("amount", 1)
            )
            await database.execute(query)

    return {"message": "Заказ успешно создан", "order_id": inserted_order}

@app.post("/auth")
async def auth(request_data: AuthRequest, session: Session = Depends(get_db)):
    print(f"Получил запрос на авторизацию с никнеймом: {request_data.nickname}")

    query = UsersTable.users.select().where(UsersTable.users.c.nickname == request_data.nickname)
    result = await session.fetch_one(query)
    if not result:
        print(f"Пользователь '{request_data.nickname}' не найден.")
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    if result["password"] != request_data.password:
        print(f"Некорректный пароль для пользователя '{request_data.nickname}'.")
        raise HTTPException(status_code=401, detail="Пароль неверный")

    return {
        "token": "example-token",
        "user": request_data.nickname
    }

@app.options("/auth")
async def options_auth():
    return {}

@app.post("/auth/token")
async def login_for_access_token(form_data: AuthRequest, db_session: Session = Depends(get_db)):
    user_query = UsersTable.users.select().where(UsersTable.users.c.nickname == form_data.nickname)
    user_result = await db_session.fetch_one(user_query)
    
    if not user_result or user_result['password'] != form_data.password:
        raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_result['nickname'], "role": user_result['role_id']},
        expires_delta=access_token_expires
    )

    response = {"access_token": access_token, "token_type": "bearer"}
    return response

@app.post("/orders/create/")
async def create_new_order(order_data: NewOrder, db_session: Session = Depends(get_db)):
    current_time = datetime.now()
    insert_order_stmt = OrdersTable.orders.insert().values(
        date_order=current_time,
        table_number=order_data.table_number,
        guest_count=order_data.guest_count
    )
    result = await db_session.execute(insert_order_stmt)
    order_id = result.lastrowid

    # Добавляем позиции в заказ
    for item_id in order_data.items:
        insert_item_stmt = OrderItemsTable.order_items.insert().values(
            order_id=order_id,
            dish_id=item_id
        )
        await db_session.execute(insert_item_stmt)

    await db_session.commit()
    return {"message": f"Заказ успешно создан, ID заказа: {order_id}"}

@app.get("/orders/all/")
async def get_orders_list(db_session: Session = Depends(get_db)):
    orders_query = OrdersTable.orders.select()
    results = await db_session.fetch_all(orders_query)
    return results

@app.get("/users/list")
async def list_users(db_session: Session = Depends(get_db)):
    users_query = UsersTable.users.select()
    results = await db_session.fetch_all(users_query)
    return [{ "id": row.id, "login": row.nickname, "roles": row.role_id } for row in results]

async def get_role_id_from_roles(role_names: List[str], db_session: Session):
    """ Получает ID ролевых записей из базы данных по списку имен ролей. Возвращает первый найденный идентификатор роли. """
    query = RolesTable.roles.select().where(RolesTable.roles.c.role.in_(role_names))
    results = await db_session.fetch_all(query)
    if len(results) > 0:
        return results[0].id
    else:
        raise ValueError("Нет соответствующей роли в базе данных.")

@app.post("/users/register")
async def register_user(user_data: RegisterUserSchema, db_session: Session = Depends(get_db)):
    # Проверяем существование пользователя
    existing_user = await db_session.execute(UsersTable.users.select().where(UsersTable.users.c.nickname == user_data.login))
    if existing_user.first():
        raise HTTPException(status_code=400, detail="Пользователь с данным логином уже существует!")

    # Найти первую подходящую роль из указанной
    role_id = await get_role_id_from_roles(user_data.roles, db_session)

    # Сохраняем пользователя в базу данных
    insert_stmt = UsersTable.users.insert().values(
        nickname=user_data.login,
        password=user_data.password,  # Не забудьте обеспечить безопасное хранение паролей!
        role_id=role_id
    )
    await db_session.execute(insert_stmt)
    await db_session.commit()

    return {"detail": "Пользователь успешно зарегистрирован."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)