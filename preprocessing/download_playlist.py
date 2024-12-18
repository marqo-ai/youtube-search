import yt_dlp
import os
from moviepy.video.io.VideoFileClip import VideoFileClip

def download_youtube_playlist_yt_dlp(playlist_url, download_path=".preprocessing/raw_youtube_videos"):
    # Set options for yt-dlp
    ydl_opts = {
        'outtmpl': f'{download_path}/%(playlist_index)03d_%(title)s.%(ext)s',  # Include playlist index for order
        'format': 'bestvideo+bestaudio/best',  # Best quality
        'merge_output_format': 'mp4',  # Ensure output is in .mp4 format
    }

    # Create download directory if it doesn't exist
    os.makedirs(download_path, exist_ok=True)
    
    print(f"Downloading playlist: {playlist_url}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

def chunk_video(file_path, output_dir, base_name, chunk_duration=20):
    """
    Splits a video file into chunks of specified duration.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    video = VideoFileClip(file_path)
    total_duration = video.duration
    
    chunk_count = 1
    start_time = 0
    while start_time < total_duration:
        end_time = min(start_time + chunk_duration, total_duration)
        chunk = video.subclipped(start_time, end_time)  # Correct method
        chunk_name = f"{base_name}_{chunk_count}.mp4"
        chunk_path = os.path.join(output_dir, chunk_name)
        chunk.write_videofile(chunk_path, codec="libx264", audio_codec="mp3")
        print(f"Created chunk: {chunk_name}")
        chunk_count += 1
        start_time += chunk_duration
    
    video.close()

# Download your YouTube playlist
playlist_url = input("Enter your YouTube playlist: ")
download_path = "./preprocessing/raw_youtube_videos"
download_youtube_playlist_yt_dlp(playlist_url, download_path)

# Path to the folder containing your MP4 files
folder_path = download_path

# Output folder for video chunks
chunk_output_path = "./preprocessing/video_chunks"

# Get a list of all MP4 files in the folder
mp4_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]

# Sort the files by playlist index (they're already named sequentially)
mp4_files.sort()

# Iterate over the files and chunk them
for idx, file_name in enumerate(mp4_files, start=1):
    input_path = os.path.join(folder_path, file_name)
    base_name = f"video{idx}"
    print(f"Processing {file_name}...")
    chunk_video(input_path, chunk_output_path, base_name, chunk_duration=20)

print("Video chunking complete!")
