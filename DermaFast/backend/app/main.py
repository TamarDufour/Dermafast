from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import torch
from PIL import Image
import io
import os

from .models import UserRegister, UserLogin, UserResponse, ErrorResponse, TokenResponse
from .auth import AuthService
from .ml_model import BasicCNN, val_transform
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
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
model = BasicCNN()
# This is a placeholder for the path to your trained model weights
MODEL_WEIGHTS_PATH = "DermaFast/backend/app/ml_model/model_weights.pkl"
if os.path.exists(MODEL_WEIGHTS_PATH):
    model.load_state_dict(torch.load(MODEL_WEIGHTS_PATH))
model.eval()

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
        # Read image from upload
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Apply transformations
        image_tensor = val_transform(image).unsqueeze(0)

        # Get prediction
        with torch.no_grad():
            classification, embedding = model(image_tensor)
        
        # Extract values
        cnn_result = classification.item()
        embedding_list = embedding.numpy().flatten().tolist()
        
        # Get user_id from the authenticated user
        user_id = current_user['id']

        # Store results in Supabase
        data, error = await supabase.table("cnn_results").insert({
            "user_id": user_id,
            "cnn_result": cnn_result,
            "embedding": embedding_list
        }).execute()
        
        if error:
            raise HTTPException(status_code=500, detail=f"Failed to store results: {error.message}")

        return {
            "message": "Analysis successful",
            "cnn_result": cnn_result,
            "embedding_dimensions": len(embedding_list)
        }
    except Exception as e:
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