from marqo import Client
import os
from dotenv import load_dotenv
import config

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("MARQO_API_KEY")

mq = Client(url="https://api.marqo.ai", api_key=api_key)

# Define settings for the index
settings = {
    "type": "unstructured",
    "vectorNumericType": "float",
    "model": "LanguageBind/Video_V1.5_FT_Audio_FT_Image",
    "normalizeEmbeddings": True,
    "treatUrlsAndPointersAsMedia": True,
    "treatUrlsAndPointersAsImages": True,
    "audioPreprocessing": {
        "splitLength": 10,
        "splitOverlap": 5,
    },
    "videoPreprocessing": {
        "splitLength": 20,
        "splitOverlap": 5,
    },
    "inferenceType": "marqo.GPU",
}

# Create a new index with the specified settings
index_name = config.INDEX_NAME
mq.create_index(index_name=index_name, settings_dict=settings)
