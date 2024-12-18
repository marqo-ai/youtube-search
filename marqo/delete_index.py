from marqo import Client
import os
from dotenv import load_dotenv
import config

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("MARQO_API_KEY")

mq = Client(url="https://api.marqo.ai", api_key=api_key)

index_name = config.INDEX_NAME

mq.delete_index(index_name)