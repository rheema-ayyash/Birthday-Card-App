from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User

# Secret key used to crypotgraphically sign JWT tokens
SECRET_KEY =  (
   "7615ad634819bfe2ccc994f451ede9e292b77b322da78fde0051a463030b80c3" 
)  # Replace with a secure random 
ALGORITHM = "HS256"  # Hashing algorithm used for signing JWT tokens
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes

# Initialize passlib context for password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="auth/token")  # URL endpoint for obtaining JWT tokens

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plaintext password using bcrypt."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Creates a JWT access token with an optional expiration time."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """FastAPI Dependency: decodes JWT from request header and fetches authenication."""
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email:str = payload.get("sub")
        if email is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    user = deb.query(User).filter(User.email == email).first()
    if user is None:
        raise credential_exception
    return user




