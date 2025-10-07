"""
YouTube Multi-Search App - Enhanced
Main application entry point using modular architecture.
"""

import streamlit as st
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.search_service import YouTubeSearchService
from src.ui.components import UIComponents
from src.utils.config import Config


def main():
    """Main application function."""
    
    # Initialize UI
    UIComponents.render_header()
    
    # Initialize search service
    if 'search_service' not in st.session_state:
        st.session_state.search_service = YouTubeSearchService(Config.YOUTUBE_API_KEY)
    
    search_service = st.session_state.search_service
    
    # Check API key
    if not search_service.is_ready():
        if UIComponents.render_api_key_setup():
            # API key was set, reinitialize service
            api_key = st.session_state.get('youtube_api_key')
            if api_key:
                search_service.set_api_key(api_key)
                Config.save_api_key(api_key)
        return
    
    # Render search interface
    search_params = UIComponents.render_search_sidebar()
    
    # Main content area
    if not search_params['query']:
        st.info("👈 Enter a search query in the sidebar to get started")
        UIComponents.render_search_examples()
        return
    
    if not search_params['content_types']:
        st.error("Please select at least one content type to search for")
        return
    
    if not search_params['search_clicked']:
        # Check if we have previous search results to display
        if 'last_search_results' in st.session_state and 'last_search_params' in st.session_state:
            st.info("📋 Showing previous search results")
            display_results(st.session_state.last_search_results, st.session_state.last_search_params)
        else:
            st.info("👈 Click the 'Search' button to start searching")
        return
    
    # Perform search
    try:
        with st.spinner("🔍 Searching YouTube..."):
            st.info(f"🔧 Debug: Search params = {search_params}")
            results = search_service.search(search_params)
            st.info(f"🔧 Debug: Results count = Videos: {len(results.get('videos', []))}, Channels: {len(results.get('channels', []))}, Playlists: {len(results.get('playlists', []))}")
        
        # Store results in session state to persist across button clicks
        st.session_state.last_search_results = results
        st.session_state.last_search_params = search_params
        
        # Display results
        display_results(results, search_params)
        
    except Exception as e:
        st.error(f"❌ Search error: {str(e)}")


def display_results(results, search_params):
    """
    Display search results.
    
    Args:
        results (dict): Search results organized by content type
        search_params (dict): Original search parameters
    """
    total_results = len(results['videos']) + len(results['channels']) + len(results['playlists'])
    
    if total_results == 0:
        st.warning("No results found. Try adjusting your search query or filters.")
        return
    
    st.success(f"Found {total_results} results")
    
    # Display videos
    if results['videos']:
        st.header(f"📹 Videos ({len(results['videos'])})")
        for index, video_info in enumerate(results['videos']):
            UIComponents.display_video_result(video_info, index)
    
    # Display channels
    if results['channels']:
        st.header(f"📺 Channels ({len(results['channels'])})")
        for index, channel_info in enumerate(results['channels']):
            UIComponents.display_channel_result(channel_info, index)
    
    # Display playlists
    if results['playlists']:
        st.header(f"📂 Playlists ({len(results['playlists'])})")
        for index, playlist_info in enumerate(results['playlists']):
            UIComponents.display_playlist_result(playlist_info, index)
    
    # Render footer
    UIComponents.render_footer()


if __name__ == "__main__":
    main()