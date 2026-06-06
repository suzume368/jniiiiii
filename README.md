# 🎬 YouTube Shorts Uploader

**Automated YouTube Shorts Upload Tool with OAuth2 Authentication**

> Upload YouTube Shorts programmatically with batch support, channel analytics, and metadata management.

---

## ✨ Features

✅ **Single & Batch Upload** - Upload 1 or 100+ videos  
✅ **Progress Tracking** - Real-time upload progress  
✅ **Channel Analytics** - Get subscribers, views, video count  
✅ **Upload History** - View recent uploads with statistics  
✅ **Metadata Updates** - Edit titles, descriptions, tags  
✅ **OAuth2 Secure** - Industry-standard authentication  
✅ **Error Handling** - Comprehensive error messages  
✅ **Resumable Uploads** - Continue interrupted uploads  

---

## 📋 Requirements

- Python 3.7+
- YouTube Channel
- Google Cloud Project with YouTube Data API v3 enabled
- ~50MB free disk space

---

## 🚀 Quick Start

### 1️⃣ Installation

```bash
# Clone or download this repository
git clone <repo-url>
cd youtube-shorts-uploader

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Get Credentials

Follow the detailed guide in `setup_instructions.md` to:
1. Create a Google Cloud Project
2. Enable YouTube Data API v3
3. Generate OAuth2 credentials
4. Get your refresh token

### 3️⃣ Configure

Edit `youtube_uploader.py` and update:

```python
class YouTubeConfig:
    YT_CLIENT_ID = "your_client_id_here"
    YT_CLIENT_SECRET = "your_client_secret_here"
    YT_REFRESH_TOKEN = "your_refresh_token_here"
```

### 4️⃣ Upload!

```python
from youtube_uploader import YouTubeUploader

uploader = YouTubeUploader()
video_id = uploader.upload_short(
    video_path='my_video.mp4',
    title='My Awesome Short',
    description='Check this out!',
    tags=['shorts', 'viral']
)
print(f"Uploaded: {video_id}")
```

---

## 📖 Usage Examples

### Single Upload

```python
uploader = YouTubeUploader()
video_id = uploader.upload_short(
    video_path='video.mp4',
    title='My Video Title',
    description='My Video Description',
    tags=['tag1', 'tag2', 'tag3']
)
```

### Batch Upload

```python
uploader = YouTubeUploader()

videos = [
    {
        'video_path': 'video1.mp4',
        'title': 'First Video',
        'description': 'Description 1',
        'tags': ['tag1']
    },
    {
        'video_path': 'video2.mp4',
        'title': 'Second Video',
        'description': 'Description 2',
        'tags': ['tag2']
    }
]

result = uploader.batch_upload(videos)
print(f"Uploaded: {result['uploaded']}/{result['total']}")
```

### Get Channel Info

```python
uploader = YouTubeUploader()
info = uploader.get_channel_info()

print(f"Channel: {info['channel_name']}")
print(f"Subscribers: {info['subscribers']}")
print(f"Total Views: {info['total_views']:,}")
print(f"Videos: {info['total_videos']}")
```

### View Upload History

```python
uploader = YouTubeUploader()
history = uploader.get_upload_history(max_results=10)

for video in history:
    print(f"{video['title']}")
    print(f"  Views: {video['views']:,}")
    print(f"  Likes: {video['likes']:,}")
```

### Update Metadata

```python
uploader = YouTubeUploader()
success = uploader.update_video_metadata(
    video_id='VIDEO_ID',
    title='New Title',
    description='New Description',
    tags=['new', 'tags']
)
```

See `example_usage.py` for more examples!

---

## 📁 Project Structure

```
youtube-shorts-uploader/
├── youtube_uploader.py       # Main uploader class
├── example_usage.py          # Example scripts
├── requirements.txt          # Python dependencies
├── setup_instructions.md     # Detailed setup guide
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

---

## ⚙️ Configuration

### Video Requirements

- **Format:** MP4 (H.264 video codec)
- **Duration:** Max 60 seconds
- **Resolution:** 1080x1920 (portrait/vertical)
- **Frame Rate:** 24-60 fps
- **File Size:** <100MB recommended
- **Audio:** AAC codec, 48kHz

### Upload Limits

- YouTube free account: 15GB/day
- Processing may take 5-30 minutes
- Batch uploads are sequential
- No rate limiting per upload

---

## 🔒 Security

✅ **DO:**
- Keep credentials secret
- Use `.env` files for local development
- Rotate tokens periodically
- Review uploaded content before publishing

❌ **DON'T:**
- Commit `youtube_token.pickle` to version control
- Share your refresh token
- Use hardcoded credentials in production
- Store credentials in public repositories

---

## 🆘 Troubleshooting

### Authentication Failed
```
❌ Make sure you've updated all credentials in YouTubeConfig
✅ Verify no extra spaces in token values
✅ Ensure tokens are in quotes
```

### Invalid Grant Error
```
❌ Refresh token may have expired
✅ Run credential setup again to get new token
✅ Update YT_REFRESH_TOKEN with new value
```

### Video File Not Found
```
❌ Check file path is correct
✅ Use absolute paths if relative fails
✅ Verify file exists before uploading
```

### Upload Stuck
```
❌ Check internet connection
✅ Try with smaller video first
✅ Uploads use 1MB chunks
✅ Monitor network speed
```

### API Quota Exceeded
```
❌ You've hit daily quota limits
✅ Wait 24 hours before uploading
✅ Check Google Cloud Console for quotas
```

---

## 📊 Supported API Endpoints

- ✅ `youtube.videos().insert()` - Upload videos
- ✅ `youtube.videos().list()` - Get upload history
- ✅ `youtube.videos().update()` - Update metadata
- ✅ `youtube.channels().list()` - Get channel info

---

## 📝 API Reference

### `YouTubeUploader`

#### `__init__(config: YouTubeConfig)`
Initialize uploader with credentials.

#### `upload_short(video_path, title, description, tags=None, made_for_kids=False)`
Upload a single YouTube Short.

**Parameters:**
- `video_path` (str): Path to video file
- `title` (str): Video title (max 100 chars)
- `description` (str): Video description (max 5000 chars)
- `tags` (list): Video tags/keywords
- `made_for_kids` (bool): Is video for kids?

**Returns:** Video ID (str) or None

#### `batch_upload(videos_data: list)`
Upload multiple videos sequentially.

**Parameters:**
- `videos_data` (list): List of video dicts

**Returns:** Summary dict with counts and IDs

#### `get_channel_info()`
Get channel statistics.

**Returns:** Dict with channel info or None

#### `get_upload_history(max_results: int)`
Get recently uploaded videos.

**Parameters:**
- `max_results` (int): Max videos to fetch (1-50)

**Returns:** List of video dicts

#### `update_video_metadata(video_id, title=None, description=None, tags=None)`
Update video metadata.

**Parameters:**
- `video_id` (str): YouTube video ID
- `title` (str): New title
- `description` (str): New description
- `tags` (list): New tags

**Returns:** Boolean success status

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - feel free to use this tool!

---

## 📞 Support

Need help? Check:
- `setup_instructions.md` - Detailed setup guide
- `example_usage.py` - Working examples
- [YouTube API Docs](https://developers.google.com/youtube/v3)
- [Google Cloud Console](https://console.cloud.google.com/)

---

## ⭐ Star This Repo!

If you find this tool useful, please star it! ⭐

---

**Made with ❤️ for content creators**

**Happy uploading! 🚀**
