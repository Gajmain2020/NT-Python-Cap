from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.auth.schemas import SignupSchema, LoginSchema
from app.auth.utils import hash_password, verify_password, create_access_token, create_refresh_token
from app.auth.models import User
from app.utils.response import create_response

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/')
def health_check():
    return create_response(data={"message": "Health Check is done."})

@router.post("/signup")
def signup(payload: SignupSchema, db: Session = Depends(get_db)):
    # check if user exists
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return create_response(data={"message": "User created successfully"})

@router.post("/signin")
def signin(payload: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    return create_response(data={"access_token": access_token, "refresh_token": refresh_token})
    