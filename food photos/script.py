from serpapi import GoogleSearch
import requests, os, math
from PIL import Image
from io import BytesIO

API_KEY = "e73933c535219f44a1fee0c07a49e4c398d0f5d2f299beb2e8a300b29106cb98"

def download_images(query, total_count=100, folder="food photo"):
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
download_images("الطعمية المصرية", total_count=100, folder="Taameya")
