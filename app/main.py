from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .database import Base, engine
from .models import User
from .schemas import RegisterRequest, LoginRequest, UserOut
from .security import hash_password, verify_password, create_access_token
from .dependencies import get_db, get_current_user, require_admin

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Secure Access Control API", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/auth/register", response_model=UserOut, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = User(
        username=payload.username.strip().lower(),
        password_hash=hash_password(payload.password),
        is_admin=False,
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="username_exists")

@app.post("/auth/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == payload.username.strip().lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="invalid_credentials")
    return {"access_token": create_access_token(user.id, user.is_admin), "token_type": "bearer"}

@app.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user

@app.get("/admin/users", response_model=list[UserOut])
def list_users(_admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return list(db.scalars(select(User).order_by(User.id)))
