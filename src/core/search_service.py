"""
Search service that coordinates between API client and data processing.
"""

from src.core.youtube_api import YouTubeAPIClient
from src.core.data_processor import YouTubeDataFormatter, FilterManager


class YouTubeSearchService:
    """High-level search service that coordinates all components."""
    
    def __init__(self, api_key=None):
        self.api_client = YouTubeAPIClient(api_key)
        self.formatter = YouTubeDataFormatter()
        self.filter_manager = FilterManager()
    
    def set_api_key(self, api_key):
        """Set API key for the service."""
        return self.api_client.set_api_key(api_key)
    
    def is_ready(self):
        """Check if the service is ready to use."""
        return self.api_client.is_ready()
    
    def search(self, search_params):
        """
        Perform a comprehensive search with filtering and formatting.
        
        Args:
            search_params (dict): Search parameters
            
        Returns:
            dict: Search results organized by content type
        """
        if not self.is_ready():
            raise Exception("YouTube API not initialized")
        
        results = {
            'videos': [],
            'channels': [],
            'playlists': []
        }
        
        content_types = search_params.get('content_types', ['video'])
        
        for content_type in content_types:
            # Handle multiple categories by performing separate searches
            category_ids = search_params.get('category_id')
            
            if category_ids and isinstance(category_ids, list) and len(category_ids) > 0:
                # Multiple categories - search each separately and combine results
                all_formatted_results = []
                
                for category_id in category_ids:
                    # Adjust search parameters for content type and single category
                    type_params = search_params.copy()
                    type_params['content_type'] = content_type
                    type_params['category_id'] = category_id
                    
                    try:
                        # Get raw search results for this category
                        print(f"Debug: Searching for {content_type} in category {category_id}")
                        raw_results = self.api_client.search_content(type_params)
                        print(f"Debug: Got {len(raw_results)} raw results for {content_type} in category {category_id}")
                        
                        # Process and format results
                        formatted_results = self._process_results(
                            raw_results, 
                            content_type, 
                            search_params
                        )
                        all_formatted_results.extend(formatted_results)
                        
                    except Exception as e:
                        print(f"Error searching {content_type}s in category {category_id}: {e}")
                        continue
                
                # Remove duplicates based on video ID and limit results
                seen_ids = set()
                unique_results = []
                max_results = search_params.get('max_results', 10)
                
                for result in all_formatted_results:
                    result_id = result.get('video_id') or result.get('channel_id') or result.get('playlist_id')
                    if result_id not in seen_ids:
                        seen_ids.add(result_id)
                        unique_results.append(result)
                        if len(unique_results) >= max_results:
                            break
                
                formatted_results = unique_results
                
            else:
                # Single category or no category - original logic
                type_params = search_params.copy()
                type_params['content_type'] = content_type
                
                try:
                    # Get raw search results
                    print(f"Debug: Searching for {content_type} with params: {type_params}")
                    raw_results = self.api_client.search_content(type_params)
                    print(f"Debug: Got {len(raw_results)} raw results for {content_type}")
                    
                    # Process and format results
                    formatted_results = self._process_results(
                        raw_results, 
                        content_type, 
                        search_params
                    )
                    print(f"Debug: Formatted {len(formatted_results)} results for {content_type}")
                    
                except Exception as e:
                    print(f"Error searching {content_type}s: {e}")
                    continue
            
            # Store results by type
            if content_type == 'video':
                results['videos'] = formatted_results
            elif content_type == 'channel':
                results['channels'] = formatted_results
            elif content_type == 'playlist':
                results['playlists'] = formatted_results
        
        return results
    
    def _process_results(self, raw_results, content_type, search_params):
        """
        Process and format raw search results.
        
        Args:
            raw_results (list): Raw API results
            content_type (str): Type of content
            search_params (dict): Original search parameters
            
        Returns:
            list: Processed and formatted results
        """
        formatted_results = []
        
        if content_type == 'video':
            # Batch video details requests for efficiency
            video_ids = []
            for item in raw_results:
                video_id = item.get('id', {}).get('videoId')
                if video_id:
                    video_ids.append(video_id)
            
            # Get all video details in one request
            video_details_dict = {}
            if video_ids:
                try:
                    video_details_list = self.api_client.get_video_details(video_ids)
                    # Create a lookup dictionary
                    for details in video_details_list:
                        video_id = details.get('id')
                        if video_id:
                            video_details_dict[video_id] = details
                except Exception as e:
                    print(f"Error getting video details: {e}")
            
            # Process each video with its details
            for item in raw_results:
                try:
                    video_id = item.get('id', {}).get('videoId')
                    video_details = video_details_dict.get(video_id) if video_id else None
                    
                    formatted_info = self.formatter.format_video_info(item, video_details)
                    
                    # Apply post-processing filters
                    if self._should_include_video(formatted_info, search_params):
                        formatted_results.append(formatted_info)
                        
                except Exception as e:
                    print(f"Error processing video result: {e}")
                    continue
        
        else:
            # Handle channels and playlists individually (less critical for batching)
            for item in raw_results:
                try:
                    if content_type == 'channel':
                        # Get detailed channel information
                        channel_id = item.get('id', {}).get('channelId')
                        if channel_id:
                            channel_details = self.api_client.get_channel_details([channel_id])
                            formatted_info = self.formatter.format_channel_info(
                                item,
                                channel_details[0] if channel_details else None
                            )
                        else:
                            formatted_info = self.formatter.format_channel_info(item)
                            
                    elif content_type == 'playlist':
                        # Get detailed playlist information
                        playlist_id = item.get('id', {}).get('playlistId')
                        if playlist_id:
                            playlist_details = self.api_client.get_playlist_details([playlist_id])
                            formatted_info = self.formatter.format_playlist_info(
                                item,
                                playlist_details[0] if playlist_details else None
                            )
                        else:
                            formatted_info = self.formatter.format_playlist_info(item)
                    
                    formatted_results.append(formatted_info)
                    
                except Exception as e:
                    print(f"Error processing {content_type} result: {e}")
                    continue
        
        return formatted_results
    
    def _should_include_video(self, formatted_info, search_params):
        """
        Check if a video should be included based on filters.
        
        Args:
            formatted_info (dict): Formatted video information
            search_params (dict): Search parameters with filters
            
        Returns:
            bool: True if video should be included
        """
        # Topic filter (check both relevantTopicIds and legacy topicIds)
        topic_id = search_params.get('topic_id')
        if topic_id:
            video_topic_ids = formatted_info.get('topic_ids', [])
            if video_topic_ids and topic_id not in video_topic_ids:
                return False
        
        # Kids content filter
        kids_filter = search_params.get('kids_filter')
        if kids_filter != 'any' and 'made_for_kids' in formatted_info:
            target_kids_status = kids_filter == 'yes'
            if formatted_info['made_for_kids'] != target_kids_status:
                return False
        
        return True