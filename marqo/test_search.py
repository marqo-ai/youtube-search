from marqo import Client
import os
from dotenv import load_dotenv
import config

# This file is not used directly within this application but is here if you'd like
# to experiment performing searches

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("MARQO_API_KEY")

mq = Client(url="https://api.marqo.ai", api_key=api_key)

index_name = config.INDEX_NAME

res = mq.index(index_name).search("embedding models")

print(res['hits'][0])
print(res['hits'][1])
