from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import User
from .schemas import UserCreate, TokenResponse
from .security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created"}

@router.post("/login", response_model=TokenResponse)
def login(user: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.username})

    return {"access_token": token}