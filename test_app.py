"""
Simple test app to verify Hugging Face Spaces deployment
"""

import streamlit as st

st.title("🎉 Hugging Face Test - Working!")
st.write("If you see this message, your Hugging Face Space is working correctly.")

# Test environment variable
import os
api_key = os.getenv('YOUTUBE_API_KEY')
if api_key:
    st.success(f"✅ YouTube API Key is set (length: {len(api_key)} characters)")
else:
    st.error("❌ YouTube API Key not found in environment variables")

st.write("Next step: Upload the full YouTube Search App!")