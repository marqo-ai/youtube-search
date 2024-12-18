from marqo import Client
import os
from dotenv import load_dotenv
import re
import config

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("MARQO_API_KEY")

mq = Client(url="https://api.marqo.ai", api_key=api_key)

def list_all_documents(input_index_name):
    index = mq.index(input_index_name)
    res = index.search(q='', limit=400)

    video_list = []
    for hit in res['hits']:
        video_list.append({'video_field': hit['video_field'], 'ID': hit['_id']})

    return video_list

index_name = config.INDEX_NAME

# Obtain full list of all video_field
full_list = list_all_documents(index_name)
print("Unsorted List:")
print(full_list)

# Function to extract video numbers
def video_sort_key(entry):
    url = entry['video_field']
    match = re.search(r"video(\d+)_(\d+)\.mp4", url)
    if match:
        video_num = int(match.group(1))  # First number after "video"
        chunk_num = int(match.group(2))  # Second number
        return (video_num, chunk_num)    # Return a tuple for sorting
    return (float("inf"), float("inf"))  # Place invalid entries at the end

# Sort the list of dictionaries by the video_field
sorted_full_list = sorted(full_list, key=video_sort_key)

# Print the sorted list
print("Sorted List:")
for entry in sorted_full_list:
    print(entry)
