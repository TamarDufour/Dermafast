import bcrypt
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional
import jwt
from fastapi import Header, HTTPException, status

from .supabase_client import supabase_client

# JWT Configuration
SECRET_KEY = "your-secret-key"  # Should be in .env file
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    
    @staticmethod
    async def create_user(national_id: str, password: str) -> bool:
        """Create a new user in the Supabase 'users' table"""
        try:
            # Check if user already exists
            response = supabase_client.from_("users").select("id").eq("national_id", national_id).execute()
            if response.data:
                return False  # User already exists

            password_hash = AuthService.hash_password(password)
            
            # Insert new user
            insert_response = supabase_client.from_("users").insert({
                "national_id": national_id,
                "password_hash": password_hash,
            }).execute()

            # Check if insert was successful
            if not insert_response.data:
                # Log error or handle it more gracefully
                print(f"Error creating user: {insert_response.get('error')}")
                return False
            
            return True
        except Exception as e:
            print(f"An unexpected error occurred in create_user: {e}")
            return False
    
    @staticmethod
    async def authenticate_user(national_id: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user from Supabase and update their last_login.
        Returns user data on success, None on failure.
        """
        try:
            response = supabase_client.from_("users").select("id, password_hash, last_login").eq("national_id", national_id).execute()
            
            if not response.data:
                return None  # User not found

            user_data = response.data[0]
            
            if not AuthService.verify_password(password, user_data['password_hash']):
                return None  # Invalid password
            
            previous_last_login = user_data.get("last_login")
            
            # Update last_login timestamp
            current_time = datetime.now(timezone.utc).isoformat()
            supabase_client.from_("users").update({
                "last_login": current_time
            }).eq("national_id", national_id).execute()

            # Create access token
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = AuthService.create_access_token(
                data={"sub": user_data['id'], "national_id": national_id}, 
                expires_delta=access_token_expires
            )

            return {
                "national_id": national_id,
                "last_login": previous_last_login,
                "access_token": access_token,
                "token_type": "bearer"
            }
        except Exception as e:
            print(f"An unexpected error occurred in authenticate_user: {e}")
            return None

    @staticmethod
    async def get_current_user(authorization: str = Header(...)) -> Dict[str, Any]:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            token_type, token = authorization.split()
            if token_type.lower() != "bearer":
                raise credentials_exception
            
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            
            # Fetch user from DB to ensure they exist
            response = supabase_client.from_("users").select("id, national_id").eq("id", user_id).execute()
            if not response.data:
                raise credentials_exception
            
            return response.data[0]
        except (jwt.PyJWTError, ValueError):
            raise credentials_exception
