from marqo import Client
import os
from dotenv import load_dotenv
import pandas as pd
import config

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("MARQO_API_KEY")

mq = Client(url="https://api.marqo.ai", api_key=api_key)

path_to_data = "data/video_urls.csv"  # Define the path to the CSV file containing product data
df = pd.read_csv(path_to_data)

documents = [
    {"video_field": video_field}
    for video_field in df["video_field"]
]

index_name = config.INDEX_NAME

res = mq.index(index_name).add_documents(
    documents=documents,
    client_batch_size=1,
    tensor_fields=['video_field'],
    use_existing_tensors=False,
)

print(res)