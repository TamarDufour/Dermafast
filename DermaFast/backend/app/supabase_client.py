import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def get_supabase_client() -> Client:
    """
    Initializes and returns the Supabase client.
    """
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError("Supabase URL and service key must be set in .env file")

    return create_client(supabase_url, supabase_key)

supabase_client = get_supabase_client()
