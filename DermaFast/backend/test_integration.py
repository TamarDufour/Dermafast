import pytest
import os
from fastapi.testclient import TestClient
from supabase import create_client, Client
from dotenv import load_dotenv
from backend.app.main import app
from backend.app.auth import AuthService

# Load environment variables from .env file
load_dotenv()

# --- Test Setup ---
# It's crucial that you have a .env file in your backend directory with these variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY") # Use service key for admin operations like user deletion

# Ensure credentials are provided
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL and Key must be set in your .env file for integration tests.")

# Create a real Supabase client for test setup/teardown
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

TEST_USER_ID = "integration_test_user"

# Mock authentication for the TestClient
async def override_get_current_user():
    return {"national_id": TEST_USER_ID}

app.dependency_overrides[AuthService.get_current_user] = override_get_current_user

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_teardown_db():
    # --- Setup ---
    # 1. Create a user record to satisfy the foreign key constraint
    user_record = {
        "national_id": TEST_USER_ID,
        "password_hash": "a_fake_password_hash_for_testing"
    }
    supabase.table("users").insert(user_record).execute()
    
    # 2. Insert a dummy CNN result for the test user
    supabase.table("cnn_results").insert({
        "national_id": TEST_USER_ID,
        "cnn_result": 0.5,  # This will trigger the "plastic surgeon" recommendation
        "embedding": [0.1] * 256
    }).execute()

    # 3. Insert dummy questionnaire answers
    supabase.table("mole_questionnaires").insert({
        "national_id": TEST_USER_ID,
        "q1": False, "q2": False, "q3": False, "q4": False, "q5": False
    }).execute()

    yield # This is where the test runs

    # --- Teardown ---
    # Clean up all created records to leave the database clean
    supabase.table("final_recommendation").delete().eq("national_id", TEST_USER_ID).execute()
    supabase.table("similar_moles_ann_user").delete().eq("national_id", TEST_USER_ID).execute()
    supabase.table("mole_questionnaires").delete().eq("national_id", TEST_USER_ID).execute()
    supabase.table("cnn_results").delete().eq("national_id", TEST_USER_ID).execute()
    supabase.table("users").delete().eq("national_id", TEST_USER_ID).execute()


def test_recommendation_is_stored_in_db():
    """
    Integration test to verify that the recommendation is actually stored
    in the final_recommendation table in the Supabase DB.
    """
    # 1. Call the endpoint to save selection and trigger recommendation
    response = client.post("/api/save_similar_moles", json={"selected_ids": ["ISIC_0024306"]})

    assert response.status_code == 200
    data = response.json()
    assert "recommendation" in data
    assert "plastic surgeon" in data["recommendation"]

    # 2. Query the database directly to verify the record was created
    query_response = supabase.table("final_recommendation").select("*").eq("national_id", TEST_USER_ID).execute()

    # 3. Assert that the data was saved correctly
    assert len(query_response.data) == 1, "A recommendation record should have been created."
    
    saved_record = query_response.data[0]
    assert saved_record["national_id"] == TEST_USER_ID
    assert saved_record["recommendation"] == data["recommendation"]

    print(f"\nSuccessfully verified that recommendation was stored for user '{TEST_USER_ID}'.")
