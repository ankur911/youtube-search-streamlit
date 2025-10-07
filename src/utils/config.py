"""
Configuration management for the YouTube Search App.
"""

import os


class Config:
    """Application configuration management."""
    
    # API Configuration - secure for Hugging Face Spaces
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    
    # Check if running on Hugging Face Spaces
    IS_HUGGING_FACE = os.getenv('SPACE_ID') is not None
    
    # Search Configuration
    DEFAULT_MAX_RESULTS = 10
    MAX_RESULTS_LIMIT = 50
    
    # UI Configuration
    PAGE_TITLE = "YouTube Multi-Search App - Enhanced"
    PAGE_ICON = "🎥"
    LAYOUT = "wide"
    
    # Cache Configuration
    CACHE_TTL = 3600  # 1 hour
    
    @classmethod
    def load_from_file(cls, config_file='config.py'):
        """Load configuration from file (only for local development)."""
        # Skip file loading if running on Hugging Face Spaces
        if cls.IS_HUGGING_FACE:
            return
            
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config_content = f.read()
                    if 'YOUTUBE_API_KEY' in config_content and not config_content.strip().startswith('#'):
                        # Execute the config file to load variables
                        local_vars = {}
                        exec(config_content, {}, local_vars)
                        if 'YOUTUBE_API_KEY' in local_vars and local_vars['YOUTUBE_API_KEY']:
                            # Only use file API key if environment variable is not set
                            if not cls.YOUTUBE_API_KEY:
                                cls.YOUTUBE_API_KEY = local_vars['YOUTUBE_API_KEY']
        except Exception as e:
            print(f"Error loading config file: {e}")
    
    @classmethod
    def save_api_key(cls, api_key, config_file='config.py'):
        """Save API key to config file (only for local development)."""
        # Don't save to file if running on Hugging Face Spaces
        if cls.IS_HUGGING_FACE:
            cls.YOUTUBE_API_KEY = api_key
            return True
            
        try:
            config_content = f'''# YouTube API Configuration for Hugging Face Spaces
import os

# Get API key from Hugging Face Spaces environment variable
# Set this in your Hugging Face Space Settings > Variables and secrets
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', "{api_key}")

# For local development, you can set YOUTUBE_API_KEY environment variable
# or use a local config file (not committed to git)

# Configuration automatically updated by the app
'''
            with open(config_file, 'w') as f:
                f.write(config_content)
            cls.YOUTUBE_API_KEY = api_key
            return True
        except Exception as e:
            print(f"Error saving config file: {e}")
            return False


# Load configuration on import
Config.load_from_file()