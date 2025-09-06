from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
# Change relative imports to absolute imports
from .models import UserRegister, UserLogin, UserResponse, ErrorResponse
from .auth import AuthService
# from .database import db
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # await db.connect()
    yield
    # Shutdown
    # await db.disconnect()

app = FastAPI(
    title="DermaFast API", 
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "DermaFast API is running successfully"
    }

@app.post("/api/register", response_model=UserResponse)
async def register(user_data: UserRegister):
    """
    Register a new user with national_id and password
    """
    try:
        # Validate input
        if not user_data.national_id or not user_data.password:
            raise HTTPException(
                status_code=400,
                detail="National ID and password are required"
            )
        
        if len(user_data.password) < 6:
            raise HTTPException(
                status_code=400,
                detail="Password must be at least 6 characters long"
            )
        
        # Create user using AuthService
        success = await AuthService.create_user(
            user_data.national_id, 
            user_data.password
        )
        
        if not success:
            raise HTTPException(
                status_code=409,
                detail="User with this national ID already exists"
            )
        
        return UserResponse(
            national_id=user_data.national_id,
            message="User registered successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/api/login", response_model=UserResponse)
async def login(user_data: UserLogin):
    """
    Login user with national_id and password
    """
    try:
        # Validate input
        if not user_data.national_id or not user_data.password:
            raise HTTPException(
                status_code=400,
                detail="National ID and password are required"
            )
        
        # Authenticate user using AuthService
        user_info = await AuthService.authenticate_user(
            user_data.national_id,
            user_data.password
        )
        
        if not user_info:
            raise HTTPException(
                status_code=401,
                detail="Invalid national ID or password"
            )
        
        return UserResponse(
            national_id=user_info["national_id"],
            message="Login successful",
            last_login=user_info["last_login"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to DermaFast API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "register": "/api/register",
            "login": "/api/login"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)