import requests
import json
import os

# 1. تعريف الرابط ونقطة النهاية
API_URL = "http://127.0.0.1:8000/predict"

# 2. تحديد مسار ملف الصورة
IMAGE_FILE_PATH = "C:\\Users\\Admin\\motmaen_api\\tested\\aug_0_3042.jpg"  

# 3. إعداد البيانات التي سيتم إرسالها
data = {
    'portion_size': '150'  # حجم الحصة بالجرام
}

try:
    # 💥 قراءة ملف الصورة كـ Bytes مباشرة
    with open(IMAGE_FILE_PATH, 'rb') as f:
        image_bytes = f.read()

    files = {
        'file': (os.path.basename(IMAGE_FILE_PATH), image_bytes, 'image/jpeg')
    }

    # 4. إرسال طلب POST
    print(f"Sending POST request to: {API_URL} with image: {os.path.basename(IMAGE_FILE_PATH)}")
    response = requests.post(API_URL, files=files, data=data)
    
    # 5. طباعة الرد
    print("--- API Response ---")
    
    # التحقق من أن الرد كان ناجحاً (كود 200)
    if response.status_code == 200:
        # تنسيق وطباعة الرد JSON
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    else:
        # طباعة رسالة الخطأ في حالة فشل الطلب
        print(f"Error Code: {response.status_code}")
        print(f"Error Details: {response.text}")

except FileNotFoundError:
    print(f"ERROR: Image file not found at {IMAGE_FILE_PATH}. Please check the path.")
except requests.exceptions.RequestException as e:
    print(f"An error occurred while connecting to the API: {e}")