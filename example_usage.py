"""
Example Usage Scripts for YouTube Shorts Uploader
Uncomment and modify the examples you want to use
"""

from youtube_uploader import YouTubeUploader
import json

# Initialize the uploader
uploader = YouTubeUploader()


# ============================================================================
# EXAMPLE 1: Upload a Single Video
# ============================================================================
def example_single_upload():
    """
    Upload one YouTube Short video
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Single Video Upload")
    print("="*60 + "\n")
    
    video_id = uploader.upload_short(
        video_path='path/to/your/video.mp4',  # ← Update this path
        title='My Awesome YouTube Short - Check It Out!',
        description='\n'.join([
            'This is an amazing YouTube Short!',
            '',
            '✨ Features:',
            '• High quality content',
            '• Entertaining and engaging',
            '• Don\'t forget to like and subscribe!',
            '',
            '#shorts #viral #trending'
        ]),
        tags=['shorts', 'viral', 'trending', 'youtube', 'awesome'],
        made_for_kids=False
    )
    
    if video_id:
        print(f"\n✅ Success! Your video: https://youtube.com/shorts/{video_id}")
    else:
        print("\n❌ Upload failed. Check the error messages above.")


# ============================================================================
# EXAMPLE 2: Batch Upload Multiple Videos
# ============================================================================
def example_batch_upload():
    """
    Upload multiple YouTube Shorts at once
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Batch Upload Multiple Videos")
    print("="*60 + "\n")
    
    videos_to_upload = [
        {
            'video_path': 'videos/short1.mp4',
            'title': 'Epic Fail Compilation - Part 1',
            'description': 'Check out these funny fails! 😂\n\n#fails #funny #shorts',
            'tags': ['fails', 'funny', 'compilation', 'humor']
        },
        {
            'video_path': 'videos/short2.mp4',
            'title': 'Amazing DIY Hacks You Must Try',
            'description': 'These DIY hacks will blow your mind! 🤯\n\n#diy #hacks #lifehacks',
            'tags': ['diy', 'hacks', 'lifehacks', 'tutorial']
        },
        {
            'video_path': 'videos/short3.mp4',
            'title': 'Trending Dance Challenge - Join Us!',
            'description': 'Do the challenge and tag us! 💃\n\n#dance #challenge #trending',
            'tags': ['dance', 'challenge', 'trending', 'music']
        },
        {
            'video_path': 'videos/short4.mp4',
            'title': 'Recipe: Quick and Easy Snack',
            'description': 'Learn to make this delicious snack in 30 seconds! 😋\n\n#recipe #cooking #food',
            'tags': ['recipe', 'cooking', 'food', 'snack']
        }
    ]
    
    result = uploader.batch_upload(videos_to_upload)
    
    print("\n" + "="*60)
    print("BATCH UPLOAD SUMMARY")
    print("="*60)
    print(json.dumps(result, indent=2))


# ============================================================================
# EXAMPLE 3: Get Channel Information
# ============================================================================
def example_get_channel_info():
    """
    Retrieve your YouTube channel statistics
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: Get Channel Information")
    print("="*60 + "\n")
    
    channel_info = uploader.get_channel_info()
    
    if channel_info:
        print("📺 CHANNEL INFORMATION")
        print("─" * 60)
        print(f"Channel Name: {channel_info['channel_name']}")
        print(f"Channel ID: {channel_info['channel_id']}")
        if channel_info['channel_url'] != 'N/A':
            print(f"Custom URL: {channel_info['channel_url']}")
        print(f"\nSubscribers: {channel_info['subscribers']}")
        print(f"Total Views: {channel_info['total_views']:,}")
        print(f"Total Videos: {channel_info['total_videos']}")
        print(f"\nDescription:")
        print(f"{channel_info['description'][:200]}..." if len(channel_info['description']) > 200 else channel_info['description'])
    else:
        print("❌ Failed to fetch channel information")


# ============================================================================
# EXAMPLE 4: Get Upload History
# ============================================================================
def example_get_upload_history():
    """
    View your recently uploaded videos with statistics
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: Upload History")
    print("="*60 + "\n")
    
    history = uploader.get_upload_history(max_results=10)
    
    if history:
        print(f"📝 RECENT VIDEOS (Last {len(history)} uploads)")
        print("─" * 60)
        for idx, video in enumerate(history, 1):
            print(f"\n{idx}. {video['title']}")
            print(f"   Video ID: {video['id']}")
            print(f"   👁️  Views: {video['views']:,}")
            print(f"   ❤️  Likes: {video['likes']:,}")
            print(f"   💬 Comments: {video['comments']:,}")
            print(f"   📅 Published: {video['published_at']}")
    else:
        print("❌ No videos found or error occurred")


# ============================================================================
# EXAMPLE 5: Update Video Metadata
# ============================================================================
def example_update_metadata():
    """
    Update the title, description, or tags of an existing video
    """
    print("\n" + "="*60)
    print("EXAMPLE 5: Update Video Metadata")
    print("="*60 + "\n")
    
    # Replace with your actual video ID
    video_id = "YOUR_VIDEO_ID_HERE"
    
    if video_id == "YOUR_VIDEO_ID_HERE":
        print("⚠️  Update the video_id in example_update_metadata() first!")
        print("   You can get video IDs from example_get_upload_history()")
        return
    
    success = uploader.update_video_metadata(
        video_id=video_id,
        title="Updated Title - Better SEO Keywords",
        description="Updated description with better content\n\n#updatedtags #newtags",
        tags=['updated', 'new', 'tags', 'seo']
    )
    
    if success:
        print(f"\n✅ Successfully updated video: {video_id}")
    else:
        print(f"\n❌ Failed to update video: {video_id}")


# ============================================================================
# MAIN - Uncomment the examples you want to run
# ============================================================================

if __name__ == '__main__':
    print("\n" + "#"*60)
    print("# YouTube Shorts Uploader - Example Scripts")
    print("#"*60)
    
    # Uncomment the example you want to run:
    
    # example_single_upload()           # Upload one video
    # example_batch_upload()             # Upload multiple videos
    example_get_channel_info()         # Get channel statistics
    example_get_upload_history()       # View upload history
    # example_update_metadata()          # Update video info
    
    print("\n" + "#"*60)
    print("# Done!")
    print("#"*60 + "\n")
