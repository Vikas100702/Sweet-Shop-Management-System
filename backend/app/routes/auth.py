from imports import (
    APIRouter, Depends, HTTPException, Session, List, status,
    verify_password, hash_password, create_access_token, get_current_user
)
from database.database import get_db
from schema.auth_schema import UserLoginSchema, TokenResponseSchema
from schema.user_schema import UserResponseSchema, UserCreateSchema
from models.user_model import UserModel

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# User Registration
@router.post("/register", response_model=UserResponseSchema)
def register_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    new_user = UserModel(
        first_name=user.first_name,
        last_name=user.last_name,
        gender=user.gender,
        email=user.email,
        phone_number=user.phone_number,
        role=user.role,
        password_hash=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Get all Users
@router.get("/users", response_model=List[UserResponseSchema])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

# Login API
@router.post("/login", response_model=TokenResponseSchema)
def login(login_data: UserLoginSchema, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == login_data.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
        )

    access_token = create_access_token(
        data={"sub": str(user.user_id), "role": user.role}
    )

    return TokenResponseSchema(access_token=access_token)

# Protected Route Example
@router.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "message": f"Hello, {current_user['sub']}! Your role is {current_user['role']}."
    }
