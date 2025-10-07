"""
Data formatting and processing utilities for YouTube search results.
"""

from datetime import datetime
import re


class YouTubeDataFormatter:
    """Handles formatting and processing of YouTube API responses."""
    
    @staticmethod
    def format_video_info(item, video_details=None):
        """
        Format video information from YouTube API response.
        
        Args:
            item (dict): YouTube search result item
            video_details (dict): Optional detailed video information
            
        Returns:
            dict: Formatted video information
        """
        snippet = item.get('snippet', {})
        video_id = item.get('id', {}).get('videoId', '')
        
        info = {
            'type': 'video',
            'id': video_id,
            'title': snippet.get('title', 'No title'),
            'description': snippet.get('description', 'No description'),
            'channel_title': snippet.get('channelTitle', 'Unknown Channel'),
            'channel_id': snippet.get('channelId', ''),
            'published_at': snippet.get('publishedAt', ''),
            'thumbnail_url': snippet.get('thumbnails', {}).get('medium', {}).get('url', ''),
            'url': f"https://www.youtube.com/watch?v={video_id}" if video_id else ""
        }
        
        # Extract category information from search API snippet (more reliable)
        search_category_id = snippet.get('categoryId', '')
        if search_category_id:
            info['category_id'] = search_category_id
            info['category_name'] = YouTubeDataFormatter._get_category_name(search_category_id)
        else:
            info['category_id'] = ''
            info['category_name'] = ''
        
        # Initialize topic information (will be enhanced if detailed data available)
        info['topic_ids'] = []
        info['topic_categories'] = []
        info['topic_categories_formatted'] = []
        info['relevant_topic_names'] = []
        
        # Add basic topic inference from category (as fallback)
        if info.get('category_name'):
            info['inferred_topics'] = [info['category_name']]
        else:
            info['inferred_topics'] = []
        
        # Add detailed information if available
        if video_details:
            details = video_details[0] if isinstance(video_details, list) else video_details
            
            # Video category (only update if we don't have it from search)
            try:
                if not info.get('category_id'):  # Only if not already set from search
                    snippet_details = details.get('snippet', {})
                    detail_category_id = snippet_details.get('categoryId', '')
                    if detail_category_id:
                        info['category_id'] = detail_category_id
                        info['category_name'] = YouTubeDataFormatter._get_category_name(detail_category_id)
                print(f"Debug: Video {info.get('id', 'unknown')} - Final category_id: {info['category_id']}, category_name: {info['category_name']}")
            except Exception as e:
                print(f"Debug: Error processing category: {e}")
            
            # Content details
            content_details = details.get('contentDetails', {})
            info['duration'] = content_details.get('duration', '')
            info['duration_readable'] = YouTubeDataFormatter._parse_duration(info['duration'])
            
            # Statistics
            statistics = details.get('statistics', {})
            info['view_count'] = int(statistics.get('viewCount', 0))
            info['like_count'] = int(statistics.get('likeCount', 0))
            info['comment_count'] = int(statistics.get('commentCount', 0))
            
            # Status
            status = details.get('status', {})
            info['made_for_kids'] = status.get('madeForKids', False)
            info['privacy_status'] = status.get('privacyStatus', 'unknown')
            
            # Topic details (updated to use relevantTopicIds)
            try:
                topic_details = details.get('topicDetails', {})
                # Use relevantTopicIds (current) instead of deprecated topicIds
                info['topic_ids'] = topic_details.get('relevantTopicIds', [])
                info['topic_categories'] = topic_details.get('topicCategories', [])
                info['topic_categories_formatted'] = YouTubeDataFormatter._format_topic_categories(info['topic_categories'])
                
                # Also format the relevantTopicIds for display
                info['relevant_topic_names'] = YouTubeDataFormatter._format_relevant_topic_ids(info['topic_ids'])
                
                print(f"Debug: Video {info.get('id', 'unknown')} - relevantTopicIds: {len(info['topic_ids'])}, topic_categories: {len(info['topic_categories'])}")
                print(f"Debug: Raw topic details: {topic_details}")
                print(f"Debug: Relevant topic names: {info['relevant_topic_names']}")
            except Exception as e:
                print(f"Debug: Error processing topics: {e}")
                info['topic_ids'] = []
                info['topic_categories'] = []
                info['topic_categories_formatted'] = []
                info['relevant_topic_names'] = []
        
        return info
    
    @staticmethod
    def format_channel_info(item, channel_details=None):
        """
        Format channel information from YouTube API response.
        
        Args:
            item (dict): YouTube search result item
            channel_details (dict): Optional detailed channel information
            
        Returns:
            dict: Formatted channel information
        """
        snippet = item.get('snippet', {})
        channel_id = item.get('id', {}).get('channelId', '')
        
        info = {
            'type': 'channel',
            'id': channel_id,
            'title': snippet.get('title', 'No title'),
            'description': snippet.get('description', 'No description'),
            'published_at': snippet.get('publishedAt', ''),
            'thumbnail_url': snippet.get('thumbnails', {}).get('medium', {}).get('url', ''),
            'url': f"https://www.youtube.com/channel/{channel_id}" if channel_id else ""
        }
        
        # Add detailed information if available
        if channel_details:
            details = channel_details[0] if isinstance(channel_details, list) else channel_details
            
            # Statistics
            statistics = details.get('statistics', {})
            info['subscriber_count'] = int(statistics.get('subscriberCount', 0))
            info['video_count'] = int(statistics.get('videoCount', 0))
            info['view_count'] = int(statistics.get('viewCount', 0))
            
            # Branding
            branding = details.get('brandingSettings', {})
            info['keywords'] = branding.get('channel', {}).get('keywords', '')
        
        return info
    
    @staticmethod
    def format_playlist_info(item, playlist_details=None):
        """
        Format playlist information from YouTube API response.
        
        Args:
            item (dict): YouTube search result item
            playlist_details (dict): Optional detailed playlist information
            
        Returns:
            dict: Formatted playlist information
        """
        snippet = item.get('snippet', {})
        playlist_id = item.get('id', {}).get('playlistId', '')
        
        info = {
            'type': 'playlist',
            'id': playlist_id,
            'title': snippet.get('title', 'No title'),
            'description': snippet.get('description', 'No description'),
            'channel_title': snippet.get('channelTitle', 'Unknown Channel'),
            'channel_id': snippet.get('channelId', ''),
            'published_at': snippet.get('publishedAt', ''),
            'thumbnail_url': snippet.get('thumbnails', {}).get('medium', {}).get('url', ''),
            'url': f"https://www.youtube.com/playlist?list={playlist_id}" if playlist_id else ""
        }
        
        # Add detailed information if available
        if playlist_details:
            details = playlist_details[0] if isinstance(playlist_details, list) else playlist_details
            
            # Content details
            content_details = details.get('contentDetails', {})
            info['item_count'] = content_details.get('itemCount', 0)
            
            # Status
            status = details.get('status', {})
            info['privacy_status'] = status.get('privacyStatus', 'unknown')
        
        return info
    
    @staticmethod
    def _parse_duration(duration_string):
        """
        Parse YouTube duration string (PT4M13S) to readable format.
        
        Args:
            duration_string (str): ISO 8601 duration string
            
        Returns:
            str: Human readable duration
        """
        if not duration_string:
            return "Unknown"
        
        # Remove PT prefix
        duration_string = duration_string.replace('PT', '')
        
        # Extract hours, minutes, seconds
        hours = 0
        minutes = 0
        seconds = 0
        
        # Hours
        if 'H' in duration_string:
            hours_match = re.search(r'(\d+)H', duration_string)
            if hours_match:
                hours = int(hours_match.group(1))
        
        # Minutes
        if 'M' in duration_string:
            minutes_match = re.search(r'(\d+)M', duration_string)
            if minutes_match:
                minutes = int(minutes_match.group(1))
        
        # Seconds
        if 'S' in duration_string:
            seconds_match = re.search(r'(\d+)S', duration_string)
            if seconds_match:
                seconds = int(seconds_match.group(1))
        
        # Format as readable string
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    @staticmethod
    def format_count(count):
        """
        Format large numbers in a readable format.
        
        Args:
            count (int): Number to format
            
        Returns:
            str: Formatted number string
        """
        if count >= 1_000_000_000:
            return f"{count / 1_000_000_000:.1f}B"
        elif count >= 1_000_000:
            return f"{count / 1_000_000:.1f}M"
        elif count >= 1_000:
            return f"{count / 1_000:.1f}K"
        else:
            return str(count)
    
    @staticmethod
    def format_published_date(published_at):
        """
        Format published date to readable format.
        
        Args:
            published_at (str): ISO 8601 date string
            
        Returns:
            str: Formatted date string
        """
        try:
            # Parse ISO 8601 date
            date_obj = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            return date_obj.strftime('%B %d, %Y')
        except:
            return published_at[:10] if published_at else "Unknown"


