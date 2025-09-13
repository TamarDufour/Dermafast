from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import torch
from PIL import Image
import io
import os

from .models import UserRegister, UserLogin, UserResponse, ErrorResponse, TokenResponse
from .auth import AuthService
from .ml_model import load_model, inference
from .supabase_client import supabase_client as supabase

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown

app = FastAPI(
    title="DermaFast API", 
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
# TODO: Make sure to replace 'model.pth' with the actual path to your model weights file.
model = load_model()


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

@app.post("/api/login", response_model=TokenResponse)
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
        
        return user_info
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
        
@app.post("/api/analyze")
async def analyze_mole(file: UploadFile = File(...), current_user: dict = Depends(AuthService.get_current_user)):
    """
    Analyze a mole image and store the results.
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image from upload
        image_bytes = await file.read()

        # Get prediction
        cnn_result, embedding_list = inference(model, image_bytes)
        
        # Get national_id from the authenticated user
        national_id = current_user['national_id']

        # Store results in Supabase
        insert_response = supabase.table("cnn_results").insert({
            "national_id": national_id,
            "cnn_result": float(cnn_result),  # Ensure it's a float
            "embedding": embedding_list
        }).execute()

        # Check if Supabase returned an error
        if hasattr(insert_response, 'error') and insert_response.error is not None:
            raise HTTPException(status_code=500, detail=f"Failed to store results: {insert_response.error}")

        # The inserted row should be available in the `data` attribute
        if insert_response.data:
            inserted_data = insert_response.data[0]
            return {
                "message": "Analysis successful",
                "cnn_result": inserted_data.get("cnn_result"),
                "embedding_dimensions": len(inserted_data.get("embedding", []))
            }

        # Fallback if no data was returned
        return {
            "message": "Analysis successful but no data returned from DB",
            "cnn_result": float(cnn_result),
            "embedding_dimensions": len(embedding_list)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in analyze_mole: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred during analysis: {str(e)}")


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
            "login": "/api/login",
            "analyze": "/api/analyze"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)