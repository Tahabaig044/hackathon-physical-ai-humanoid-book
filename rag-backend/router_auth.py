from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional

from config import settings
from neon_client import neon_client

router = APIRouter(prefix="/auth", tags=["authentication"])

security = HTTPBearer()

class UserCreateRequest(BaseModel):
    username: str
    email: str
    password: str

class UserLoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get the current user from the token"""
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

@router.post("/signup", response_model=UserResponse)
async def signup(user_data: UserCreateRequest):
    """Register a new user"""
    try:
        # Check if user already exists
        query = "SELECT id FROM users WHERE username = $1 OR email = $2"
        result = await neon_client.execute_query(query, user_data.username, user_data.email)

        if result:
            raise HTTPException(status_code=400, detail="Username or email already registered")

        # Hash the password
        hashed_password = hash_password(user_data.password)

        # Insert the new user
        insert_query = """
            INSERT INTO users (username, email, password_hash, created_at)
            VALUES ($1, $2, $3, $4)
            RETURNING id
        """
        result = await neon_client.execute_query(
            insert_query,
            user_data.username,
            user_data.email,
            hashed_password,
            datetime.utcnow()
        )

        user_id = result[0]['id']

        return UserResponse(
            id=user_id,
            username=user_data.username,
            email=user_data.email
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLoginRequest):
    """Authenticate a user and return an access token"""
    try:
        # Find the user by username
        query = "SELECT id, password_hash FROM users WHERE username = $1"
        result = await neon_client.execute_query(query, user_data.username)

        if not result:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        user = result[0]
        user_id = user['id']
        stored_password_hash = user['password_hash']

        # Verify the password
        if not verify_password(user_data.password, stored_password_hash):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"user_id": user_id}, expires_delta=access_token_expires
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@router.post("/logout")
async def logout(current_user: int = Depends(get_current_user)):
    """Logout the current user (for token-based auth, this is typically handled on the client side)"""
    # In a real application, you might want to implement token blacklisting
    return {"message": "Successfully logged out"}