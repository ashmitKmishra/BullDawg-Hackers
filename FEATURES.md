Project consolidation status

This branch now runs a single Flask app with:
- Backend: main.py, adaptive_questionnaire_engine.py, pdf_report_generator.py
- UI: templates/index.html (vanilla JS/CSS)
- Tests: tests/

Pending cleanup candidates (to be removed if not used):
- package.json, package-lock.json, server.js, src/ (React), api/, netlify.toml, vercel.json

After confirmation, we will remove these to minimize file count and keep a Python-only repo.
# Feature Overview

## Core Features

### 🧠 Adaptive Questioning Engine
- **Smart Question Selection**: Uses entropy-based algorithms to select the most informative questions
- **Dynamic Scoring**: Real-time benefit scoring based on user responses
- **Efficient Stopping**: Automatically stops when sufficient information is gathered

### 🤖 Machine Learning Models
- **Multi-Model Ensemble**: XGBoost, LightGBM, and CatBoost for robust predictions
- **Feature Engineering**: Advanced feature extraction from user demographics and responses
- **Continuous Learning**: Models can be retrained with new data

### 📊 Risk Assessment
- **Multi-Dimensional Analysis**: Financial, health, family, career, and retirement risks
- **Personalized Scoring**: Risk levels tailored to individual circumstances
- **Actionable Insights**: Clear explanations and recommendations for each risk area

### 📄 PDF Report Generation
- **Professional Design**: Clean, burgundy-themed reports
- **Comprehensive Content**: Full benefit analysis, risk assessment, and recommendations
- **Downloadable**: Users can save and share their personalized reports

### 🎯 Benefit Recommendations
- **Personalized Scoring**: Each benefit scored 0-100 based on user profile
- **Priority Classification**: Critical, High, Medium, Low priority levels
- **Detailed Rationale**: Clear explanations for why each benefit is recommended
- **Cost Information**: Typical cost ranges and coverage details

## Technical Features

### 🔧 Backend Architecture
- **Flask Framework**: Lightweight, scalable web framework
- **RESTful API**: Clean API endpoints for frontend integration
- **Session Management**: Secure session handling for questionnaire state
- **Database Integration**: Optional Supabase integration for benefit data

### 🎨 Frontend Interface
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Interactive UI**: Smooth animations and user-friendly interface
- **Progress Tracking**: Visual progress indicators and question rationale
- **Accessibility**: WCAG compliant design for all users

### 🧪 Testing & Quality
- **Comprehensive Test Suite**: Unit tests, integration tests, and functional tests
- **Model Validation**: Cross-validation and performance metrics
- **Error Handling**: Graceful error handling and user feedback
- **Code Quality**: Clean, documented, maintainable code

## Supported Benefits

### Insurance & Protection
- Medical Insurance
- Dental Insurance
- Vision Insurance
- Life Insurance
- Disability Insurance
- Pet Insurance

### Financial & Retirement
- 401(k) Plans
- Health Savings Account (HSA)
- Healthcare FSA
- Dependent Care FSA
- Student Loan Repayment

### Wellness & Development
- Mental Health Stipend
- Learning & Development Stipend
- Remote Work Stipend
- Sabbatical Programs

## Future Enhancements

- Real-time chat integration
- Mobile app development
- Advanced analytics dashboard
- Integration with HR systems
- Multi-language support