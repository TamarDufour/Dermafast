import bcrypt
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from .supabase_client import supabase_client

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
            response = supabase_client.from_("users").select("password_hash, last_login").eq("national_id", national_id).execute()
            
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
            
            return {
                "national_id": national_id,
                "last_login": previous_last_login
            }
        except Exception as e:
            print(f"An unexpected error occurred in authenticate_user: {e}")
            return None
