from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.auth.schemas import SignupSchema, LoginSchema, ResetPasswordSchema, ForgotPasswordRequestSchema
from app.auth.utils import hash_password, verify_password, create_access_token, create_refresh_token, verify_token, create_reset_token, send_reset_email
from app.auth.models import User
from app.utils.response import create_response
from jose import JWTError
from typing import Optional

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


# ###################### USER MANAGEMENT ROUTES ######################

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
    access_token = create_access_token(data={"sub": user.email, "role": user.role.value})
    refresh_token = create_refresh_token(data={"sub": user.email, "role": user.role.value})
    return create_response(data={"access_token": access_token, "refresh_token": refresh_token})
    
@router.post("/reset-password")
def reset_password(
    payload: ResetPasswordSchema,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")

    token = authorization.split(" ")[1]

    try:
        payload_data = verify_token(token)
        user_email = payload_data.get("sub")
        if not user_email:
            raise HTTPException(status_code=400, detail="Invalid token")

        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.hashed_password = hash_password(payload.new_password)
        db.commit()

        return create_response(data={"message": "Password reset successfully"})

    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid or expired")

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequestSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email does not exist."
        )

    token = create_reset_token({"sub": user.email, "role": user.role.value})
    send_reset_email(to_email=user.email, token=token)
    
    return create_response(data={"message": "Password reset link sent to your email."})  
