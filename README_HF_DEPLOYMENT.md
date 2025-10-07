# YouTube Multi-Search App - Hugging Face Spaces Deployment

## 🚀 Deployment Instructions

### 1. Create a Hugging Face Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose:
   - **SDK**: Streamlit
   - **Hardware**: CPU Basic (free tier)
   - **Visibility**: Public or Private

### 2. Set Up Environment Variables

⚠️ **CRITICAL**: The app requires a YouTube Data API v3 key to function.

**In your Hugging Face Space:**
1. Go to **Settings** tab
2. Click **Variables and secrets**
3. Add a new **Secret**:
   - **Name**: `YOUTUBE_API_KEY`
   - **Value**: Your YouTube Data API v3 key

### 3. Get YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **YouTube Data API v3**
4. Create credentials (API Key)
5. Restrict the API key to YouTube Data API v3 (recommended)

### 4. Upload Files

Upload all files from this `hf_deployment_package` folder to your Hugging Face Space:

```
app.py                 # Main application
requirements.txt       # Dependencies
config.py             # Configuration (secure)
src/                  # Source code
├── core/            # Core functionality
├── ui/              # User interface
└── utils/           # Utilities
docs/                # Documentation
```

### 5. App Features

✨ **Enhanced YouTube Search App** with:

- 🔍 **Multi-Content Search**: Videos, Channels, Playlists
- 📂 **Category Filtering**: 29 YouTube categories
- 🏷️ **Topic Filtering**: 60+ YouTube topics via relevantTopicIds
- 👶 **Kids Content Filter**: COPPA compliance filtering
- 📊 **Rich Metadata**: Views, likes, duration, publish date
- 🎥 **Embedded Player**: Watch videos directly in the app
- 🔧 **Debug Information**: Transparent API data sources

### 6. Security Features

🔒 **API Key Security**:
- ✅ No hardcoded API keys
- ✅ Environment variable configuration
- ✅ Hugging Face Spaces secrets integration
- ✅ Secure for public deployment

### 7. Performance Optimizations

⚡ **Efficient API Usage**:
- Batched video details requests (8% quota savings)
- Smart caching with TTL
- Optimized API call patterns
- Error handling and fallbacks

## 📋 Configuration Details

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `YOUTUBE_API_KEY` | ✅ Yes | YouTube Data API v3 key |
| `SPACE_ID` | Auto-set | Hugging Face Space identifier |

### API Quota Usage

**Typical search for 10 videos**:
- Search API: 100 quota units
- Video Details API: 1 quota unit (batched)
- **Total**: 101 quota units per search

**Daily quota limit**: 10,000 units (default)
**Estimated searches per day**: ~99 searches

## 🛠️ Local Development

For local testing:

```bash
# Set environment variable
export YOUTUBE_API_KEY="your_api_key_here"

# Or create a local config.py file (not committed)
echo 'YOUTUBE_API_KEY = "your_api_key_here"' > config.py

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📊 App Architecture

```
📁 hf_deployment_package/
├── app.py                     # Main Streamlit app
├── config.py                  # Secure configuration
├── requirements.txt           # Dependencies
├── 📁 src/
│   ├── 📁 core/
│   │   ├── youtube_api.py     # YouTube API client
│   │   ├── search_service.py  # Search orchestration
│   │   └── data_processor.py  # Data formatting
│   ├── 📁 ui/
│   │   └── components.py      # Streamlit UI components
│   └── 📁 utils/
│       └── config.py          # Configuration management
└── 📁 docs/
    └── DATA_FLOW_DOCUMENTATION.md  # Technical docs
```

## 🔧 Troubleshooting

### Common Issues

1. **"YouTube API not initialized"**
   - Check that `YOUTUBE_API_KEY` environment variable is set
   - Verify API key is valid and has YouTube Data API v3 enabled

2. **"API quota exceeded"**
   - Monitor usage in Google Cloud Console
   - Consider upgrading quota limits
   - Implement request throttling

3. **Missing topic/category data**
   - Normal behavior - not all videos have complete metadata
   - App provides fallback mechanisms

### Debug Information

The app shows transparent debug information:
- API data sources (Search vs Video Details)
- Topic extraction status
- Category mapping results
- Raw API response data

## 📈 Monitoring

### Usage Tracking
- Monitor API quota in Google Cloud Console
- Track app usage in Hugging Face Spaces analytics
- Review error logs for API failures

### Performance Metrics
- API response times
- Search success rates
- User engagement metrics

## 🔄 Updates

### Updating the App
1. Modify code in your Hugging Face Space
2. Push changes (auto-deploys)
3. Monitor logs for any issues

### API Changes
- YouTube API updates are handled gracefully
- Supports both current and legacy API structures
- Fallback mechanisms for deprecated features

## 🆘 Support

### Resources
- [YouTube Data API Documentation](https://developers.google.com/youtube/v3)
- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [Streamlit Documentation](https://docs.streamlit.io/)

### App Documentation
- See `docs/DATA_FLOW_DOCUMENTATION.md` for technical details
- Check console logs for debug information
- Review API responses in debug mode

---

**🎉 Ready for Deployment!**

Your YouTube Search App is now secure and ready for Hugging Face Spaces deployment with proper API key management and enterprise-grade features.

*Last Updated: October 7, 2025*