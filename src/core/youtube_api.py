"""
YouTube API core functionality for the YouTube Search App.
This module handles all YouTube Data API v3 interactions.
"""

import os
import sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class YouTubeAPIClient:
    """YouTube API client for handling all API interactions."""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.youtube = None
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize YouTube API service with error handling."""
        if not self.api_key:
            self.api_key = self._get_api_key()
        
        if self.api_key:
            try:
                self.youtube = build('youtube', 'v3', developerKey=self.api_key)
                return True
            except Exception as e:
                print(f"Error initializing YouTube API: {str(e)}")
                return False
        return False
    
    def _get_api_key(self):
        """Get API key from multiple sources."""
        # Method 1: Environment variable
        api_key = os.getenv('YOUTUBE_API_KEY')
        if api_key:
            return api_key
        
        # Method 2: Try to import from local config
        try:
            sys.path.append(os.getcwd())
            from config import YOUTUBE_API_KEY
            if YOUTUBE_API_KEY and YOUTUBE_API_KEY != "YOUR_API_KEY_HERE":
                return YOUTUBE_API_KEY
        except ImportError:
            pass
        
        return None
    
    def set_api_key(self, api_key):
        """Set new API key and reinitialize service."""
        self.api_key = api_key
        return self._initialize_service()
    
    def is_ready(self):
        """Check if API client is ready to use."""
        return self.youtube is not None
    
    def search_content(self, search_params):
        """
        Search YouTube content with enhanced parameters.
        
        Args:
            search_params (dict): Search parameters including query, content_type, etc.
            
        Returns:
            list: List of search results
        """
        if not self.is_ready():
            raise Exception("YouTube API client not initialized")
        
        try:
            # Build search request
            search_request = self.youtube.search().list(
                part="snippet",
                q=search_params.get('query', ''),
                type=search_params.get('content_type', 'video'),
                maxResults=search_params.get('max_results', 10),
                order=search_params.get('order', 'relevance'),
                safeSearch=search_params.get('safe_search', 'moderate'),
                videoDuration=search_params.get('video_duration'),
                videoDefinition=search_params.get('video_definition'),
                videoCategoryId=search_params.get('category_id'),
                publishedAfter=search_params.get('published_after'),
                publishedBefore=search_params.get('published_before'),
                regionCode=search_params.get('region_code'),
                relevanceLanguage=search_params.get('language')
            )
            
            # Remove None values
            search_request.uri = self._clean_uri(search_request.uri)
            
            response = search_request.execute()
            return response.get('items', [])
            
        except HttpError as e:
            raise Exception(f"YouTube API error: {e}")
        except Exception as e:
            raise Exception(f"Search error: {e}")
    
    def get_video_details(self, video_ids):
        """
        Get detailed information for videos.
        
        Args:
            video_ids (list): List of video IDs
            
        Returns:
            list: List of video details
        """
        if not self.is_ready():
            raise Exception("YouTube API client not initialized")
        
        try:
            if isinstance(video_ids, str):
                video_ids = [video_ids]
            
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics,status,topicDetails",
                id=",".join(video_ids)
            )
            
            response = request.execute()
            items = response.get('items', [])
            
            # Debug: Print what we're actually getting
            for item in items:
                video_id = item.get('id', 'unknown')
                snippet = item.get('snippet', {})
                topic_details = item.get('topicDetails', {})
                print(f"Debug API Response for {video_id}:")
                print(f"  - categoryId: {snippet.get('categoryId', 'None')}")
                print(f"  - topicDetails keys: {list(topic_details.keys())}")
                print(f"  - relevantTopicIds: {topic_details.get('relevantTopicIds', [])}")
                print(f"  - topicCategories: {topic_details.get('topicCategories', [])}")
                print(f"  - (deprecated) topicIds: {topic_details.get('topicIds', [])}")
            
            return items
            
        except HttpError as e:
            raise Exception(f"YouTube API error: {e}")
        except Exception as e:
            raise Exception(f"Video details error: {e}")
    
    def get_channel_details(self, channel_ids):
        """
        Get detailed information for channels.
        
        Args:
            channel_ids (list): List of channel IDs
            
        Returns:
            list: List of channel details
        """
        if not self.is_ready():
            raise Exception("YouTube API client not initialized")
        
        try:
            if isinstance(channel_ids, str):
                channel_ids = [channel_ids]
            
            request = self.youtube.channels().list(
                part="snippet,statistics,brandingSettings",
                id=",".join(channel_ids)
            )
            
            response = request.execute()
            return response.get('items', [])
            
        except HttpError as e:
            raise Exception(f"YouTube API error: {e}")
        except Exception as e:
            raise Exception(f"Channel details error: {e}")
    
    def get_playlist_details(self, playlist_ids):
        """
        Get detailed information for playlists.
        
        Args:
            playlist_ids (list): List of playlist IDs
            
        Returns:
            list: List of playlist details
        """
        if not self.is_ready():
            raise Exception("YouTube API client not initialized")
        
        try:
            if isinstance(playlist_ids, str):
                playlist_ids = [playlist_ids]
            
            request = self.youtube.playlists().list(
                part="snippet,contentDetails,status",
                id=",".join(playlist_ids)
            )
            
            response = request.execute()
            return response.get('items', [])
            
        except HttpError as e:
            raise Exception(f"YouTube API error: {e}")
        except Exception as e:
            raise Exception(f"Playlist details error: {e}")
    
    def _clean_uri(self, uri):
        """Remove parameters with None values from URI."""
        # This is a simplified implementation
        # In a real implementation, you'd properly parse and clean the URI
        return uri