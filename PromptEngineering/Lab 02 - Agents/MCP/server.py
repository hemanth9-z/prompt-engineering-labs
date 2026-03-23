from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# -------------------------------
# Tool 1: BMI
# -------------------------------
class BMIInput(BaseModel):
    weight: float
    height: float

@app.post("/calculate_bmi")
def calculate_bmi(data: BMIInput):
    bmi = data.weight / (data.height ** 2)
    
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return {
        "bmi": round(bmi, 2),
        "category": category
    }

# -------------------------------
# Tool 2: Credit Score
# -------------------------------
class CreditInput(BaseModel):
    user_id: str

@app.post("/get_credit_score")
def get_credit_score(data: CreditInput):
    # fake database
    fake_scores = {
        "123": 780,
        "456": 650,
        "789": 720
    }

    score = fake_scores.get(data.user_id, 600)

    return {
        "credit_score": score
    }