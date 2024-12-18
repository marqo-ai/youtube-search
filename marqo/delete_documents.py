from marqo import Client
import os
from dotenv import load_dotenv
import config

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("MARQO_API_KEY")

mq = Client(url="https://api.marqo.ai", api_key=api_key)

index_name = config.INDEX_NAME

# This deletes documents by their ids
mq.index(index_name).delete_documents(
    ids=[
        "b6eefc39-e8a8-4aac-98ed-4abaf6d50848"
        ]
    )

# This will delete all documents in your index
def empty_index(input_index_name):
    index = mq.index(input_index_name)
    res =  index.search(q = '', limit=400)
    while len(res['hits']) > 0:
        id_set = []
        for hit in res['hits']:
            id_set.append(hit['_id'])
        index.delete_documents(id_set)
        res = index.search(q = '', limit=400)

# Only do this if you want EVERY document in your index deleting
# empty_index(index_name)