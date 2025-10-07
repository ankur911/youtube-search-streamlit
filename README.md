---
title: YouTube Multi-Search App
emoji: 🎥
colorFrom: red
colorTo: blue
sdk: streamlit
sdk_version: 1.50.0
app_file: app.py
pinned: false
license: mit
---

# YouTube Multi-Search App 🎥

**Advanced YouTube search application with comprehensive filtering capabilities.**

## ✨ Features

- 🔍 **Advanced Search**: Videos, channels, and playlists with enhanced filtering
- 📂 **Category Filters**: 15 YouTube video categories (Education, Music, Gaming, etc.)
- 🏷️ **Topic Filters**: 56+ topic categories with smart keyword matching
- 👶 **Kids Content**: Safe content filtering for family-friendly results
- 🎬 **Embedded Player**: Watch videos directly in the app
- 📊 **Rich Metadata**: Detailed statistics, view counts, and descriptions
- 🛡️ **Safe Search**: Configurable content safety levels

## 🚀 Quick Start

1. **Add your YouTube API key** as a secret variable named `YOUTUBE_API_KEY`
2. **Enter your search terms** in the sidebar
3. **Apply filters** to refine your results
4. **Enjoy enhanced YouTube discovery!**

## 🔑 Setup Instructions

### Get YouTube Data API v3 Key:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Enable "YouTube Data API v3"
4. Create an API Key credential
5. Add it as `YOUTUBE_API_KEY` secret in this Space

## 🏗️ Architecture

This app uses a **modular architecture** with clean separation of concerns:

- **Core Logic**: API client, data processing, search orchestration
- **UI Components**: Streamlit interface elements
- **Configuration**: Centralized settings management

## 🎯 Example Searches

- **Educational**: "python tutorial" + Education category + Technology topic
- **Kids Content**: "learning songs" + Kids Only filter
- **Music**: "classical music" + Music category + Classical topic
- **Gaming**: "minecraft gameplay" + Gaming category

## 📱 Responsive Design

Optimized for both desktop and mobile viewing with an intuitive sidebar interface.

---

**Powered by YouTube Data API v3 | Built with Streamlit**