import os
from dotenv import load_dotenv
from supabase import create_client

# Load .env automatically on import
load_dotenv(dotenv_path=".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # service role key for inserts

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials not set in .env")

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
