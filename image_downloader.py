
# Code By : Atul Kushwaha || Chat GPT
import os
import requests
from tqdm import tqdm

# Pixabay API Key (Replace with your valid key)
API_KEY = 'YOUR_PIXABAY_API_KEY'

# Configuration
SEARCH_QUERY = "Nature"   # Change this to any topic you like
TOTAL_IMAGES = 3          # Number of images to fetch

# Orientation options
ORIENTATION = 'landscape'   # Common choice
# ORIENTATION = 'portrait'
# ORIENTATION = 'all'

# Folder to save images
SAVE_FOLDER = "output"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Pixabay API URL
url = (
    f'https://pixabay.com/api/?key={API_KEY}'
    f'&q={SEARCH_QUERY}&image_type=photo&orientation={ORIENTATION}'
    f'&per_page={TOTAL_IMAGES}&safesearch=true'
)

# Fetch and download images
response = requests.get(url)
if response.status_code == 200:
    data = response.json()

    if not data['hits']:
        print("⚠️ No images found for your search.")
    else:
        print(f"\n🔍 Found {len(data['hits'])} images for '{SEARCH_QUERY}' ({ORIENTATION}). Downloading...\n")
        for i, hit in enumerate(tqdm(data['hits'], desc=f'Downloading {SEARCH_QUERY}')):
            image_url = hit.get('largeImageURL')
            if not image_url:
                continue

            file_name = os.path.join(SAVE_FOLDER, f'{SEARCH_QUERY.replace(' ', '_').lower()}_{i+1}.jpg')
            try:
                image_data = requests.get(image_url).content
                with open(file_name, 'wb') as f:
                    f.write(image_data)
            except Exception as e:
                print(f"❌ Failed to download image {i+1}: {e}")

        print(f"\n✅ Successfully downloaded {len(data['hits'])} images for '{SEARCH_QUERY}'.")
else:
    print(f"❌ Error: {response.status_code}")

print("\n🎉 Download complete.")
