from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import uuid
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

app = FastAPI()

DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    dob = Column(String)
    location = Column(String)
    sex = Column(String)
    userid = Column(String, unique=True, index=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    name: str
    email: str
    phone_number: str
    dob: str
    location: str
    sex: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    name: str = None
    phone_number: str = None
    dob: str = None
    location: str = None
    sex: str = None
    password: str = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    user_id = str(uuid.uuid4())
    dob = datetime.strptime(user.dob, "%Y-%m-%d").date()
    user_data = user.dict()
    user_data.pop('dob', None)
    existing_user = db.query(User).filter(User.email == user_data["email"]).first()
    if existing_user:
        raise ValueError("Email already in use")
    db_user = User(userid=user_id,dob= dob ,  **user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"userid": user_id, "message": "User registered successfully"}

@app.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}

@app.put("/update/{email}")
def update_user(email: str, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return {"message": "User updated successfully"}

@app.delete("/delete/{email}")
def delete_user(email: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
