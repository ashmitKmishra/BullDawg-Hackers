# ML Model Transition Plan - 99%+ Accuracy Goal

## Current State
- Information Theory + Bayesian approach
- Rule-based correlations
- 41 hardcoded questions with manual correlation matrices

## Target State
- Machine Learning model (Random Forest / XGBoost / Neural Network)
- Trained on real benefit selection data
- 99%+ accuracy in benefit recommendations
- Adaptive questioning using uncertainty sampling

## Architecture

### 1. Data Layer
- **Synthetic Training Data Generator** (initially, until we get real data)
  - Generate 10,000+ realistic user profiles
  - Simulate benefit selections based on logical rules
  - Add noise for realism

### 2. ML Model Layer
- **Primary Model**: XGBoost Classifier (best for tabular data)
- **Alternative**: Random Forest (fallback)
- **Features**:
  - Demographics (age, marital status, children, location)
  - Financial (income, debt, savings, expenses)
  - Behavioral (from questionnaire answers)
  - Derived features (debt-to-income ratio, savings rate, etc.)

### 3. Active Learning for Questions
- **Uncertainty Sampling**: Ask questions that reduce model uncertainty
- **Expected Model Change**: Questions that would most change predictions
- **Query by Committee**: Ensemble disagreement on answers

### 4. Benefits to Predict (Multi-label Classification)
- Medical, Dental, Vision
- Life Insurance, Disability
- 401k, HSA, FSA
- Critical Illness, Accident Insurance
- Legal Services, Identity Theft Protection
- etc. (18 total benefit types)

## Implementation Steps

### Phase 1: Data Generation (TODAY)
1. Create synthetic data generator
2. Generate 10,000 training samples
3. Split: 70% train, 15% validation, 15% test

### Phase 2: Model Training (TODAY)
1. Feature engineering
2. Train XGBoost multi-label classifier
3. Hyperparameter tuning
4. Achieve 99%+ accuracy on test set

### Phase 3: Active Learning Integration (TODAY)
1. Implement uncertainty-based question selection
2. Replace information gain with model uncertainty
3. Stop when all benefit predictions have >95% confidence

### Phase 4: Production Integration (NEXT)
1. Replace adaptive_questionnaire_engine.py
2. Update Flask API
3. Keep existing UI
4. Add model versioning

## Files to Keep
- ✅ app.py (Flask API)
- ✅ templates/index.html (UI)
- ✅ requirements.txt (update with ML libs)
- ✅ tests/ (rewrite for ML model)

## Files to Delete/Archive
- ❌ adaptive_questioning_algorithm.md (old approach)
- ❌ ALL_QUESTIONS.md (manual questions)
- ❌ QUESTION_BANK.md (manual correlations)
- ❌ demo_dynamic.py, demo_dynamic_v2.py (demos for old system)
- ❌ sample_output.txt (old output)
- ❌ adaptive_questionnaire_engine.py (replace with ML version)
- ❌ src/, public/, index.html, package.json, vite.config.js (React/Vite not used)

## Success Metrics
- ✅ 99%+ accuracy on test set
- ✅ 95%+ precision per benefit type
- ✅ <10 questions average to reach 99% confidence
- ✅ Handles edge cases gracefully

## Tech Stack
- **ML**: XGBoost, scikit-learn
- **Data**: pandas, numpy
- **Serialization**: joblib (model persistence)
- **API**: Flask (existing)
- **Frontend**: Vanilla JS (existing)

Let's build this! 🚀
