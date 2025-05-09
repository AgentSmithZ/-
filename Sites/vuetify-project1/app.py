from fastapi import FastAPI, Request, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
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

# Таблица ролей
class RolesTable(sqlalchemy.Table):
    roles = sqlalchemy.Table(
        "roles",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("role", sqlalchemy.String(length=50), unique=True, nullable=False)
    )

# Таблица пользователей
class UsersTable(sqlalchemy.Table):
    users = sqlalchemy.Table(
        "users",
        metadata,
        sqlalchemy.Column("nickname", sqlalchemy.String(length=50), primary_key=True),
        sqlalchemy.Column("password", sqlalchemy.String(length=255), nullable=False),  # Пароль хранится открытым текстом
        sqlalchemy.Column("role_id", None, sqlalchemy.ForeignKey(RolesTable.roles.c.id))
    )

from pydantic import BaseModel

class RegisterUserSchema(BaseModel):
    login: str
    password: str
    roles: List[str]

metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
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

@app.post("/auth")
async def auth(request_data: AuthRequest, session: Session = Depends(get_db)):
    # Попытайтесь вывести диагностические сообщения
    print(f"Получил запрос на авторизацию с никнеймом: {request_data.nickname}")

    # Проверяем существование пользователя
    query = UsersTable.users.select().where(UsersTable.users.c.nickname == request_data.nickname)
    result = await session.fetch_one(query)
    if not result:
        print(f"Пользователь '{request_data.nickname}' не найден.")
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    # Проверяем пароль
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

@app.get("/users/list")
async def list_users(db_session: Session = Depends(get_db)):
    users_query = UsersTable.users.select()
    results = await db_session.fetch_all(users_query)
    return [{ "id": row.id, "login": row.nickname, "roles": row.role_id } for row in results]

@app.post("/users/register")
async def register_user(user_data: RegisterUserSchema, db_session: Session = Depends(get_db)):
    existing_user = await db_session.execute(UsersTable.users.select().where(UsersTable.users.c.nickname == user_data.login))
    if existing_user.first():
        raise HTTPException(status_code=400, detail="Пользователь с данным логином уже существует!")

    insert_stmt = UsersTable.users.insert().values(
    nickname=user_data.login,
    password=user_data.password,  # Без хэширования
    role_id=get_role_id_from_roles(user_data.roles)
)
    await db_session.execute(insert_stmt)
    await db_session.commit()

    return {"detail": "Пользователь успешно зарегистрирован."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)