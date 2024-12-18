# YouTube Video and Audio Search
This repository performs searches over content that appears in YouTube videos. This demo uses Marqo's YouTube channel to search for relevant video clips. It will then direct you to that specific timestamp on YouTube. 

<p align="center">
    <a><img src="https://github.com/marqo-ai/youtube-search/blob/main/assets/youtube-search.gif"></a>
</p>

Note, this demo uses already chunked data that is hosted online. If you want to do this for your own YouTube videos, we have provided the code that downloads a YouTube playlist and chunks the data for you. It is then up to you to host these files somewhere. We recommend using AWS S3 buckets. 

## Step 1: Clone this Repository
You can do this with:
```bash
git clone https://github.com/marqo-ai/youtube-search
```
Then, load all the dependencies needed for this project.
```bash
python3 -m venv venv
source venv/bin/activate   # For Windows, run  venv\Scripts\activate
pip3 install -r requirements.txt
```

## Step 2: (Optional) Download Your YouTube Videos
This step is optional. If you are happy using Marqo's youtube videos to build this project then you can jump straight to Step 4.

If you want to download your own YouTube videos, keep reading. We encourage you to create a small playlist of your videos to begin with, depending on their size. For this demo, we have 10 videos that vary in size from 3 minutes to 24 minutes. Note, if you want to test this out with just one YouTube video, you can also just specify the individual YouTube link. To download your YouTube playlist, run the following code:
```bash
python3 preprocessing/download_playlist.py
```
Enter your YouTube playlist when prompted to do so.

This will first begin downloading your YouTube video(s) and placing them into the folder `processing/raw_youtube_videos`. Once all videos have been downloaded to this folder, it will begin chunking them into 20 second splits and placing these into the `processing/video_chunks`. This is needed when loading the video files into Marqo ready to perform video and audio searches. 

## Step 3: (Optional) Hosting Your YouTube Videos
To load these video files into Marqo, they need to be hosted at a URL address so Marqo can successfully retrieve them. For this demo, we hosted our YouTuube videos using an AWS S3 Bucket. Feel free to use whichever hosting platform you'd like, just ensure the URL ends in `.mp4` and is publicly accessible so Marqo can access and retrieve it.

Once you have hosted your YouTube videos, we need to create the data CSV file that will be fed into Marqo. This keeps track of all URLs. First, obtain the starting URL to your videos. In our example, our videos are hosted at `https://marqo-tutorial-public.s3.us-west-2.amazonaws.com/youtube-search-demo/marqo-youtube-videos-chunked/` and so, we append each video title in `video_chunks` to this URL and store them in a CSV, for each video.

To create this data CSV, run the following:
```bash
python3 preprocessing/generate_urls.py
```
This will create a new CSV in the `data` folder called `video_urls.csv` which will contain all of the URLs for your chunked videos. It will also create another file called `youtube_ids.csv` which will contain the corresponding YouTube video IDs. Note: if you do this for Marqo's YouTube playlist, the IDs will be slightly different as the files were preprocessed and loaded using a different playlist. 

For peace of mind, we encourage you to check that all of the URLs in the `video_urls.csv` file are valid. This will avoid Marqo throwing any errors if it cannot access them. Run this script to check your URLs:
```bash
python3 data/test_urls.py
```
The terminal will only populate with URLs if an error has occurred. 
## Step 4: Set up Marqo Index
Now we have all of our data, we can set up a Marqo index and begin adding these video files to our index. 

### Obtain API Key
First, you will need a Marqo Cloud API Key. To obtain this, visit this [article](https://www.marqo.ai/blog/finding-my-marqo-api-key).
Once you have your API Key, place it inside a `.env` file such that:
```env
MARQO_API_KEY = "XXXXXXXX"   # Visit https://www.marqo.ai/blog/finding-my-marqo-api-key 
```

### Create Marqo Index
Next, we can create our index:
```bash
python3 marqo/create_index.py
```

This may take a few minutes to create. You can see the status of your index in the [Marqo Cloud Console](https://cloud.marqo.ai/indexes):

Your terminal will also begin populating:
```bash
2024-12-18 16:13:44,437 logger:'marqo' INFO Current index status: IndexStatus.CREATING
2024-12-18 16:13:55,621 logger:'marqo' INFO Current index status: IndexStatus.CREATING
2024-12-18 16:14:06,816 logger:'marqo' INFO Current index status: IndexStatus.CREATING
...
```

### Add Documents to Marqo Index
Once your index is successfully created, you can begin adding documents to your index. If you index creation failed for whatever reason, reach out to us on our [Slack Community](https://join.slack.com/t/marqo-community/shared_invite/zt-2b4nsvbd2-TDf8agPszzWH5hYKBMIgDA) where a member of our team can help. 

To add documents to your index, run:
```bash
python3 marqo/add_documents.py
```
This will read all of the video URLs in `data/video_urls.csv` and begin uploading them to Marqo Cloud. We have chosen a batch size of 1 so that we can see logs for each video URL added. 

### (Optional) List All Documents / Get Stats
While documents are being added to your index, I always find it helpful to track the statistics of the index and to list all the documents with their IDs (these IDs are automatically generated by Marqo).

To list all the documents currently in your index, run:
```bash
python3 marqo/list_all_documents.py
```

To obtain index statistics, run:
```bash
python3 marqo/get_stats.py
```

## Step 5: Begin Searching
You can begin searching even while your documents are being added. Note, the more documents in your index, the better the search results will be. 

For searching, we use Streamlit as the UI and use the search feature in Marqo. If you want to experiment with just Marqo search without the UI, you can run `python3 marqo/test_search.py` which will perform a simple search. 

To run the UI, 
```bash
streamlit run app.py
```

This will launch the user interface ready for you to perform searches!

## Step 6: Clean Up
If you follow the steps in this guide, you will create an index with GPU inference and a basic storage shard. This index will cost $1.03 per hour. When you are done with the index you can delete it with the following code:
```bash
python3 marqo/delete_index.py
```

**If you do not delete your index you will continue to be charged for it.**

## Questions? Contact Us!
If you have any questions about this search demo or about Marqo's capabilities, you can:
* [Join Our Slack Community](https://join.slack.com/t/marqo-community/shared_invite/zt-2ry33y71j-H0WUeQvFaVlKuuZwl38BeA)
* [Book a Demo](https://www.marqo.ai/book-demo?utm_source=github&utm_medium=organic&utm_campaign=marqo-ai&utm_term=2024-11-07-04-36-utc)