class FilterManager:
    """Manages YouTube search filters and categories."""
    
    # YouTube video categories
    CATEGORIES = {
        "1": "Film & Animation",
        "2": "Autos & Vehicles", 
        "10": "Music",
        "15": "Pets & Animals",
        "17": "Sports",
        "18": "Short Movies",
        "19": "Travel & Events",
        "20": "Gaming",
        "21": "Videoblogging",
        "22": "People & Blogs",
        "23": "Comedy",
        "24": "Entertainment",
        "25": "News & Politics",
        "26": "Howto & Style",
        "27": "Education",
        "28": "Science & Technology",
        "29": "Nonprofits & Activism",
        "30": "Movies",
        "31": "Anime/Animation",
        "32": "Action/Adventure",
        "33": "Classics",
        "34": "Documentary",
        "35": "Drama",
        "36": "Family",
        "37": "Foreign",
        "38": "Horror",
        "39": "Sci-Fi/Fantasy",
        "40": "Thriller",
        "41": "Shorts",
        "42": "Shows",
        "43": "Trailers"
    }

    
    
    # YouTube topic categories (Knowledge Graph topic IDs)
    TOPICS = {
        "/m/04rlf": "Music",
        "/m/02mscn": "Christian music",
        "/m/0ggq0m": "Classical music", 
        "/m/01lyv": "Country music",
        "/m/02lkt": "Electronic music",
        "/m/0glt670": "Hip hop music",
        "/m/05rwpb": "Independent music",
        "/m/03_d0": "Jazz",
        "/m/028sqc": "Music of Asia",
        "/m/0g293": "Music of Latin America",
        "/m/064t9": "Pop music",
        "/m/06cqb": "Reggae",
        "/m/06j6l": "Rhythm and blues",
        "/m/06by7": "Rock music",
        "/m/0gywn": "Soul music",
        "/m/0bzvm2": "Gaming",
        "/m/025zzc": "Action game",
        "/m/02ntfj": "Adventure game",
        "/m/0b1vjn": "Casual game",
        "/m/02hygl": "Music video game",
        "/m/04q1x3q": "Puzzle video game",
        "/m/01sjng": "Racing video game",
        "/m/0403l3g": "Role-playing video game",
        "/m/021bp2": "Simulation video game",
        "/m/022dc6": "Sports game",
        "/m/03hf_rm": "Strategy video game",
        "/m/06ntj": "Sports",
        "/m/0jm_": "American football",
        "/m/018jz": "Baseball",
        "/m/018w8": "Basketball",
        "/m/01cgz": "Boxing",
        "/m/09xp_": "Cricket",
        "/m/02vx4": "Football",
        "/m/037hz": "Golf",
        "/m/03tmr": "Ice hockey",
        "/m/01h7lh": "Mixed martial arts",
        "/m/0410tth": "Motorsport",
        "/m/07bs0": "Tennis",
        "/m/07_53": "Volleyball",
        "/m/02jjt": "Entertainment",
        "/m/09kqc": "Humor",
        "/m/02vxn": "Movies",
        "/m/05qjc": "Performing arts",
        "/m/066wd": "Professional wrestling",
        "/m/0f2f9": "TV shows",
        "/m/019_rr": "Lifestyle",
        "/m/032tl": "Fashion",
        "/m/027x7n": "Fitness",
        "/m/02wbm": "Food",
        "/m/03glg": "Hobby",
        "/m/068hy": "Pets",
        "/m/041xxh": "Physical attractiveness",
        "/m/07c1v": "Technology",
        "/m/07bxq": "Tourism",
        "/m/07yv9": "Vehicles",
        "/m/01k8wb": "Knowledge"
    }
    
    # Search order options
    ORDERS = {
        "relevance": "Relevance",
        "date": "Upload date", 
        "rating": "Rating",
        "viewCount": "View count",
        "title": "Title"
    }
    
    # Safe search options
    SAFE_SEARCH = {
        "moderate": "Moderate",
        "strict": "Strict", 
        "none": "None"
    }
    
    # Video duration options
    DURATIONS = {
        "any": "Any duration",
        "short": "Short (< 4 minutes)",
        "medium": "Medium (4-20 minutes)", 
        "long": "Long (> 20 minutes)"
    }
    
    # Video definition options
    DEFINITIONS = {
        "any": "Any quality",
        "high": "High Definition",
        "standard": "Standard Definition"
    }
    
    @classmethod
    def get_all_categories(cls):
        """Get all available categories."""
        return cls.CATEGORIES
    
    @classmethod
    def get_all_topics(cls):
        """Get all available topics."""
        return cls.TOPICS
    
    @classmethod
    def get_category_name(cls, category_id):
        """Get category name by ID."""
        return cls.CATEGORIES.get(category_id, "Unknown Category")
    
    @classmethod
    def get_topic_name(cls, topic_id):
        """Get topic name by ID."""
        return cls.TOPICS.get(topic_id, "Unknown Topic")
    
    @classmethod
    def filter_by_topic(cls, results, topic_id):
        """Filter results by topic ID."""
        if not topic_id:
            return results
        
        filtered_results = []
        for result in results:
            topic_ids = result.get('topic_ids', [])
            if topic_id in topic_ids:
                filtered_results.append(result)
        
        return filtered_results
    
    @classmethod
    def filter_by_kids_content(cls, results, made_for_kids):
        """Filter results by kids content status."""
        if made_for_kids is None:
            return results
        
        filtered_results = []
        for result in results:
            if result.get('made_for_kids') == made_for_kids:
                filtered_results.append(result)
        
        return filtered_results
    
    @staticmethod
    def _get_category_name(category_id):
        """
        Map YouTube category ID to readable category name.
        
        Args:
            category_id (str): YouTube category ID
            
        Returns:
            str: Human-readable category name
        """
        # YouTube category mapping
        categories = {
            '1': 'Film & Animation',
            '2': 'Autos & Vehicles', 
            '10': 'Music',
            '15': 'Pets & Animals',
            '17': 'Sports',
            '18': 'Short Movies',
            '19': 'Travel & Events',
            '20': 'Gaming',
            '21': 'Videoblogging',
            '22': 'People & Blogs',
            '23': 'Comedy',
            '24': 'Entertainment',
            '25': 'News & Politics',
            '26': 'Howto & Style',
            '27': 'Education',
            '28': 'Science & Technology',
            '29': 'Nonprofits & Activism',
            '30': 'Movies',
            '31': 'Anime/Animation',
            '32': 'Action/Adventure',
            '33': 'Classics',
            '34': 'Comedy',
            '35': 'Documentary',
            '36': 'Drama',
            '37': 'Family',
            '38': 'Foreign',
            '39': 'Horror',
            '40': 'Sci-Fi/Fantasy',
            '41': 'Thriller',
            '42': 'Shorts',
            '43': 'Shows',
            '44': 'Trailers'
        }
        
        return categories.get(str(category_id), f'Category {category_id}')
    
    @staticmethod
    def _format_topic_categories(topic_categories):
        """
        Format topic categories for display.
        
        Args:
            topic_categories (list): List of topic category URLs
            
        Returns:
            list: List of formatted topic names
        """
        if not topic_categories:
            return []
        
        formatted_topics = []
        for topic_url in topic_categories:
            # Extract topic name from Wikipedia URL
            if 'wikipedia.org/wiki/' in topic_url:
                topic_name = topic_url.split('/')[-1].replace('_', ' ')
                formatted_topics.append(topic_name)
            else:
                formatted_topics.append(topic_url)
        
        return formatted_topics
    
    @staticmethod
    def _format_relevant_topic_ids(topic_ids):
        """
        Format relevantTopicIds into readable topic names.
        
        Args:
            topic_ids (list): List of topic IDs like ["/m/04rlf", "/m/0ggq0m"]
            
        Returns:
            list: List of formatted topic names
        """
        if not topic_ids:
            return []
        
        # Common YouTube topic ID mappings
        topic_mapping = {
            "/m/04rlf": "Music",
            "/m/0ggq0m": "Pop music", 
            "/m/064t9": "Rock music",
            "/m/0glt670": "Hip hop music",
            "/m/05rwpb": "Jazz",
            "/m/05pd6": "Blues",
            "/m/0342h": "Country music",
            "/m/02lkt": "Classical music",
            "/m/015lz1": "Song",
            "/m/0l14md": "Dance music",
            "/m/01lyv": "Electronic music",
            "/m/07gxw": "Rhythm and blues",
            "/m/06cqb": "Reggae",
            "/m/03_d0": "Folk music",
            "/m/02w4v": "Alternative rock",
            "/m/01k8wb": "Knowledge",
            "/m/019_rr": "Lifestyle",
            "/m/032tl": "Entertainment",
            "/m/098wr": "Sports",
            "/m/01h6rj": "Health",
            "/m/07c1v": "Technology",
            "/m/07bxq": "Tourism",
            "/m/06ntj": "Sports",
            "/m/02jjt": "Entertainment",
            "/m/05qt0": "Performing arts",
            "/m/07yv9": "Vehicle",
            "/m/02p0sh1": "Food",
            "/m/01h44": "Cuisine",
            "/m/02wbm": "Food",
            "/m/0kt51": "Health",
            "/m/01cgz": "Fitness",
            "/m/01h7lh": "Physical fitness",
            "/m/027x7n": "Cooking",
            "/m/02p1r": "Beauty",
            "/m/07c1v": "Technology",
            "/m/019_rr": "Lifestyle",
            "/m/098wr": "Sport",
            "/m/06ntj": "Sports",
            "/m/0jm_": "History",
            "/m/05qjt": "Politics",
            "/m/09s1f": "Business",
            "/m/04fn_": "Television",
            "/m/02vxn": "Movies",
            "/m/06_fw": "Film",
            "/m/02ntfj": "Documentary film",
            "/m/0f2f9": "Comedy",
            "/m/0bzvm2": "Gaming",
            "/m/01sjng": "Video game",
            "/m/0403l3g": "Video game culture",
            "/m/025zzc": "Animal",
            "/m/068hy": "Pet",
            "/m/0ch_cf": "Dog",
            "/m/01yrx": "Cat",
            "/m/07bgp": "Travel",
            "/m/07bxq": "Tourism",
            "/m/01h6rj": "Health",
            "/m/0kt51": "Health",
            "/m/01cgz": "Fitness",
        }
        
        formatted_names = []
        for topic_id in topic_ids:
            readable_name = topic_mapping.get(topic_id, f"Topic: {topic_id}")
            formatted_names.append(readable_name)
        
        return formatted_names