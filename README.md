# Motmaen | مُـطـمئِـن
<p align="center">
  <img src="assets/imgs/banner.png" alt="Motmaen AI Banner" width="100%" />
</p>

## 🚀 Overview

Motmaen AI is a deep-learning powered **Egyptian food image classification model** trained on a large, curated dataset of 10+ famous Egyptian dishes.
This model is part of the wider **Motmaen** ecosystem — a smart health assistant designed to support diabetic and chronic-disease patients by guiding nutrition choices with food recognition, personalized feedback, and future API integrations.

This repository contains:

* The **full dataset** (train/valid/test splits)
* The **entire training pipeline** (EDA, preprocessing, augmentation, training notebooks)
* The **final Keras model** and **TensorFlow Lite model** for deployment
* Scripts for exporting, predicting, and future API usage
* [Our Presentation](https://www.canva.com/design/DAG2iOg2Aig/3zS1O5Iuy0ErtlQO9XhvDA/edit?utm_content=DAG2iOg2Aig&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
* [Demo Video](https://drive.google.com/file/d/1wItbhkH81M8Mwk08QXbhkX_xCFkQmEi_/view?usp=sharing)

---

## 📁 Repository Structure

```
motmaen-ai/
├── Models/                # Final trained models
│   ├── best_final.keras
│   ├── final_model.tflite
│   ├── fine_tuned_model.keras
│   ├── labels.txt
│   └── model_tflit_script (old).py
│
├── code/                  # Training & analysis notebooks
│   ├── EDA.ipynb
│   ├── motmaen-final-model.ipynb
│   └── script.py
│
├── food photos/           # The processed dataset (train/valid/test)
│   ├── train/
│   ├── test/
│   └── valid/
│
├── GI_Table.xlsx          # Nutritional table per food class
└── README.md
```

The repo also contains earlier raw datasets under `/droped images/` for transparency and reproducibility.

---

# 🍲 Supported Food Classes

The model currently recognizes the following Egyptian dishes:

* **Fattah (فتة)**
* **Fool Medames (فول)**
* **Hawawshy (حواوشي)**
* **Koshari (كشري)**
* **Kunafa (كنافة)**
* **Mahshy El Kosa (محشي كوسة)**
* **Roz Bel Laban (رز بلبن / Rice Pudding)**
* **Taameya (طعمية / Falafel)**
* **Umm Ali (أم علي)**
* **Baked Sweet Potato (بطاطا)**

Dataset size after cleaning & augmentation exceeds **15,000 images**.

---

# 🧠 Model Architecture

The final model is based on:

* **MobileNetV2** (pretrained on ImageNet)
* **Custom dense layers** optimized for 10-class classification
* **Mixed-precision training** for performance
* **Data augmentation** pipeline (rotation, flip, brightness, zoom, hue shifts, etc.)

The exported `.tflite` file is optimized for:

* Mobile CPUs
* Real-time inference
* Low latency (<30ms on mid-range phones)

---

# 📊 Training Pipeline

The full pipeline is available in:

* `code/EDA.ipynb` – dataset analysis, cleaning, visualization
* `code/motmaen-final-model.ipynb` – model building, training, evaluation
* `script.py` – utilities for exporting & predicting

Key steps:

1. **Dataset Cleaning & Deduplication**
2. **Train/Valid/Test Splits**
3. **Image Augmentation**
4. **Transfer Learning + Fine Tuning**
5. **Evaluation (Accuracy, Confusion Matrix, F1)**
6. **TFLite Quantization (Float16)**

Accuracy achieved:

> ⭐ **~92% Top-1 Accuracy** on the final validation set.

---

# 📦 How to Use

### 1️⃣ Install dependencies

```bash
pip install tensorflow matplotlib numpy pillow
```

### 2️⃣ Load the TFLite model

```python
import tensorflow as tf
import numpy as np
from PIL import Image

interpreter = tf.lite.Interpreter(model_path="Models/final_model.tflite")
interpreter.allocate_tensors()

# Get input-output layers
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
```

### 3️⃣ Make a prediction

```python
img = Image.open("test_image.jpg").resize((224,224))
img = np.array(img, dtype=np.float32) / 255.0
img = np.expand_dims(img, 0)

interpreter.set_tensor(input_details[0]['index'], img)
interpreter.invoke()

prediction = interpreter.get_tensor(output_details[0]['index'])
print("Predicted class:", np.argmax(prediction))
```

---

# 🧩 How This Fits in the Motmaen Ecosystem

Motmaen is a larger unified platform designed to support:

### 🌐 **Future API (Planned)**

* /predict (upload food image → return prediction)
* /nutrition (link prediction → nutritional table)
* /profile recommendations (personalized diabetic guidance)

### 📱 **Mobile App (Planned)**

Food scanning → Nutrition estimation → Dietary advice → Progress tracking.

This repo provides the **vision foundation**: a reliable, optimized, deployable food recognition model.

---

# 🔮 Future Work

* Expand dataset to **30+ Egyptian dishes**
* Add calorie estimation & portion size detection
* Full FastAPI backend
* Mobile inference benchmarks (Android/iOS)
* Add ONNX export
* Model pruning for ultra-low-power devices

---

# 🙌 Contributors

* [Mohamed Geweida](https://www.github/mohamed-geweida/)
* [Eman Elnaggar](https://github.com/Eman-elnagggar)
* [Sohaila Mohamed](https://github.com/sohailamohamed15)
* [Shams Goda](https://github.com/usernameee111)
* [Noureen Ibrahim](https://github.com/noureen-156)
---

# 📜 License

This project is released under the **MIT License**.

---

# ⭐ Want to Support the Project?

Give the repo a **star** ⭐ on GitHub — it really helps with visibility as Motmaen grows into a full health assistant!

Just tell me!
