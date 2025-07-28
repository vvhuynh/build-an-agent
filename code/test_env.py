"""
Test environment variable loading
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("../variables.env")

print("Testing environment variable loading...")
print(f"NVIDIA_API_KEY: {os.getenv('NVIDIA_API_KEY')}")
print(f"API Key length: {len(os.getenv('NVIDIA_API_KEY', ''))}")
print(f"API Key starts with: {os.getenv('NVIDIA_API_KEY', '')[:20]}...") 