# Import FastAPI router, status codes, and dependency injection tools,
from app.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.database import get_db
from app.models import User
from app.schemas import Token, UserCreate, UserResponse
from fastapi import APIRouter, Depends, HTTPException, status

# OAuth2 form dependency to handle standard username/password login form data
from fastapi.security import OAuth2PasswordRequestForm

# SQLAlchemy session for database interactions
from sqlalchemy.orm import Session

# Initalize an APIRouter group authentication routes
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    """Registers a new user account with hashed password."""
    # Check if the email is already registered/user already exists in the database
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    # Hash the raw password before saving it to the database for security
    hashed_password = get_password_hash(user.password)

    # Create a new User database model instance
    hashed_password = get_password_hash(user.password)

    # Create a new User database model instance 
    new_user = User(email=user.email, hashed_password=hashed_password)

    db.add(new_user)  # Add the new user to the database session
    db.commit()  # Commit the transaction to save the new user
    db.refresh(new_user)  # Refresh the instance to get the updated data from the database
    return new_user # Return the newly created user data (excluding password) as a response

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    """Authenticates a user and returns a JWT access token."""
    # Fetches the user from the database based on the provided email (username).
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},

        )
    # Create a JWT access token with the user's email as the subject and an expiration time.
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=30)
    )

    return {"access_token": access_token, "token_type": "bearer"} # Return the access token and token type in the response
    