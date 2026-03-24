"""Authentication and user management"""
from datetime import datetime, timedelta
from typing import Optional
import hashlib
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from pydantic import BaseModel


security = HTTPBearer()


class User(BaseModel):
    """User model"""
    user_id: str
    username: str
    email: Optional[str] = None
    created_at: datetime = datetime.now()
    is_active: bool = True


class TokenData(BaseModel):
    """Token payload"""
    user_id: str
    exp: datetime


class UserManager:
    """Manage users (in-memory for now, can be extended to DB)"""
    
    def __init__(self):
        self.users: dict = {}
        self.tokens: dict = {}
    
    def create_user(self, username: str, email: Optional[str] = None) -> User:
        """Create a new user"""
        user_id = secrets.token_urlsafe(16)
        user = User(user_id=user_id, username=username, email=email)
        self.users[user_id] = user
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def list_users(self) -> list:
        """List all users"""
        return list(self.users.values())
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
    
    def generate_token(self, user_id: str) -> str:
        """Generate API token for user"""
        if user_id not in self.users:
            raise ValueError(f"User {user_id} not found")
        
        token = secrets.token_urlsafe(32)
        exp = datetime.now() + timedelta(days=30)
        self.tokens[token] = {
            'user_id': user_id,
            'exp': exp
        }
        return token
    
    def validate_token(self, token: str) -> Optional[str]:
        """Validate token and return user_id"""
        if token not in self.tokens:
            return None
        
        token_data = self.tokens[token]
        if datetime.now() > token_data['exp']:
            del self.tokens[token]
            return None
        
        return token_data['user_id']
    
    def revoke_token(self, token: str) -> bool:
        """Revoke token"""
        if token in self.tokens:
            del self.tokens[token]
            return True
        return False


# Global user manager
user_manager = UserManager()


async def verify_token(credentials: HTTPAuthCredentials = Depends(security)) -> str:
    """Verify API token"""
    token = credentials.credentials
    user_id = user_manager.validate_token(token)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return user_id
