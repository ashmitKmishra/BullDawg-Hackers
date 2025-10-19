"""
Flask Backend for Adaptive Questionnaire
Provides REST API for interactive questioning
"""

from flask import Flask, render_template, request, jsonify, session
import secrets
from adaptive_questionnaire_engine import (
    AdaptiveQuestionnaireEngine,
    UserDemographics,
    UserFinancials
)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Store active sessions in memory (use Redis/DB in production)
sessions = {}


@app.route('/')
def index():
    """Serve the main questionnaire page"""
    return render_template('index.html')


@app.route('/api/start', methods=['POST'])
def start_questionnaire():
    """Initialize a new questionnaire session"""
    data = request.json
    
    # Get user profile
    demographics = UserDemographics(
        name=data.get('name', 'User'),
        age=int(data.get('age', 30)),
        gender=data.get('gender'),
        marital_status=data.get('marital_status', 'single'),
        num_children=int(data.get('num_children', 0))
    )
    
    financials = UserFinancials(
        annual_income=float(data.get('annual_income', 50000)),
        monthly_expenses=float(data.get('monthly_expenses', 3000)),
        total_debt=float(data.get('total_debt', 0)),
        savings=float(data.get('savings', 10000)),
        investment_accounts=float(data.get('investment_accounts', 0))
    )
    
    # Create engine
    engine = AdaptiveQuestionnaireEngine(demographics, financials)
    
    # Store in session
    session_id = secrets.token_urlsafe(16)
    sessions[session_id] = {
        'engine': engine,
        'demographics': demographics,
        'financials': financials
    }
    
    # Get first question
    question = engine.select_next_question()
    
    # Get rationale if available
    rationale = getattr(question, 'selection_rationale', None)
    
    return jsonify({
        'session_id': session_id,
        'question': {
            'id': question.id,
            'text': question.text,
            'choices': [question.choice_a, question.choice_b],
            'why': rationale  # NEW: Show why this question was selected
        },
        'progress': {
            'questions_asked': len(engine.questions_asked),
            'total_questions': len(engine.question_bank),
            'entropy': round(engine.calculate_entropy(engine.benefit_scores), 2)
        }
    })


@app.route('/api/answer', methods=['POST'])
def submit_answer():
    """Process an answer and get next question"""
    data = request.json
    session_id = data.get('session_id')
    choice = int(data.get('choice'))  # 0 or 1
    
    if session_id not in sessions:
        return jsonify({'error': 'Invalid session'}), 400
    
    engine = sessions[session_id]['engine']
    
    # Process the answer
    current_question = engine.questions_asked[-1] if engine.questions_asked else engine.question_bank[0]
    # Get the question from history or find it
    question_id = data.get('question_id')
    question = next(q for q in engine.question_bank if q.id == question_id)
    
    engine.process_answer(question, choice)
    
    # Check if we should stop
    if engine.should_stop():
        # Generate recommendations
        recommendations = engine.generate_recommendations()
        
        return jsonify({
            'complete': True,
            'recommendations': [
                {
                    'benefit': rec.benefit_type.value,
                    'score': rec.score,
                    'priority': rec.priority,
                    'confidence': rec.confidence,
                    'rationale': rec.rationale,
                    'details': rec.details
                }
                for rec in recommendations[:10]  # Top 10
            ],
            'progress': {
                'questions_asked': len(engine.questions_asked),
                'total_questions': len(engine.question_bank),
                'entropy': round(engine.calculate_entropy(engine.benefit_scores), 2)
            }
        })
    
    # Get next question
    next_question = engine.select_next_question()
    
    # Get rationale if available
    rationale = getattr(next_question, 'selection_rationale', None)
    
    return jsonify({
        'complete': False,
        'question': {
            'id': next_question.id,
            'text': next_question.text,
            'choices': [next_question.choice_a, next_question.choice_b],
            'why': rationale  # NEW: Show why this question was selected
        },
        'progress': {
            'questions_asked': len(engine.questions_asked),
            'total_questions': len(engine.question_bank),
            'entropy': round(engine.calculate_entropy(engine.benefit_scores), 2)
        }
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Adaptive Benefit Questionnaire - Interactive Demo")
    print("="*60)
    print("\n👉 Open your browser to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    app.run(debug=True, port=5000)
