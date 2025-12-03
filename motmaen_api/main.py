import os
import sys
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
import uvicorn
from io import BytesIO
from PIL import Image
import numpy as np
import json
import tensorflow.lite as tflite 
from typing import Optional
from tensorflow.keras.applications.densenet import preprocess_input 

from nutrition_logic import NutritionExpert

app = FastAPI(title="Motmaen AI API", version="1.0")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.tflite")
LABELS_PATH = os.path.join(BASE_DIR, "labels.json")

print(f"📂 Looking for model at: {MODEL_PATH}")

try:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    
    with open(MODEL_PATH, 'rb') as f:
        model_content = f.read()

    interpreter = tflite.Interpreter(model_content=model_content)
    
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    if os.path.exists(LABELS_PATH):
        with open(LABELS_PATH, "r") as f:
            labels_map = json.load(f)
            labels = {int(k): v for k, v in labels_map.items()}
    else:
        print("⚠️ Warning: labels.json not found. Predictions will be numbers only.")
        labels = {}
        
    expert = NutritionExpert()
    print("✅ Model & Nutrition Expert Loaded Successfully.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    interpreter = None 


def process_image(image_bytes):
    img = Image.open(BytesIO(image_bytes)).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img, dtype=np.float32)
    
    img_array = preprocess_input(img_array)
    
    img_array = np.expand_dims(img_array, axis=0) 
    return img_array

@app.get("/")
def home():
    return {"message": "Motmaen API is running..."}

@app.post("/predict")
async def predict(
    file: UploadFile = File(...), 
    portion_size: Optional[float] = Form(None)
):
    if interpreter is None:
        return JSONResponse(status_code=500, content={"error": "Model not loaded on server."})

    try:
        image_bytes = await file.read()
        input_data = process_image(image_bytes)

        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        
        prediction_idx = np.argmax(output_data)
        confidence = float(np.max(output_data))
        predicted_label = labels.get(prediction_idx, "Unknown")

        # 💥 التعديل الحاسم: خفض الحد الأدنى للثقة إلى 0.01 (1%)
        if confidence < 0.01:
             return JSONResponse(content={"error": "Unrecognized food or low confidence", "confidence": round(confidence, 2)})

        nutrition_info = expert.analyze_meal(predicted_label, portion_size)

        if not nutrition_info:
            return JSONResponse(content={
                "prediction": predicted_label,
                "confidence": round(confidence, 2),
                "error": "Nutritional data not found for this item"
            })

        return {
            "prediction": predicted_label,
            "confidence": round(confidence, 2),
            "input_portion_g": nutrition_info['portion_size_g'],
            "carbs": nutrition_info['carbs'],
            "gi": nutrition_info['gi'],
            "gl": nutrition_info['gl'],
            "status": nutrition_info['health_status'],
            "recommendation": nutrition_info['recommendation'],
            "advice": nutrition_info['recommended_portion_advice']
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"An unexpected error occurred during prediction: {str(e)}"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)