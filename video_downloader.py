
# Code By : Atul Kushwaha || Chat GPT
import os
import requests
from tqdm import tqdm

# Pixabay API Key (replace with your valid key)
API_KEY = 'YOUR_PIXABAY_API_KEY'

# Configuration
SEARCH_QUERY = "Nature"     # Topic
TOTAL_VIDEOS = 3            # Number of videos to fetch
VIDEO_QUALITY = 'medium'    # 'large', 'medium', 'small'

# Folder to save videos
SAVE_FOLDER = "videos"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Pixabay Video API URL (orientation not supported for videos)
url = (
    f'https://pixabay.com/api/videos/?key={API_KEY}'
    f'&q={SEARCH_QUERY}'
    f'&per_page={TOTAL_VIDEOS}'
    f'&safesearch=true'
)

# Fetch video metadata
response = requests.get(url)
if response.status_code == 200:
    data = response.json()

    if not data.get('hits'):
        print(f"⚠️ No videos found for '{SEARCH_QUERY}'.")
    else:
        print(f"\\n🎬 Found {len(data['hits'])} videos for '{SEARCH_QUERY}'. Downloading...\\n")

        for i, hit in enumerate(tqdm(data['hits'], desc=f'Downloading {SEARCH_QUERY}')):
            videos = hit.get('videos', {})
            video_url = videos.get(VIDEO_QUALITY, {}).get('url')

            if not video_url:
                print(f"⚠️ No '{VIDEO_QUALITY}' quality video available for item {i+1}. Skipping.")
                continue

            file_name = os.path.join(SAVE_FOLDER, f"{SEARCH_QUERY.replace(' ', '_').lower()}_{i+1}.mp4")

            try:
                with requests.get(video_url, stream=True) as r:
                    r.raise_for_status()
                    total_size = int(r.headers.get('content-length', 0))

                    with open(file_name, 'wb') as f:
                        for chunk in tqdm(r.iter_content(1024), total=total_size // 1024, unit='KB', leave=False):
                            f.write(chunk)

                print(f"✅ Downloaded: {file_name}")
            except Exception as e:
                print(f"❌ Failed to download video {i+1}: {e}")

        print(f"\\n✅ Successfully downloaded {len(data['hits'])} videos for '{SEARCH_QUERY}'.")
else:
    print(f"❌ Error fetching data: {response.status_code}")

print("\\n🎉 Download complete.")
