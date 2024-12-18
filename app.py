import streamlit as st
from marqo import Client
import os
from dotenv import load_dotenv
import re
import csv
import config

# Set full-screen page layout
st.set_page_config(page_title="Marqo YouTube Video Search App", layout="wide")

# Load environment variables
load_dotenv()
api_key = os.getenv("MARQO_API_KEY")

# Initialize Marqo client
mq = Client(url="https://api.marqo.ai", api_key=api_key)

# Load VIDEO_ID_MAP from CSV
VIDEO_ID_MAP = {}
with open("data/youtube_ids.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        VIDEO_ID_MAP[row["video_name"]] = row["video_id"]


def get_youtube_link(url):
    """
    Given a chunked video URL, return the corresponding YouTube link with timestamp.
    """
    match = re.search(r"video(\d+)_(\d+)\.mp4", url)
    if not match:
        return "Invalid URL"

    video_num = match.group(1)  # Video number
    chunk_num = int(match.group(2))  # Chunk number

    # Map video number to YouTube video ID
    video_key = f"video{video_num}"
    youtube_id = VIDEO_ID_MAP.get(video_key)

    if not youtube_id:
        return "YouTube video ID not found"

    # Calculate the start time in seconds
    start_time = (chunk_num - 1) * 20  # Each chunk is 20 seconds

    # Construct the YouTube link
    youtube_url = f"https://www.youtube.com/watch?v={youtube_id}&t={start_time}s"
    return youtube_url

@st.cache_data
def search_videos(query):
    """Fetch top 6 video URLs."""
    try:
        index_name = config.INDEX_NAME
        res = mq.index(index_name).search(query)
        print(res['hits'][0])
        video_urls = [result.get('video_field') for result in res.get('hits', [])[:6]]
        return video_urls
    except Exception as e:
        print(e)
        return []

# Streamlit app layout
st.title("Marqo YouTube Video Search")
st.text("Perform visual and audio searches over YouTube videos. This demo uses Marqo's YouTube channel to search for relevant information and will direct you to the corresponding timestamp in the YouTube video.")
st.text("Examples: \"What are embedding models?\", \"Marqo API Key?\", \" Demo Presentation?\"")

query = st.text_input("Input your query...", "fun fact")

if st.button("Search") and query:
    with st.spinner("Fetching videos..."):
        video_urls = search_videos(query)

    # Display videos in a 3x2 grid
    if video_urls:
        rows = 2
        cols = 3
        video_grid = st.columns(cols)  # Define columns for the grid layout

        for i, video_url in enumerate(video_urls):
            if video_url:
                youtube_link = get_youtube_link(video_url)  # Generate the YouTube link

                with video_grid[i % cols]:  # Place video in the correct column
                    st.video(video_url)  # Display video
                    if "youtube" in youtube_link:
                        st.markdown(f"[**Watch this on YouTube**]({youtube_link})", unsafe_allow_html=True)

            if (i + 1) % cols == 0:  # Create new columns for the next row
                video_grid = st.columns(cols)

    else:
        st.error("No videos found. Try a different query.")
