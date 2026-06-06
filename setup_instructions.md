# YouTube Shorts Uploader Setup Guide

## 🎬 Overview
This is a complete YouTube Shorts automation tool that allows you to:
- Upload individual YouTube Shorts
- Batch upload multiple videos
- Get channel information
- View upload history with statistics
- Update video metadata

---

## 📋 Prerequisites

1. **Python 3.7+** installed
2. **YouTube Data API** enabled on Google Cloud Console
3. **YouTube Channel** (obviously!)

---

## 🔑 Step 1: Get YouTube API Credentials

### 1.1 Create Google Cloud Project
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Click "Select a Project" → "New Project"
- Name it: `YouTube-Shorts-Uploader`
- Click "Create"

### 1.2 Enable YouTube Data API v3
- In the search bar, type: `YouTube Data API v3`
- Click on it → Click **"ENABLE"**

### 1.3 Create OAuth 2.0 Credentials
- Go to **"Credentials"** in the left menu
- Click **"+ CREATE CREDENTIALS"**
- Select **"OAuth client ID"**
- Choose **"Desktop application"**
- Click **"Create"**
- You'll get:
  - **Client ID** (copy this)
  - **Client Secret** (copy this)

### 1.4 Get Refresh Token

Download this Python script to get your refresh token:

```python
# get_refresh_token.py
import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_ID = "YOUR_CLIENT_ID_HERE"
CLIENT_SECRET = "YOUR_CLIENT_SECRET_HERE"
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.readonly'
]

def get_refresh_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json', SCOPES)
    
    creds = flow.run_local_server(port=0)
    
    print("\n" + "="*60)
    print("🔑 YOUR REFRESH TOKEN:")
    print("="*60)
    print(creds.refresh_token)
    print("="*60)
    print("\nCopy this token and add it to youtube_uploader.py")
    print("Add it to: YT_REFRESH_TOKEN = 'PASTE_HERE'")

if __name__ == '__main__':
    get_refresh_token()
```

---

## 🔧 Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Step 3: Configure Credentials

Open `youtube_uploader.py` and find the `YouTubeConfig` class:

```python
class YouTubeConfig:
    YT_CLIENT_ID = "YOUR_YT_CLIENT_ID_HERE"           # ← Paste your Client ID
    YT_CLIENT_SECRET = "YOUR_YT_CLIENT_SECRET_HERE"   # ← Paste your Client Secret
    YT_REFRESH_TOKEN = "YOUR_YT_REFRESH_TOKEN_HERE"   # ← Paste your Refresh Token
```

Replace the placeholder values with your actual credentials.

---

## 🚀 Usage Examples

### Single Video Upload

```python
from youtube_uploader import YouTubeUploader

uploader = YouTubeUploader()

video_id = uploader.upload_short(
    video_path='my_video.mp4',
    title='My Awesome YouTube Short',
    description='Check out this amazing content!',
    tags=['shorts', 'viral', 'trending']
)

print(f"Video uploaded! ID: {video_id}")
```

### Batch Upload Multiple Videos

```python
uploader = YouTubeUploader()

videos = [
    {
        'video_path': 'video1.mp4',
        'title': 'First Short - Amazing Content',
        'description': 'Description for video 1',
        'tags': ['shorts', 'trending']
    },
    {
        'video_path': 'video2.mp4',
        'title': 'Second Short - Even Better',
        'description': 'Description for video 2',
        'tags': ['viral', 'shorts']
    },
    {
        'video_path': 'video3.mp4',
        'title': 'Third Short - The Best',
        'description': 'Description for video 3',
        'tags': ['trending', 'amazing']
    }
]

result = uploader.batch_upload(videos)
print(f"\nUploaded: {result['uploaded']}/{result['total']}")
print(f"Video IDs: {result['video_ids']}")
```

### Get Channel Information

```python
uploader = YouTubeUploader()

channel_info = uploader.get_channel_info()
print(f"Channel: {channel_info['channel_name']}")
print(f"Subscribers: {channel_info['subscribers']}")
print(f"Total Views: {channel_info['total_views']:,}")
print(f"Total Videos: {channel_info['total_videos']}")
```

### View Upload History

```python
uploader = YouTubeUploader()

history = uploader.get_upload_history(max_results=10)
for video in history:
    print(f"Title: {video['title']}")
    print(f"Views: {video['views']:,} | Likes: {video['likes']:,}")
    print(f"Published: {video['published_at']}")
    print("---")
```

### Update Video Metadata

```python
uploader = YouTubeUploader()

success = uploader.update_video_metadata(
    video_id='dQw4w9WgXcQ',
    title='Updated Title',
    description='Updated description',
    tags=['new', 'tags']
)
```

---

## 📁 Video Requirements

- **Format:** MP4
- **Max Duration:** 60 seconds (YouTube Shorts limit)
- **Resolution:** 1080x1920 (vertical/portrait)
- **File Size:** Less than 100MB recommended
- **Frame Rate:** 24-60 fps

---

## ⚠️ Troubleshooting

### "Credentials not configured" Error
- ✅ Make sure you've updated all three tokens in `YouTubeConfig`
- ✅ Make sure there are no extra spaces in the token values
- ✅ Make sure the tokens are in quotes: `"TOKEN"`

### "Invalid grant" Error
- ✅ Your refresh token may have expired
- ✅ Run `get_refresh_token.py` again to get a new token
- ✅ Update `YT_REFRESH_TOKEN` with the new value

### "Video file not found" Error
- ✅ Make sure the video file path is correct
- ✅ Use absolute paths if relative paths don't work
- ✅ Make sure the file exists before uploading

### Upload Stuck or Very Slow
- ✅ Check your internet connection
- ✅ Try with a smaller video file first
- ✅ Video uploads are done in 1MB chunks

---

## 🔒 Security Tips

⚠️ **IMPORTANT:**
- ✅ NEVER commit credentials to public repositories
- ✅ Add `youtube_token.pickle` to `.gitignore`
- ✅ Use environment variables for production
- ✅ Rotate your tokens periodically

---

## 📊 Output Example

When you run `python youtube_uploader.py`:

```
============================================================
🎬 YouTube Shorts Uploader
============================================================

📺 Fetching channel information...

✅ Channel: My Awesome Channel
   📊 Subscribers: 50,000
   👁️  Total Views: 1,500,000
   🎬 Total Videos: 120

📝 Recent uploads:

1. My First Viral Short
   👁️  Views: 250,000 | ❤️  Likes: 15,000
   📅 Published: 2024-06-05T10:30:00Z

2. Another Amazing Short
   👁️  Views: 180,000 | ❤️  Likes: 12,000
   📅 Published: 2024-06-04T15:45:00Z
```

---

## 🆘 Need Help?

1. Check YouTube API documentation: https://developers.google.com/youtube/v3
2. Review error messages in the console
3. Make sure all credentials are correct
4. Try with a small test video first

---

## ✨ Features

✅ Upload single or batch videos  
✅ Progress tracking for uploads  
✅ Get channel statistics  
✅ View upload history with metrics  
✅ Update video metadata  
✅ OAuth2 authentication  
✅ Automatic token refresh  
✅ Error handling and logging  

---

**Happy uploading! 🚀**
