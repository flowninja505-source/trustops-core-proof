import os
from supabase import create_client
from dotenv import load_dotenv

# Load .env
load_dotenv(dotenv_path=".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("Supabase credentials not set in environment")

# Export only the client
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
