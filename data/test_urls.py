# This code checks the validity of the URLs. You should not need this but if you want to 
# check all files still exist and are accessible, this code will do that. 
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# Load the list of URLs from the CSV file
input_csv = "./data/video_urls.csv"
df = pd.read_csv(input_csv)
urls = df["video_field"].tolist()

# Function to check URL validity
def check_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code == 200:
            return None
        else:
            return url
    except requests.RequestException:
        return url

# Use ThreadPoolExecutor for concurrent checking
print("Checking URLs...")
with ThreadPoolExecutor(max_workers=10) as executor:
    for result in executor.map(check_url, urls):
        if result:
            print(f"URL not working: {result}")