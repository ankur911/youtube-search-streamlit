"""
YouTube Search App - Minimal HF Version
Bypasses Streamlit configuration issues on Hugging Face Spaces
"""

import os
import tempfile
import sys

# Set Streamlit environment variables BEFORE any Streamlit imports
os.environ.update({
    'STREAMLIT_SERVER_HEADLESS': 'true',
    'STREAMLIT_SERVER_PORT': '7860',
    'STREAMLIT_BROWSER_GATHER_USAGE_STATS': 'false',
    'STREAMLIT_GLOBAL_DEVELOPMENT_MODE': 'false',
    'STREAMLIT_LOGGER_LEVEL': 'error',
    'STREAMLIT_CLIENT_CACHING': 'false',
    'STREAMLIT_CLIENT_DISPLAY_ENABLED': 'false'
})

# Create temp directory for Streamlit cache
temp_dir = tempfile.gettempdir()
os.environ['STREAMLIT_CONFIG_DIR'] = temp_dir

import streamlit as st

# Suppress Streamlit warnings
st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
    """Minimal YouTube Search App"""
    
    st.title("🎥 YouTube Search App")
    
    # Check API key
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        st.error("🔑 **YouTube API Key Required**")
        st.markdown("""
        **Setup Instructions:**
        1. Go to your HF Space → **Settings** → **Variables and secrets**
        2. Add **Secret**: Name = `YOUTUBE_API_KEY`, Value = your YouTube API key
        3. Get API key from [Google Cloud Console](https://console.cloud.google.com/)
        4. Enable YouTube Data API v3
        """)
        return
    
    st.success("✅ API Key Found")
    
    # Simple search interface
    query = st.text_input("🔍 Search YouTube:", placeholder="Enter your search...")
    
    if query:
        try:
            # Import here to avoid early import issues
            sys.path.append('src')
            from googleapiclient.discovery import build
            
            # Initialize YouTube API
            youtube = build('youtube', 'v3', developerKey=api_key)
            
            # Search
            with st.spinner("Searching..."):
                request = youtube.search().list(
                    part="snippet",
                    q=query,
                    maxResults=10,
                    type="video"
                )
                results = request.execute()
            
            # Display results
            st.write(f"**Found {len(results['items'])} videos:**")
            
            for item in results['items']:
                video_id = item['id']['videoId']
                title = item['snippet']['title']
                description = item['snippet']['description'][:200] + "..."
                channel = item['snippet']['channelTitle']
                
                with st.expander(f"📹 {title}"):
                    st.write(f"**Channel:** {channel}")
                    st.write(f"**Description:** {description}")
                    st.write(f"**Watch:** https://youtube.com/watch?v={video_id}")
                    
                    # Embed video
                    st.video(f"https://youtube.com/watch?v={video_id}")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.write("Check your API key and try again.")

if __name__ == "__main__":
    main()