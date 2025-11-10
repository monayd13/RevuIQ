"""
Authentication and Authorization
JWT-based authentication system
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security
security = HTTPBearer()


# ==================== DATA MODELS ====================

class Token(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Token payload data"""
    email: Optional[str] = None
    user_id: Optional[int] = None


class UserCreate(BaseModel):
    """User registration model"""
    email: EmailStr
    password: str
    full_name: str
    business_name: Optional[str] = None


class UserLogin(BaseModel):
    """User login model"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response model"""
    id: int
    email: str
    full_name: str
    role: str
    business_id: Optional[int] = None
    created_at: datetime


# ==================== PASSWORD FUNCTIONS ====================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


# ==================== JWT FUNCTIONS ====================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    
    Args:
        data: Payload data to encode
        expires_delta: Token expiration time
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    """
    Decode and verify a JWT token
    
    Args:
        token: JWT token to decode
        
    Returns:
        TokenData with user information
        
    Raises:
        HTTPException if token is invalid
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        
        if email is None:
            raise credentials_exception
            
        token_data = TokenData(email=email, user_id=user_id)
        return token_data
        
    except JWTError:
        raise credentials_exception


# ==================== AUTHENTICATION DEPENDENCIES ====================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """
    Get current authenticated user from JWT token
    
    Use as dependency in protected routes:
        @app.get("/protected")
        async def protected_route(user: TokenData = Depends(get_current_user)):
            return {"user": user.email}
    """
    token = credentials.credentials
    return decode_access_token(token)


async def get_current_active_user(
    current_user: TokenData = Depends(get_current_user)
) -> TokenData:
    """
    Get current active user (additional checks can be added)
    """
    # TODO: Add database check for user.is_active
    return current_user


# ==================== AUTHENTICATION ROUTES ====================

def authenticate_user(db, email: str, password: str):
    """
    Authenticate a user with email and password
    
    Args:
        db: Database session
        email: User email
        password: Plain text password
        
    Returns:
        User object if authenticated, None otherwise
    """
    from database import User
    
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
        
    return user


def create_user(db, user_data: UserCreate):
    """
    Create a new user
    
    Args:
        db: Database session
        user_data: User registration data
        
    Returns:
        Created user object
    """
    from database import User, Business
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create business if provided
    business_id = None
    if user_data.business_name:
        business = Business(name=user_data.business_name)
        db.add(business)
        db.commit()
        db.refresh(business)
        business_id = business.id
    
    # Create user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        business_id=business_id,
        role="admin" if business_id else "manager"
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


# ==================== EXAMPLE USAGE ====================

if __name__ == "__main__":
    # Test password hashing
    password = "test123"
    hashed = get_password_hash(password)
    print(f"Password: {password}")
    print(f"Hashed: {hashed}")
    print(f"Verified: {verify_password(password, hashed)}")
    
    # Test JWT token
    token = create_access_token(data={"sub": "test@example.com", "user_id": 1})
    print(f"\nJWT Token: {token}")
    
    decoded = decode_access_token(token)
    print(f"Decoded: {decoded}")
