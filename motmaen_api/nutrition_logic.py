import json

class NutritionExpert:
    def __init__(self):
        # قاعدة بيانات الأكلات المستخرجة من ملف Excel الخاص بك
        self.food_db = {
            "Fattah": {"std_serving_g": 238, "std_carbs_g": 71.4, "gi": 73},
            "Fool": {"std_serving_g": 170, "std_carbs_g": 17, "gi": 79},
            "Hawawshy": {"std_serving_g": 150, "std_carbs_g": 30, "gi": 75},
            "Koshari": {"std_serving_g": 426, "std_carbs_g": 52, "gi": 60},
            "Kunafa": {"std_serving_g": 120, "std_carbs_g": 55, "gi": 75},
            "Mahshy El Kosa": {"std_serving_g": 200, "std_carbs_g": 30, "gi": 60},
            "Ptata": {"std_serving_g": 150, "std_carbs_g": 26, "gi": 78},
            "Taameya": {"std_serving_g": 100, "std_carbs_g": 21, "gi": 40},
            "Umm Ali": {"std_serving_g": 150, "std_carbs_g": 45, "gi": 70}
        }

    def calculate_health_status(self, gl):
        if gl <= 10:
            return "Suitable (Safe)", "Recommended"
        elif 11 <= gl <= 19:
            return "Moderate (Caution)", "Eat in moderation"
        else:
            return "Not Suitable (High Risk)", "Avoid or limit portion"

    def analyze_meal(self, label, user_portion_g=None):
        if label not in self.food_db:
            return None

        data = self.food_db[label]
        
        portion_size = float(user_portion_g) if user_portion_g else data["std_serving_g"]
        
        # حساب الكربوهيدرات الجديدة
        carbs_per_gram = data["std_carbs_g"] / data["std_serving_g"]
        calculated_carbs = round(carbs_per_gram * portion_size, 1)
        
        # حساب الحمل الجلايسيمي (GL)
        gi = data["gi"]
        gl = round((calculated_carbs * gi) / 100, 1)
        
        # تحديد الحالة الصحية
        health_status, recommendation = self.calculate_health_status(gl)
        
        recommended_portion_msg = f"{portion_size}g"
        if gl >= 20:
            # حساب الحصة الآمنة (التي تجعل الـ GL حوالي 10)
            safe_portion = int((10 * 100) / (carbs_per_gram * gi))
            recommended_portion_msg = f"Reduce to {safe_portion}g for safety"

        return {
            "label": label,
            "portion_size_g": portion_size,
            "carbs": calculated_carbs,
            "gi": gi,
            "gl": gl,
            "health_status": health_status,
            "recommendation": recommendation,
            "recommended_portion_advice": recommended_portion_msg
        }