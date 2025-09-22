from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import torch
from PIL import Image
import io
import os

from .models import UserRegister, UserLogin, UserResponse, ErrorResponse, TokenResponse, SimilarMoleSelection
from .auth import AuthService
from .ml_model import load_model, inference
from .supabase_client import supabase_client as supabase
from .faiss_service import faiss_service

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
    Analyze a mole image and store the results with FAISS similarity search.
    """
    try:
        print(f"Starting analysis for user: {current_user.get('national_id', 'unknown')}")
        
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        print(f"File type validated: {file.content_type}")
        
        # Read image from upload
        image_bytes = await file.read()
        print(f"Image read successfully, size: {len(image_bytes)} bytes")

        # Get prediction
        print("Running CNN inference...")
        cnn_result, embedding_list = inference(model, image_bytes)
        print(f"CNN inference completed. Result: {cnn_result}, Embedding dimensions: {len(embedding_list)}")
        
        # Get national_id from the authenticated user
        national_id = current_user['national_id']

        # Store results in Supabase
        print("Storing results in Supabase...")
        insert_response = supabase.table("cnn_results").insert({
            "national_id": national_id,
            "cnn_result": float(cnn_result),  # Ensure it's a float
            "embedding": embedding_list
        }).execute()

        # Check if Supabase returned an error
        if hasattr(insert_response, 'error') and insert_response.error is not None:
            print(f"Supabase error: {insert_response.error}")
            raise HTTPException(status_code=500, detail=f"Failed to store results: {insert_response.error}")

        print("Results stored successfully in Supabase")

        # Perform FAISS similarity search
        print("Starting FAISS similarity search...")
        similar_images_with_metadata = []
        try:
            # Check if FAISS service is ready
            if not faiss_service.embeddings_loaded:
                print("FAISS embeddings not loaded, attempting to load...")
                load_success = await faiss_service.load_embeddings()
                if not load_success:
                    print("FAISS embeddings could not be loaded - similarity search unavailable")
                    similar_images_with_metadata = []
                else:
                    print("FAISS embeddings loaded successfully")
            
            # Only proceed if embeddings are available
            if faiss_service.embeddings_loaded:
                similar_images = await faiss_service.find_similar_images(embedding_list, k=9)
                print(f"Found {len(similar_images)} similar images")
                
                if similar_images:
                    # Get metadata for similar images
                    similar_image_ids = [img_id for img_id, _ in similar_images]
                    similar_images_metadata = await faiss_service.get_image_metadata(similar_image_ids)
                    print(f"Retrieved metadata for {len(similar_images_metadata)} images")
                    
                    # Create a mapping of image_id to metadata for easy lookup
                    metadata_dict = {item['image_id']: item for item in similar_images_metadata}
                    
                    # Combine similarity results with metadata
                    for image_id, distance in similar_images:
                        metadata = metadata_dict.get(image_id, {})
                        similar_images_with_metadata.append({
                            "image_id": image_id,
                            "distance": distance,
                            "image_url": metadata.get("image_url", ""),
                            "diagnosis": metadata.get("dx", "unknown"),
                            "age": metadata.get("age", None),
                            "sex": metadata.get("sex", "unknown"),
                            "localization": metadata.get("localization", "unknown")
                        })
                else:
                    print("No similar images found")
            else:
                print("FAISS service not ready - skipping similarity search")
            
        except Exception as faiss_error:
            print(f"FAISS error (continuing without similar images): {str(faiss_error)}")
            import traceback
            traceback.print_exc()
            similar_images_with_metadata = []

        # The inserted row should be available in the `data` attribute
        if insert_response.data:
            inserted_data = insert_response.data[0]
            result = {
                "message": "Analysis successful",
                "cnn_result": inserted_data.get("cnn_result"),
                "embedding_dimensions": len(inserted_data.get("embedding", [])),
                "similar_images": similar_images_with_metadata
            }
            print(f"Analysis complete. Returning result with {len(similar_images_with_metadata)} similar images")
            return result

        # Fallback if no data was returned
        result = {
            "message": "Analysis successful but no data returned from DB",
            "cnn_result": float(cnn_result),
            "embedding_dimensions": len(embedding_list),
            "similar_images": similar_images_with_metadata
        }
        print(f"Analysis complete (fallback). Returning result with {len(similar_images_with_metadata)} similar images")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in analyze_mole: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An error occurred during analysis: {str(e)}")


@app.post("/api/save_similar_moles")
async def save_similar_moles(
    selection: SimilarMoleSelection,
    current_user: dict = Depends(AuthService.get_current_user)
):
    """
    Save the user's selection of similar moles and return a recommendation.
    """
    try:
        national_id = current_user['national_id']
        selected_ids = selection.selected_ids

        # Pad the list with None if fewer than 3 images were selected
        image_ids = selected_ids + [None] * (3 - len(selected_ids))

        # Create the record to insert
        record = {
            "national_id": national_id,
            "image_id1": image_ids[0],
            "image_id2": image_ids[1],
            "image_id3": image_ids[2],
        }

        # Insert into Supabase
        insert_response = supabase.table("similar_moles_ann_user").insert(record).execute()

        if hasattr(insert_response, 'error') and insert_response.error:
            raise HTTPException(status_code=500, detail=f"Failed to save selection: {insert_response.error}")

        # --- Recommendation Logic ---

        # 1. Get latest CNN result
        cnn_response = supabase.table("cnn_results").select("cnn_result").eq("national_id", national_id).order("timestamp", desc=True).limit(1).execute()
        latest_cnn_result = cnn_response.data[0]['cnn_result'] if cnn_response.data else None

        # 2. Get latest questionnaire answers
        questionnaire_response = supabase.table("mole_questionnaires").select("q1, q2, q3, q4, q5").eq("national_id", national_id).order("timestamp", desc=True).limit(1).execute()
        yes_answers = 0
        if questionnaire_response.data:
            answers = questionnaire_response.data[0]
            yes_answers = sum(1 for q in ['q1', 'q2', 'q3', 'q4', 'q5'] if answers.get(q) is True)

        # 3. Check diagnosis of selected similar moles
        has_melanoma_selection = False
        if selected_ids:
            metadata_response = supabase.table("ham_metadata").select("dx").in_("image_id", selected_ids).eq("dx", "mel").execute()
            if metadata_response.data:
                has_melanoma_selection = True

        # --- Determine Recommendation ---
        
        plastic_surgeon_msg = "According to the data you have provided to DermaFast, we highly recommend you schedule a meeting with a plastic surgeon."
        dermatologist_msg = "According to the data you have provided to DermaFast, we highly recommend you schedule a meeting with a dermatologist."
        monitoring_msg = "According to the data you have provided to DermaFast, we highly recommend you continue monitoring your moles and beauty marks, and visit a dermatologist at least once a year."

        recommendation_message = ""

        # Condition for Plastic Surgeon
        is_plastic_surgeon_case = (
            (latest_cnn_result is not None and latest_cnn_result >= 0.4) or
            (yes_answers >= 2) or
            has_melanoma_selection
        )

        if is_plastic_surgeon_case:
            recommendation_message = plastic_surgeon_msg
        else:
            # Condition for Dermatologist
            is_dermatologist_case = (
                (latest_cnn_result is not None and 0.2 < latest_cnn_result < 0.4) or
                (yes_answers == 1)
            )
            if is_dermatologist_case:
                recommendation_message = dermatologist_msg
            else:
                recommendation_message = monitoring_msg
        
        # --- Store Recommendation in the new table ---
        try:
            supabase.table("final_recommendation").insert({
                "national_id": national_id,
                "recommendation": recommendation_message
            }).execute()
        except Exception as e:
            # Log the error but don't fail the request
            print(f"Could not save recommendation to 'final_recommendation' table: {e}")

        return {
            "message": "Selection saved successfully",
            "recommendation": recommendation_message
        }

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


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
