import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print(f"SUPABASE_URL: {SUPABASE_URL}")
print(f"SUPABASE_KEY: {SUPABASE_KEY[:5]}...") # Hanya tampilkan 5 karakter pertama untuk keamanan

try:
    # Initialize Supabase client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Coba query sederhana ke Supabase
    response = supabase.from_("products").select("*").limit(1).execute()
    
    print("\n✅ Berhasil terhubung ke Supabase!")
    print(f"Data: {response.data}")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}") 