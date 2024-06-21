## Dear Priya 

## Backend API Development Task User Management

### Overview
In this task, you will develop a backend API using Python with FastAPI and SQLite. The API will manage user data and provide endpoints for user registration, login, updating user information, deleting users, and retrieving all users.

### Prerequisites
- Install Python (preferably 3.7 or higher)
- Install SQLite
- Install FastAPI and relevant dependencies

### Reference Links
- **SQLite Installation on Windows**: [SQLite Installation Guide](https://www.tutorialspoint.com/sqlite/sqlite_installation.htm)
- **FastAPI with SQLite Tutorial**: [FastAPI SQLite Tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/)

### Task Breakdown

#### 1. Project Setup

**Subtask**: Set up the project environment.
- Install Python.
- Set up a virtual environment.
- Install FastAPI and Uvicorn.
- Install SQLite and SQLAlchemy for database interactions.

**Expected Result**: A clean environment with all dependencies installed and a project directory ready for development.

**Steps**:
1. Install Python from the official website.
2. Create a virtual environment:
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
   ```
3. Install FastAPI and Uvicorn:
   ```bash
   pip install fastapi uvicorn sqlalchemy sqlite
   ```

#### 2. Database Setup

**Subtask**: Set up the SQLite database and create a table for users.

**Expected Result**: A SQLite database file with a users table.

**Steps**:
1. Create a SQLite database file (e.g., `users.db`).
2. Define the user schema using SQLAlchemy.
   ```python
   from sqlalchemy import create_engine, Column, Integer, String, Date
   from sqlalchemy.ext.declarative import declarative_base
   from sqlalchemy.orm import sessionmaker

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
       dob = Column(Date)
       location = Column(String)
       sex = Column(String)
       userid = Column(String, unique=True, index=True)
       password = Column(String)

   Base.metadata.create_all(bind=engine)
   ```

#### 3. API Endpoints

**Subtask**: Implement API endpoints for user registration, login, updating user information, deleting users, and retrieving all users.

##### a. User Registration

**Expected Result**: An endpoint to register a new user, generating a unique user ID.

**Steps**:
1. Define the registration endpoint.
2. Generate a unique user ID.
3. Save the user data to the database.

Example:
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from sqlalchemy.orm import Session

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str
    phone_number: str
    dob: str
    location: str
    sex: str
    password: str

@app.post("/register")
def register_user(user: UserCreate, db: Session = SessionLocal()):
    user_id = str(uuid.uuid4())
    db_user = User(userid=user_id, **user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"userid": user_id, "message": "User registered successfully"}
```

##### b. User Login

**Expected Result**: An endpoint to log in a user using email and password.

**Steps**:
1. Define the login endpoint.
2. Validate email and password.

Example:
```python
class UserLogin(BaseModel):
    email: str
    password: str

@app.post("/login")
def login_user(user: UserLogin, db: Session = SessionLocal()):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}
```

##### c. Update User Information

**Expected Result**: An endpoint to update user information based on email.

**Steps**:
1. Define the update endpoint.
2. Update user data in the database.

Example:
```python
class UserUpdate(BaseModel):
    name: str = None
    phone_number: str = None
    dob: str = None
    location: str = None
    sex: str = None
    password: str = None

@app.put("/update/{email}")
def update_user(email: str, user: UserUpdate, db: Session = SessionLocal()):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return {"message": "User updated successfully"}
```

##### d. Delete User

**Expected Result**: An endpoint to delete a user based on email.

**Steps**:
1. Define the delete endpoint.
2. Remove user data from the database.

Example:
```python
@app.delete("/delete/{email}")
def delete_user(email: str, db: Session = SessionLocal()):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
```

##### e. Get All Users

**Expected Result**: An endpoint to retrieve all users.

**Steps**:
1. Define the get all users endpoint.
2. Query the database for all users.

Example:
```python
@app.get("/users")
def get_all_users(db: Session = SessionLocal()):
    users = db.query(User).all()
    return users
```

### Deliverables
- A FastAPI application with the following endpoints:
  - POST /register
  - POST /login
  - PUT /update/{email}
  - DELETE /delete/{email}
  - GET /users
- A SQLite database file with user data.
- A README file with instructions on how to run the application and test the endpoints.

### Timeline
This task is designed to be completed within one week. Here is a suggested timeline:
- Day 1-2: Project setup and database setup.
- Day 3-5: Implement API endpoints.
- Day 6: Testing and debugging.
- Day 7: Documentation and final review.

