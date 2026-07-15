import os
import streamlit as st
from dotenv import load_dotenv

# Load local .env if it exists
load_dotenv()

# Try to get API key from Streamlit secrets first
API_KEY = None
try:
    if "GOOGLE_GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GOOGLE_GEMINI_API_KEY"]
    elif "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

# If not found in secrets, fallback to environment variables
if not API_KEY:
    API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")