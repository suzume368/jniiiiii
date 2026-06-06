"""
YouTube Shorts Uploader Module
Handles YouTube Shorts automation with OAuth2 authentication
Update YT_REFRESH_TOKEN manually before running
"""

import os
import pickle
import json
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


class YouTubeConfig:
    """YouTube API Configuration - UPDATE THESE MANUALLY"""
    
    # ========== ⚠️ MANUAL UPDATE REQUIRED - ADD YOUR TOKENS HERE ⚠️ ==========
    YT_CLIENT_ID = "YOUR_YT_CLIENT_ID_HERE"
    YT_CLIENT_SECRET = "YOUR_YT_CLIENT_SECRET_HERE"
    YT_REFRESH_TOKEN = "YOUR_YT_REFRESH_TOKEN_HERE"
    # =========================================================================
    
    SCOPES = [
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/youtube',
        'https://www.googleapis.com/auth/youtube.readonly'
    ]
    
    CREDENTIALS_FILE = 'youtube_credentials.pickle'
    TOKEN_FILE = 'youtube_token.pickle'


class YouTubeUploader:
    """Main YouTube Shorts Uploader Class"""
    
    def __init__(self, config: YouTubeConfig = None):
        """Initialize YouTube uploader with credentials"""
        self.config = config or YouTubeConfig()
        self.youtube = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with YouTube API using OAuth2"""
        try:
            # Try to load existing credentials
            if os.path.exists(self.config.TOKEN_FILE):
                with open(self.config.TOKEN_FILE, 'rb') as token:
                    creds = pickle.load(token)
                    if creds and creds.valid:
                        self.youtube = build('youtube', 'v3', credentials=creds)
                        print("✅ Authenticated using saved token")
                        return
            
            # Check if manual credentials are provided
            if (self.config.YT_REFRESH_TOKEN and 
                self.config.YT_REFRESH_TOKEN != "YOUR_YT_REFRESH_TOKEN_HERE"):
                
                creds = Credentials(
                    token=None,
                    refresh_token=self.config.YT_REFRESH_TOKEN,
                    token_uri="https://oauth2.googleapis.com/token",
                    client_id=self.config.YT_CLIENT_ID,
                    client_secret=self.config.YT_CLIENT_SECRET
                )
                
                # Refresh token if needed
                request = google.auth.transport.requests.Request()
                creds.refresh(request)
                
                # Save token for future use
                with open(self.config.TOKEN_FILE, 'wb') as token:
                    pickle.dump(creds, token)
                
                self.youtube = build('youtube', 'v3', credentials=creds)
                print("✅ Authenticated using refresh token")
                return
            
            raise Exception(
                "❌ Credentials not configured. Please add your tokens to YouTubeConfig class:"
                "\n   YT_CLIENT_ID\n   YT_CLIENT_SECRET\n   YT_REFRESH_TOKEN"
            )
        
        except Exception as e:
            print(f"❌ Authentication failed: {str(e)}")
            raise
    
    def upload_short(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: list = None,
        made_for_kids: bool = False
    ) -> Optional[str]:
        """
        Upload a YouTube Short (vertical video)
        
        Args:
            video_path: Path to video file (MP4)
            title: Video title (max 100 chars)
            description: Video description (max 5000 chars)
            tags: List of tags/keywords
            made_for_kids: Is video made for kids?
        
        Returns:
            Video ID if successful, None otherwise
        """
        try:
            if not os.path.exists(video_path):
                print(f"❌ Video file not found: {video_path}")
                return None
            
            file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
            print(f"📁 File size: {file_size:.2f} MB")
            
            # Prepare request body
            request_body = {
                'snippet': {
                    'title': title[:100],
                    'description': description[:5000],
                    'tags': tags or [],
                    'categoryId': '22',  # Shorts category
                },
                'processingDetails': {
                    'processingStatus': 'processing'
                },
                'status': {
                    'privacyStatus': 'public',
                    'madeForKids': made_for_kids,
                    'selfDeclaredMadeForKids': made_for_kids,
                },
            }
            
            # Upload video with resumable chunks
            media_upload = MediaFileUpload(
                video_path,
                mimetype='video/mp4',
                resumable=True,
                chunksize=1024 * 1024  # 1MB chunks
            )
            
            print(f"\n📤 Uploading: {title}")
            print(f"📁 File: {video_path}")
            print("⏳ Upload in progress...\n")
            
            request = self.youtube.videos().insert(
                part='snippet,processingDetails,status',
                body=request_body,
                media_body=media_upload
            )
            
            # Execute with progress tracking
            response = None
            previous_progress = 0
            
            while response is None:
                status, response = request.next_chunk()
                if status:
                    current_progress = int(status.progress() * 100)
                    if current_progress != previous_progress:
                        print(f"⏳ Upload progress: {current_progress}%")
                        previous_progress = current_progress
            
            video_id = response.get('id')
            print(f"\n✅ Upload successful!")
            print(f"🎬 Video ID: {video_id}")
            print(f"🔗 URL: https://youtube.com/shorts/{video_id}")
            
            return video_id
        
        except HttpError as e:
            print(f"❌ HTTP Error: {e}")
            return None
        except Exception as e:
            print(f"❌ Upload failed: {str(e)}")
            return None
    
    def get_upload_history(self, max_results: int = 10) -> list:
        """Get list of recently uploaded videos"""
        try:
            request = self.youtube.videos().list(
                part='snippet,statistics',
                forMine=True,
                maxResults=min(max_results, 50),
                order='date'
            )
            response = request.execute()
            
            videos = []
            for item in response.get('items', []):
                video_data = {
                    'id': item['id'],
                    'title': item['snippet']['title'],
                    'published_at': item['snippet']['publishedAt'],
                    'views': int(item['statistics'].get('viewCount', 0)),
                    'likes': int(item['statistics'].get('likeCount', 0)),
                    'comments': int(item['statistics'].get('commentCount', 0)),
                }
                videos.append(video_data)
            
            return videos
        
        except Exception as e:
            print(f"❌ Error fetching history: {str(e)}")
            return []
    
    def get_channel_info(self) -> Optional[Dict[str, Any]]:
        """Get YouTube channel information"""
        try:
            request = self.youtube.channels().list(
                part='snippet,statistics',
                mine=True
            )
            response = request.execute()
            
            if response['items']:
                channel = response['items'][0]
                return {
                    'channel_id': channel['id'],
                    'channel_name': channel['snippet']['title'],
                    'channel_url': channel['snippet']['customUrl'] if 'customUrl' in channel['snippet'] else 'N/A',
                    'subscribers': channel['statistics'].get('subscriberCount', 'Private'),
                    'total_views': int(channel['statistics'].get('viewCount', 0)),
                    'total_videos': int(channel['statistics'].get('videoCount', 0)),
                    'description': channel['snippet']['description'],
                }
            return None
        
        except Exception as e:
            print(f"❌ Error fetching channel info: {str(e)}")
            return None
    
    def batch_upload(self, videos_data: list) -> Dict[str, Any]:
        """
        Upload multiple videos in batch
        
        Args:
            videos_data: List of dicts with keys:
                - video_path: Path to video file
                - title: Video title
                - description: Video description
                - tags: (optional) List of tags
        
        Returns:
            Summary with uploaded/failed counts and video IDs
        """
        summary = {
            'total': len(videos_data),
            'uploaded': 0,
            'failed': 0,
            'video_ids': [],
            'errors': []
        }
        
        print(f"\n{'='*60}")
        print(f"🎬 BATCH UPLOAD START - {len(videos_data)} videos")
        print(f"{'='*60}\n")
        
        for idx, video in enumerate(videos_data, 1):
            print(f"\n[{idx}/{len(videos_data)}] Processing video...")
            print(f"{'─'*60}")
            
            video_id = self.upload_short(
                video_path=video['video_path'],
                title=video['title'],
                description=video.get('description', ''),
                tags=video.get('tags', [])
            )
            
            if video_id:
                summary['uploaded'] += 1
                summary['video_ids'].append(video_id)
            else:
                summary['failed'] += 1
                summary['errors'].append(f"Failed: {video['title']}")
        
        print(f"\n{'='*60}")
        print(f"📊 BATCH UPLOAD COMPLETE")
        print(f"{'='*60}")
        print(f"✅ Uploaded: {summary['uploaded']}/{summary['total']}")
        print(f"❌ Failed: {summary['failed']}/{summary['total']}")
        if summary['video_ids']:
            print(f"\n🎬 Video IDs:")
            for vid_id in summary['video_ids']:
                print(f"   • {vid_id}")
        
        return summary
    
    def update_video_metadata(
        self,
        video_id: str,
        title: str = None,
        description: str = None,
        tags: list = None
    ) -> bool:
        """Update video title, description, or tags"""
        try:
            # Get current video details
            request = self.youtube.videos().list(
                part='snippet',
                id=video_id
            )
            response = request.execute()
            
            if not response['items']:
                print(f"❌ Video not found: {video_id}")
                return False
            
            video = response['items'][0]
            snippet = video['snippet']
            
            # Update fields
            if title:
                snippet['title'] = title[:100]
            if description:
                snippet['description'] = description[:5000]
            if tags:
                snippet['tags'] = tags
            
            # Update video
            update_request = self.youtube.videos().update(
                part='snippet',
                body={'id': video_id, 'snippet': snippet}
            )
            update_request.execute()
            
            print(f"✅ Video metadata updated: {video_id}")
            return True
        
        except Exception as e:
            print(f"❌ Error updating metadata: {str(e)}")
            return False


def main():
    """
    Main function with example usage
    Uncomment the functions you want to use
    """
    
    print("\n" + "="*60)
    print("🎬 YouTube Shorts Uploader")
    print("="*60 + "\n")
    
    try:
        # Initialize uploader
        uploader = YouTubeUploader()
        
        # Get channel info
        print("📺 Fetching channel information...\n")
        channel_info = uploader.get_channel_info()
        if channel_info:
            print(f"✅ Channel: {channel_info['channel_name']}")
            print(f"   📊 Subscribers: {channel_info['subscribers']}")
            print(f"   👁️  Total Views: {channel_info['total_views']:,}")
            print(f"   🎬 Total Videos: {channel_info['total_videos']}")
            print()
        
        # Example: Upload a single video
        # Uncomment below to use:
        # video_id = uploader.upload_short(
        #     video_path='path/to/your/video.mp4',
        #     title='My Awesome YouTube Short',
        #     description='Check out this amazing short video!',
        #     tags=['shorts', 'viral', 'trending']
        # )
        
        # Example: Batch upload multiple videos
        # Uncomment below to use:
        # videos = [
        #     {
        #         'video_path': 'video1.mp4',
        #         'title': 'First Amazing Short',
        #         'description': 'First video description',
        #         'tags': ['tag1', 'tag2']
        #     },
        #     {
        #         'video_path': 'video2.mp4',
        #         'title': 'Second Amazing Short',
        #         'description': 'Second video description',
        #         'tags': ['tag3', 'tag4']
        #     }
        # ]
        # result = uploader.batch_upload(videos)
        # print(f"\n📊 Batch Summary: {json.dumps(result, indent=2)}")
        
        # Example: Get upload history
        print("📝 Recent uploads:\n")
        history = uploader.get_upload_history(max_results=5)
        if history:
            for idx, video in enumerate(history, 1):
                print(f"{idx}. {video['title']}")
                print(f"   👁️  Views: {video['views']:,} | ❤️  Likes: {video['likes']:,}")
                print(f"   📅 Published: {video['published_at']}\n")
        else:
            print("No videos found or error fetching history.\n")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n⚠️  Make sure you've updated the YouTube credentials in youtube_uploader.py")


if __name__ == '__main__':
    main()
