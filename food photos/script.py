from serpapi import GoogleSearch
import requests, os, math
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")

print(f"API Key found: {'Yes' if API_KEY else 'No'}")
if not API_KEY:
    print("ERROR: API_KEY environment variable is not set!")
    print("Please set your SerpAPI key: set API_KEY=your_api_key_here")
    exit(1)

def download_images(query, total_count=100, folder="food photos"):
    os.makedirs(folder, exist_ok=True)
    per_page = 50
    pages = math.ceil(total_count / per_page)
    img_num = 0

    for page in range(pages):
        search = GoogleSearch({
            "q": query,
            "tbm": "isch",
            "ijn": str(page),
            "api_key": API_KEY
        })
        results = search.get_dict()
        images = results.get("images_results", [])
        
        for img in images:
            if img_num >= total_count:
                break
            try:
                url = img["original"]
                response = requests.get(url, timeout=10)
                image = Image.open(BytesIO(response.content))  # نحاول نفتح الصورة
                image.save(f"{folder}/{query}_{img_num}.jpg")   # نخزنها كـ jpg
                print(f"✅ Saved: {query}_{img_num}.jpg")
                img_num += 1
            except Exception as e:
                print(f"❌ Skipped broken image ({url}):", e)

# مثال: 100 صورة كشري
download_images("فول مدمس مصري", total_count=100, folder="Fool")
