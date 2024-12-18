# import os
# import csv

# # Specify the folder containing the files
# folder_path = "./preprocessing/video_chunks"  # Replace with your folder path
# base_url = input("Enter your hosting URL (without the filenames). For our example, we have our URLs hosted at 'https://marqo-tutorial-public.s3.us-west-2.amazonaws.com/youtube-search-demo/marqo-youtube-videos-chunked/'. Ensure it ends with a '/'. Input your URL here: ")
# data_dir = "./data"
# csv_file_path = os.path.join(data_dir, "video_urls.csv")

# # Create the /data directory if it doesn't exist
# os.makedirs(data_dir, exist_ok=True)

# # Collect file names from the folder
# file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# # Create CSV with video_field
# with open(csv_file_path, mode="w", newline="") as csv_file:
#     csv_writer = csv.writer(csv_file)
#     csv_writer.writerow(["video_field"])

#     for file_name in file_names:
#         file_url = f"{base_url}{file_name}"
#         csv_writer.writerow([file_url])

# print(f"CSV file created at: {csv_file_path}")

# Now create a CSV that takes a YouTube ID in a playlist and saves them
from pytube import Playlist
import csv

# Playlist URL
PLAYLIST_URL = input("Input your YouTube Playlist URL: ")

# Fetch the playlist
playlist = Playlist(PLAYLIST_URL)

# Prepare video details
video_details = [(f"video{i+1}", video.video_id) for i, video in enumerate(playlist.videos)]

# Save to CSV
csv_filename = "./data/youtube_ids.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["video_name", "video_id"])
    writer.writerows(video_details)

print(f"Saved {len(video_details)} videos to '{csv_filename}'")
