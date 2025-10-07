"""
Streamlit UI components for the YouTube Search App.
"""

import streamlit as st
from urllib.parse import urlparse, parse_qs
from streamlit_player import st_player


class UIComponents:
    """Streamlit UI components for the YouTube search application."""
    
    @staticmethod
    def render_header():
        """Render the application header."""
        st.set_page_config(
            page_title="YouTube Multi-Search App - Enhanced",
            page_icon="🎥",
            layout="wide"
        )
        
        st.title("🎥 YouTube Multi-Search App - Enhanced")
        st.markdown("""
        **🚀 Advanced YouTube Search with Enhanced Filtering**
        
        Search for videos, channels, and playlists with powerful filters including:
        - 📂 **Category Filtering** - Browse by content category
        - 🏷️ **Topic Categories** - Filter by specific topics using YouTube's Knowledge Graph
        - 👶 **Kids Content Filter** - Find family-friendly or adult content
        - ⏱️ **Duration & Quality** - Filter by video length and definition
        - 📅 **Date Range** - Find content from specific time periods
        """)
    
    @staticmethod
    def render_api_key_setup():
        """Render API key setup interface."""
        st.error("❌ YouTube API key not found or invalid!")
        
        with st.expander("🔑 Configure YouTube API Key", expanded=True):
            st.markdown("""
            ### How to get a YouTube API Key:
            
            1. **Go to Google Cloud Console**: https://console.cloud.google.com/
            2. **Create or select a project**
            3. **Enable YouTube Data API v3**:
               - Go to "APIs & Services" > "Library"
               - Search for "YouTube Data API v3"
               - Click "Enable"
            4. **Create credentials**:
               - Go to "APIs & Services" > "Credentials"
               - Click "Create Credentials" > "API Key"
               - Copy your API key
            
            ### Enter your API key below:
            """)
            
            user_api_key = st.text_input(
                "YouTube API Key:",
                type="password",
                placeholder="Paste your YouTube Data API v3 key here",
                help="Your API key will be stored in the session and not saved permanently"
            )
            
            if st.button("💾 Save API Key"):
                if user_api_key and len(user_api_key) > 10:
                    st.session_state.youtube_api_key = user_api_key
                    # Also update the config file
                    try:
                        config_content = f'''# YouTube API Configuration
YOUTUBE_API_KEY = "{user_api_key}"

# Configuration automatically updated by the app
'''
                        with open('config.py', 'w') as f:
                            f.write(config_content)
                        st.success("✅ API key saved! Please refresh the page to start searching.")
                        st.rerun()
                    except:
                        st.warning("⚠️ API key saved to session but couldn't update config file.")
                        st.rerun()
                else:
                    st.error("Please enter a valid API key")
        
        return False
    
    @staticmethod
    def render_search_sidebar():
        """
        Render the search parameters sidebar.
        
        Returns:
            dict: Search parameters
        """
        with st.sidebar:
            st.header("🔍 Search Parameters")
            
            # Basic search parameters
            search_query = st.text_input(
                "Search Query:",
                placeholder="Enter your search terms...",
                help="Enter keywords to search for YouTube content"
            )
            
            content_types = st.multiselect(
                "Content Types:",
                options=["video", "channel", "playlist"],
                default=["video"],
                help="Select the types of content to search for"
            )
            
            max_results = st.slider(
                "Max Results per Type:",
                min_value=1,
                max_value=50,
                value=10,
                help="Maximum number of results to return for each content type"
            )
            
            # Advanced filters
            st.subheader("🔧 Advanced Filters")
            
            order = st.selectbox(
                "Sort Order:",
                options=["relevance", "date", "rating", "viewCount", "title"],
                format_func=lambda x: {
                    "relevance": "Relevance",
                    "date": "Upload date", 
                    "rating": "Rating",
                    "viewCount": "View count",
                    "title": "Title"
                }[x],
                help="How to sort the search results"
            )
            
            safe_search = st.selectbox(
                "Safe Search:",
                options=["moderate", "strict", "none"],
                format_func=lambda x: {
                    "moderate": "Moderate",
                    "strict": "Strict", 
                    "none": "None"
                }[x],
                help="Filter inappropriate content"
            )
            
            # Video-specific filters
            if "video" in content_types:
                st.subheader("🎬 Video Filters")
                
                from src.core.data_processor import FilterManager
                
                # Category filter
                category_options = ["ALL"] + list(FilterManager.CATEGORIES.keys())
                selected_categories = st.multiselect(
                    "Categories:",
                    options=category_options,
                    format_func=lambda x: "Any Category" if x == "ALL" else FilterManager.CATEGORIES.get(x, x),
                    help="Filter by YouTube video categories (select multiple, or 'Any Category' for no filter)"
                )
                
                # Topic filter
                topic_options = [""] + list(FilterManager.TOPICS.keys())
                selected_topic = st.selectbox(
                    "Topic:",
                    options=topic_options,
                    format_func=lambda x: FilterManager.TOPICS.get(x, "Any Topic") if x else "Any Topic",
                    help="Filter by specific topic using YouTube's Knowledge Graph"
                )
                
                # Duration filter
                duration = st.selectbox(
                    "Duration:",
                    options=["any", "short", "medium", "long"],
                    format_func=lambda x: FilterManager.DURATIONS[x],
                    help="Filter by video duration"
                )
                
                # Quality filter
                definition = st.selectbox(
                    "Video Quality:",
                    options=["any", "high", "standard"],
                    format_func=lambda x: FilterManager.DEFINITIONS[x],
                    help="Filter by video definition quality"
                )
                
                # Kids content filter
                kids_filter = st.selectbox(
                    "Kids Content:",
                    options=["any", "yes", "no"],
                    format_func=lambda x: {
                        "any": "Any Content",
                        "yes": "Kids Only",
                        "no": "Not for Kids"
                    }[x],
                    help="Filter content based on family-friendly status"
                )
                
                # Date range filter
                use_date_filter = st.checkbox("Filter by Date Range")
                published_after = None
                published_before = None
                
                if use_date_filter:
                    col1, col2 = st.columns(2)
                    with col1:
                        published_after = st.date_input("Published After:")
                    with col2:
                        published_before = st.date_input("Published Before:")
            
            else:
                selected_categories = []
                selected_topic = ""
                duration = "any"
                definition = "any"
                kids_filter = "any"
                published_after = None
                published_before = None
            
            # Search button
            search_clicked = st.button("🔍 Search", type="primary", use_container_width=True)
        
        return {
            'query': search_query,
            'content_types': content_types,
            'max_results': max_results,
            'order': order,
            'safe_search': safe_search,
            'category_id': [cat for cat in selected_categories if cat != "ALL"] if selected_categories and "ALL" not in selected_categories else None,
            'topic_id': selected_topic if selected_topic else None,
            'video_duration': duration if duration != "any" else None,
            'video_definition': definition if definition != "any" else None,
            'kids_filter': kids_filter,
            'published_after': published_after,
            'published_before': published_before,
            'search_clicked': search_clicked
        }
    
    @staticmethod
    def display_video_result(info, index):
        """
        Display a single video search result.
        
        Args:
            info (dict): Formatted video information
            index (int): Result index for unique keys
        """
        # Debug info at the top
        st.write(f"🔧 **DEBUG**: Displaying video {index} - ID: {info.get('id', 'unknown')}")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Thumbnail
            if info.get('thumbnail_url'):
                st.image(info['thumbnail_url'], use_container_width=True)
            
            # Video stats
            if 'view_count' in info:
                from src.core.data_processor import YouTubeDataFormatter
                st.write(f"👀 **Views:** {YouTubeDataFormatter.format_count(info['view_count'])}")
            
            if 'duration_readable' in info:
                st.write(f"⏱️ **Duration:** {info['duration_readable']}")
            
            if 'like_count' in info:
                from src.core.data_processor import YouTubeDataFormatter
                st.write(f"👍 **Likes:** {YouTubeDataFormatter.format_count(info['like_count'])}")
            
            # Simple test button with persistent feedback
            test_key = f"test_button_{index}"
            test_result_key = f"test_result_{index}"
            
            if st.button(f"🧪 Test Button {index}", key=test_key):
                st.balloons()
                st.session_state[test_result_key] = f"✅ Button {index} clicked successfully!"
            
            # Show persistent test result
            if test_result_key in st.session_state:
                st.success(st.session_state[test_result_key])
            
            # Video player control with explicit state management
            player_key = f"show_player_{index}"
            
            # Initialize state if not exists
            if player_key not in st.session_state:
                st.session_state[player_key] = False
            
            current_state = st.session_state[player_key]
            
            # Debug information
            st.caption(f"🔧 Debug: {player_key} = {current_state}")
            
            # Use proper buttons for video player control
            if current_state:
                # Show "Hide Video" button when player is visible
                if st.button("❌ Hide Video", key=f"hide_{index}_{info['id']}", use_container_width=True):
                    st.session_state[player_key] = False
                    # Force a minimal rerun to update UI but preserve search results
                    st.rerun()
            else:
                # Show "Play Video" button when player is hidden
                if st.button("▶️ Play Video", key=f"play_{index}_{info['id']}", use_container_width=True):
                    st.session_state[player_key] = True
                    # Force a minimal rerun to update UI but preserve search results
                    st.rerun()
        
        with col2:
            # Video information
            st.markdown(f"### {index + 1}. {info['title']}")
            st.write(f"**Channel:** {info['channel_title']}")
            
            # Debug: Show all available info keys
            st.caption(f"🔧 Debug: Available data keys: {list(info.keys())}")
            
            # Category information (now from search API)
            if info.get('category_name'):
                st.write(f"**📂 Category:** {info['category_name']}")
            elif info.get('category_id'):
                st.write(f"**� Category:** Category {info['category_id']}")
            else:
                st.caption("📂 Category: Not specified")
            
            # Topic information (prioritize relevantTopicIds)
            topics_to_show = []
            
            # Add relevant topic IDs (current YouTube API) if available
            if info.get('relevant_topic_names') and len(info['relevant_topic_names']) > 0:
                topics_to_show.extend(info['relevant_topic_names'])
                st.caption(f"🔧 Debug: Found {len(info['relevant_topic_names'])} relevantTopicIds")
            
            # Add legacy topic categories if available and no relevant topics
            elif info.get('topic_categories_formatted') and len(info['topic_categories_formatted']) > 0:
                topics_to_show.extend(info['topic_categories_formatted'])
                st.caption(f"🔧 Debug: Using {len(info['topic_categories_formatted'])} legacy topic categories")
            
            # Add inferred topics as fallback
            if info.get('inferred_topics') and len(info['inferred_topics']) > 0:
                for topic in info['inferred_topics']:
                    if topic not in topics_to_show:  # Avoid duplicates
                        topics_to_show.append(f"{topic} (inferred)")
            
            if topics_to_show:
                topics_display = ', '.join(topics_to_show[:5])  # Show first 5 topics
                if len(topics_to_show) > 5:
                    topics_display += f" (+{len(topics_to_show) - 5} more)"
                st.write(f"**🏷️ Topics:** {topics_display}")
                
                # Show ALL topics for discovery
                if len(topics_to_show) > 1:
                    with st.expander(f"🏷️ All Topics ({len(topics_to_show)})"):
                        for i, topic in enumerate(topics_to_show, 1):
                            st.write(f"{i}. {topic}")
                        
                        # Show raw topic IDs for debugging
                        if info.get('topic_ids'):
                            st.caption(f"🔧 Raw relevantTopicIds: {info['topic_ids']}")
            else:
                st.caption("🏷️ Topics: Limited metadata available")
                st.caption(f"🔧 Debug: No topic data found")
            
            if 'published_at' in info:
                from src.core.data_processor import YouTubeDataFormatter
                formatted_date = YouTubeDataFormatter.format_published_date(info['published_at'])
                st.write(f"**Published:** {formatted_date}")
            
            # Description (truncated)
            description = info.get('description', '')
            if len(description) > 200:
                description = description[:200] + "..."
            st.write(f"**Description:** {description}")
            
            # Links
            if info.get('url'):
                st.markdown(f"[🔗 Watch on YouTube]({info['url']})")
        
        # Video player display
        player_key = f"show_player_{index}"
        if st.session_state.get(player_key, False):
            st.markdown("---")
            st.markdown("### 🎥 Now Playing:")
            
            # Debug info
            st.caption(f"🔧 Debug: Player state = {st.session_state.get(player_key, 'Not set')}")
            
            try:
                # Create YouTube embed URL from regular URL
                video_url = info.get('url', '')
                st.caption(f"🔧 Debug: Original URL = {video_url}")
                
                if 'youtube.com/watch?v=' in video_url:
                    video_id = video_url.split('v=')[1].split('&')[0]
                    embed_url = f"https://www.youtube.com/embed/{video_id}"
                    st.caption(f"🔧 Debug: Video ID = {video_id}")
                    st.caption(f"🔧 Debug: Embed URL = {embed_url}")
                else:
                    embed_url = video_url
                    st.caption(f"🔧 Debug: Using original URL = {embed_url}")
                
                st.info("🎬 Loading video player...")
                st_player(embed_url, key=f"player_{index}", height=400)
                st.caption("💡 Click 'Hide Video' above to close")
                
            except Exception as e:
                st.error(f"Error loading video player: {str(e)}")
                st.markdown(f"[🔗 Watch on YouTube]({info['url']})")
                # Reset player state if there's an error
                st.session_state[player_key] = False
        
        st.markdown("---")
    
    @staticmethod
    def display_channel_result(info, index):
        """
        Display a single channel search result.
        
        Args:
            info (dict): Formatted channel information
            index (int): Result index for unique keys
        """
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Thumbnail
            if info.get('thumbnail_url'):
                st.image(info['thumbnail_url'], use_container_width=True)
            
            # Channel stats
            if 'subscriber_count' in info:
                from src.core.data_processor import YouTubeDataFormatter
                st.write(f"👥 **Subscribers:** {YouTubeDataFormatter.format_count(info['subscriber_count'])}")
            
            if 'video_count' in info:
                st.write(f"📹 **Videos:** {info['video_count']:,}")
            
            if 'view_count' in info:
                from src.core.data_processor import YouTubeDataFormatter
                st.write(f"👀 **Total Views:** {YouTubeDataFormatter.format_count(info['view_count'])}")
        
        with col2:
            # Channel information
            st.markdown(f"### {index + 1}. {info['title']}")
            
            if 'published_at' in info:
                from src.core.data_processor import YouTubeDataFormatter
                formatted_date = YouTubeDataFormatter.format_published_date(info['published_at'])
                st.write(f"**Created:** {formatted_date}")
            
            # Description (truncated)
            description = info.get('description', '')
            if len(description) > 200:
                description = description[:200] + "..."
            st.write(f"**Description:** {description}")
            
            # Links
            if info.get('url'):
                st.markdown(f"[🔗 Visit Channel]({info['url']})")
        
        st.markdown("---")
    
    @staticmethod
    def display_playlist_result(info, index):
        """
        Display a single playlist search result.
        
        Args:
            info (dict): Formatted playlist information
            index (int): Result index for unique keys
        """
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Thumbnail
            if info.get('thumbnail_url'):
                st.image(info['thumbnail_url'], use_container_width=True)
            
            # Playlist stats
            if 'item_count' in info:
                st.write(f"📹 **Videos:** {info['item_count']}")
        
        with col2:
            # Playlist information
            st.markdown(f"### {index + 1}. {info['title']}")
            st.write(f"**Channel:** {info['channel_title']}")
            
            if 'published_at' in info:
                from src.core.data_processor import YouTubeDataFormatter
                formatted_date = YouTubeDataFormatter.format_published_date(info['published_at'])
                st.write(f"**Created:** {formatted_date}")
            
            # Description (truncated)
            description = info.get('description', '')
            if len(description) > 200:
                description = description[:200] + "..."
            st.write(f"**Description:** {description}")
            
            # Links
            if info.get('url'):
                st.markdown(f"[🔗 View Playlist]({info['url']})")
        
        st.markdown("---")
    
    @staticmethod
    def render_search_examples():
        """Render search examples section."""
        with st.expander("💡 Search Examples & Tips"):
            st.markdown("""
            ### 🎯 Search Examples:
            """)
            
            example_col1, example_col2 = st.columns(2)
            
            with example_col1:
                st.markdown("""
                **📚 Educational Content:**
                - Search: "python programming tutorial"
                - Category: "Education"
                - Duration: "long"
                - Safe Search: "strict"
                """)
                
                st.markdown("""
                **👶 Kids Content:**
                - Search: "learning songs"
                - Category: "Education"
                - Kids Filter: "Kids Only"
                - Safe Search: "strict"
                """)
            
            with example_col2:
                st.markdown("""
                **🎵 Music Discovery:**
                - Search: "classical music"
                - Category: "Music"
                - Topic: "Classical music"
                - Duration: "medium"
                """)
                
                st.markdown("""
                **🎮 Gaming Content:**
                - Search: "minecraft gameplay"
                - Category: "Gaming"
                - Topic: "Gaming"
                - Kids Filter: "Any"
                """)
    
    @staticmethod
    def render_footer():
        """Render the application footer."""
        st.markdown("---")
        st.markdown("🚀 Enhanced YouTube Multi-Search App with Advanced Filtering")
        st.markdown("**✨ Features:** Category Filtering | Topic Categories | Kids Content Filter | Enhanced Metadata")