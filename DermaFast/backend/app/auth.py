import bcrypt
from datetime import datetime
from typing import Dict, Any, Optional

# In-memory user store for demonstration
# In a real app, use a proper database
db = {}

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @staticmethod
    async def create_user(national_id: str, password: str) -> bool:
        """Create a new user in the in-memory store"""
        if national_id in db:
            return False  # User already exists
        
        password_hash = AuthService.hash_password(password)
        db[national_id] = {
            "password_hash": password_hash,
            "last_login": None
        }
        return True
    
    @staticmethod
    async def authenticate_user(national_id: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user from the in-memory store and update their last_login.
        Returns user data on success, None on failure.
        """
        user = db.get(national_id)
        
        if not user:
            return None  # User not found
        
        if not AuthService.verify_password(password, user['password_hash']):
            return None  # Invalid password
            
        previous_last_login = user["last_login"]
        
        # Update last_login timestamp
        user["last_login"] = datetime.now().isoformat()
        
        return {
            "national_id": national_id,
            "last_login": previous_last_login
        }
