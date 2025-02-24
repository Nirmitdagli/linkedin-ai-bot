import os
from dotenv import load_dotenv

# Load environment variables
print("\n🔹 Loading .env file...\n")  # Debugging
load_dotenv()

# LinkedIn API Credentials
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_COMPANY_ID = os.getenv("LINKEDIN_COMPANY_ID")

# Hugging Face Model (Ensure this exists)
HUGGINGFACE_MODEL = "EleutherAI/gpt-neo-1.3B"  # ✅ Fix added here

# Debugging output
print(f"\n🔹 LINKEDIN_ACCESS_TOKEN: {LINKEDIN_ACCESS_TOKEN[:5]}... (masked)")
print(f"🔹 LINKEDIN_COMPANY_ID: {LINKEDIN_COMPANY_ID}")
print(f"🔹 HUGGINGFACE_MODEL: {HUGGINGFACE_MODEL}")

# Error handling
if not LINKEDIN_ACCESS_TOKEN or not LINKEDIN_COMPANY_ID:
    raise ValueError("\n❌ ERROR: Missing LinkedIn credentials in .env file.")

