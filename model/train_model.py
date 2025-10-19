"""
Model Training Script for Adaptive Benefit Questionnaire

This script trains the recommendation model using demographic, financial, and questionnaire response data.
"""

import pickle
from adaptive_questionnaire_engine import UserDemographics, UserFinancials, Question, BenefitType
import numpy as np

# Placeholder: Load your real data here
# For demonstration, we use a small sample
train_data = [
    {
        "demographics": UserDemographics(name="Alice", age=29, gender="Female", location="CA", zip_code="90001", marital_status="single", num_children=0),
        "financials": UserFinancials(annual_income=85000, monthly_expenses=3200, total_debt=15000, savings=20000, investment_accounts=10000, spending_categories={"housing": 1800, "food": 600}, income_volatility=0.05),
        "answers": ["A", "B", "A", "B", "A"]
    },
    {
        "demographics": UserDemographics(name="Bob", age=45, gender="Male", location="NY", zip_code="10001", marital_status="married", num_children=2),
        "financials": UserFinancials(annual_income=120000, monthly_expenses=5000, total_debt=40000, savings=50000, investment_accounts=40000, spending_categories={"housing": 2500, "food": 900}, income_volatility=0.08),
        "answers": ["B", "B", "A", "A", "B"]
    }
]

# Example: Simple scoring model (replace with your actual ML model)
def train_model(data):
    # Aggregate scores by benefit type
    benefit_scores = {b: [] for b in BenefitType}
    for entry in data:
        # Example: Score medical higher for older users
        score = 50 + entry["demographics"].age // 2
        benefit_scores[BenefitType.MEDICAL].append(score)
    # Compute average scores
    avg_scores = {b: np.mean(scores) if scores else 0 for b, scores in benefit_scores.items()}
    return avg_scores

if __name__ == "__main__":
    model = train_model(train_data)
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)
    print("Model trained and saved as model.pkl")
