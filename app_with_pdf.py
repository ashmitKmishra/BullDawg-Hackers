"""
Flask Backend for Adaptive Questionnaire with PDF Generation
Provides REST API for interactive questioning and comprehensive PDF reports
"""

from flask import Flask, render_template, request, jsonify, session, send_file
import secrets
import os
from adaptive_questionnaire_engine import (
    AdaptiveQuestionnaireEngine,
    UserDemographics,
    UserFinancials
)
from pdf_report_generator import BenefitReportGenerator, calculate_risk_assessment

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Store active sessions in memory (use Redis/DB in production)
sessions = {}


def _convert_profile_types(profile: dict) -> dict:
    p = dict(profile)
    try:
        if 'age' in p:
            p['age'] = int(p['age']) if p['age'] else 0
        if 'annual_income' in p:
            p['annual_income'] = float(p['annual_income']) if p['annual_income'] else 0.0
        if 'monthly_expenses' in p:
            p['monthly_expenses'] = float(p['monthly_expenses']) if p['monthly_expenses'] else 0.0
        if 'total_debt' in p:
            p['total_debt'] = float(p['total_debt']) if p['total_debt'] else 0.0
        if 'savings' in p:
            p['savings'] = float(p['savings']) if p['savings'] else 0.0
        if 'num_children' in p:
            p['num_children'] = int(p['num_children']) if p['num_children'] else 0
    except Exception:
        pass
    return p


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
        'financials': financials,
        'user_profile': data,  # Store for PDF generation
        'answers': []  # Track all answers
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
            'why': rationale
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
    
    # Store answer for PDF
    question_id = data.get('question_id')
    sessions[session_id]['answers'].append({
        'question_id': question_id,
        'choice': choice
    })
    
    # Get the question from history or find it
    question = next(q for q in engine.question_bank if q.id == question_id)
    
    engine.process_answer(question, choice)
    
    # Check if we should stop
    if engine.should_stop():
        # Generate recommendations
        recommendations = engine.generate_recommendations()
        
        # Store recommendations for PDF
        sessions[session_id]['recommendations'] = recommendations
        
        # Compute risk assessment for results page
        user_profile_raw = sessions[session_id].get('user_profile', {})
        user_profile_converted = _convert_profile_types(user_profile_raw)
        risk_assessment = calculate_risk_assessment(user_profile_converted, sessions[session_id].get('answers', []))

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
                for rec in recommendations[:15]  # Top 15
            ],
            'progress': {
                'questions_asked': len(engine.questions_asked),
                'total_questions': len(engine.question_bank),
                'entropy': round(engine.calculate_entropy(engine.benefit_scores), 2)
            },
            'session_id': session_id,  # Return for PDF download
            'risk_assessment': risk_assessment
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
            'why': rationale
        },
        'progress': {
            'questions_asked': len(engine.questions_asked),
            'total_questions': len(engine.question_bank),
            'entropy': round(engine.calculate_entropy(engine.benefit_scores), 2)
        }
    })


@app.route('/api/generate-pdf/<session_id>', methods=['GET'])
def generate_pdf_report(session_id):
    """Generate and download PDF report"""
    
    if session_id not in sessions:
        return jsonify({'error': 'Invalid session'}), 400
    
    session_data = sessions[session_id]
    user_profile = session_data.get('user_profile', {})
    recommendations = session_data.get('recommendations', [])
    answers = session_data.get('answers', [])
    
    # Convert recommendations to dict format
    recs_dict = [
        {
            'benefit_type': rec.benefit_type.value,  # Changed from 'benefit' to 'benefit_type'
            'score': rec.score,
            'priority': rec.priority,
            'confidence': rec.confidence,
            'rationale': rec.rationale,
            'details': rec.details
        }
        for rec in recommendations
    ]
    
    # Convert string values to proper types in user_profile
    user_profile_converted = user_profile.copy()
    if 'age' in user_profile_converted:
        user_profile_converted['age'] = int(user_profile_converted['age']) if user_profile_converted['age'] else 30
    if 'annual_income' in user_profile_converted:
        user_profile_converted['annual_income'] = float(user_profile_converted['annual_income']) if user_profile_converted['annual_income'] else 0
    if 'monthly_expenses' in user_profile_converted:
        user_profile_converted['monthly_expenses'] = float(user_profile_converted['monthly_expenses']) if user_profile_converted['monthly_expenses'] else 0
    if 'total_debt' in user_profile_converted:
        user_profile_converted['total_debt'] = float(user_profile_converted['total_debt']) if user_profile_converted['total_debt'] else 0
    if 'savings' in user_profile_converted:
        user_profile_converted['savings'] = float(user_profile_converted['savings']) if user_profile_converted['savings'] else 0
    if 'num_children' in user_profile_converted:
        user_profile_converted['num_children'] = int(user_profile_converted['num_children']) if user_profile_converted['num_children'] else 0
    
    # Calculate risk assessment
    risk_assessment = calculate_risk_assessment(user_profile_converted, answers)
    
    # Generate PDF
    pdf_generator = BenefitReportGenerator()
    
    # Create reports directory if it doesn't exist
    os.makedirs('reports', exist_ok=True)
    
    # Generate unique filename
    filename = f"benefit_report_{session_id}.pdf"
    filepath = os.path.join('reports', filename)
    
    # Enrich answers with question text and selected label for PDF
    answered_qas = []
    try:
        engine = session_data.get('engine')
        bank = getattr(engine, 'question_bank', []) if engine else []
        qmap = {q.id: q for q in bank}
        for a in answers:
            qid = a.get('question_id')
            choice_idx = a.get('choice')
            q = qmap.get(qid)
            if q:
                label = q.choice_a if int(choice_idx) == 0 else q.choice_b
                answered_qas.append({
                    'id': qid,
                    'text': q.text,
                    'answer': label
                })
    except Exception:
        answered_qas = []

    pdf_generator.generate_report(user_profile_converted, recs_dict, risk_assessment, filepath, answered_questions=answered_qas)
    
    # Send file for download
    return send_file(
        filepath,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"Benefit_Assessment_Report_{user_profile.get('name', 'User').replace(' ', '_')}.pdf"
    )


if __name__ == '__main__':
    print("\n" + "="*70)
    print("Benefit Questionnaire with PDF Reports")
    print("="*70)
    print("\nFeatures:")
    print("  • Adaptive questioning (8–12 questions)")
    print("  • Accurate recommendations")
    print("  • Comprehensive PDF reports with risk assessment")
    print("  • Supabase integration for benefit details")
    print("\nOpen your browser to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    
    # Create reports directory
    os.makedirs('reports', exist_ok=True)
    
    app.run(debug=True, port=5000)
