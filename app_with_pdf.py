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
"""
PDF generation and risk assessment are inlined below to consolidate files.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# Burgundy color theme for PDF
BURGUNDY = colors.HexColor('#6b0f1a')
DARK_BURGUNDY = colors.HexColor('#4a0a11')

class BenefitReportGenerator:
    """Generate comprehensive PDF reports with benefit recommendations"""
    def __init__(self):
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        try:
            self.supabase = create_client(supabase_url, supabase_key) if supabase_url and supabase_key else None
        except Exception:
            self.supabase = None

    def _get_default_benefit_info(self, benefit_type: str) -> Dict:
        defaults = {
            'medical': {'name': 'Medical Insurance', 'description': 'Comprehensive health coverage', 'coverage': 'Hospital visits, prescriptions, preventive care', 'typical_cost': '$200-500/month', 'priority': 'Critical'},
            'dental': {'name': 'Dental Insurance', 'description': 'Dental care coverage', 'coverage': 'Cleanings, fillings, orthodontics', 'typical_cost': '$30-50/month', 'priority': 'High'},
            'vision': {'name': 'Vision Insurance', 'description': 'Eye care coverage', 'coverage': 'Exams, glasses, contacts', 'typical_cost': '$10-20/month', 'priority': 'Medium'},
            'life_insurance': {'name': 'Life Insurance', 'description': 'Family financial protection', 'coverage': 'Death benefit, income replacement', 'typical_cost': '$20-100/month', 'priority': 'High'},
            'disability': {'name': 'Disability Insurance', 'description': 'Income protection', 'coverage': '60-70% salary replacement', 'typical_cost': '$30-80/month', 'priority': 'High'},
            '401k': {'name': '401(k) Plan', 'description': 'Retirement savings', 'coverage': 'Employer match, tax advantages', 'typical_cost': '3-15% of salary', 'priority': 'Critical'},
            'hsa': {'name': 'Health Savings Account', 'description': 'Tax-free medical savings', 'coverage': 'Triple tax advantage', 'typical_cost': 'Variable', 'priority': 'Medium'},
            'healthcare_fsa': {'name': 'Healthcare FSA', 'description': 'Pre-tax medical funds', 'coverage': 'Copays, prescriptions', 'typical_cost': 'Up to $3,050/year', 'priority': 'Medium'},
            'dependent_care_fsa': {'name': 'Dependent Care FSA', 'description': 'Pre-tax childcare funds', 'coverage': 'Daycare, after-school programs', 'typical_cost': 'Up to $5,000/year', 'priority': 'High'},
        }
        return defaults.get(benefit_type, {
            'name': benefit_type.replace('_', ' ').title(),
            'description': 'Benefit coverage',
            'coverage': 'Contact HR for details',
            'typical_cost': 'Varies',
            'priority': 'Medium'
        })

    def generate_report(self, user_profile: Dict, recommendations: List[Dict], 
                        risk_assessment: Dict, output_path: str,
                        answered_questions: List[Dict] = None):
        if answered_questions is None:
            answered_questions = []

        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )

        story = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=BURGUNDY,
            spaceAfter=30, alignment=TA_CENTER, fontName='Helvetica-Bold', leading=28
        )
        heading_style = ParagraphStyle(
            'CustomHeading', parent=styles['Heading2'], fontSize=16, textColor=DARK_BURGUNDY,
            spaceAfter=12, spaceBefore=20, fontName='Helvetica-Bold', leading=20
        )
        subheading_style = ParagraphStyle(
            'CustomSubheading', parent=styles['Heading3'], fontSize=13, textColor=BURGUNDY,
            spaceAfter=10, fontName='Helvetica-Bold', leading=16
        )
        body_style = ParagraphStyle(
            'CustomBody', parent=styles['BodyText'], fontSize=10, leading=14,
            alignment=TA_JUSTIFY, spaceAfter=8, wordWrap='CJK'
        )

        # Title
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph("COMPREHENSIVE BENEFIT ASSESSMENT REPORT", title_style))
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%B %d, %Y')}",
            ParagraphStyle('Date', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10, textColor=colors.grey)
        ))
        story.append(Spacer(1, 0.5*inch))

        # Profile
        story.append(Paragraph("PERSONAL PROFILE", heading_style))
        profile_data = [
            ["Age:", str(user_profile.get('age', 'N/A'))],
            ["Marital Status:", (user_profile.get('marital_status') or 'N/A').title()],
            ["Number of Children:", str(user_profile.get('num_children', 0))],
            ["Annual Income:", f"${int(user_profile.get('annual_income', 0)):,}"],
            ["Monthly Expenses:", f"${int(user_profile.get('monthly_expenses', 0)):,}"],
            ["Total Debt:", f"${int(user_profile.get('total_debt', 0)):,}"],
            ["Savings:", f"${int(user_profile.get('savings', 0)):,}"],
        ]
        table = Table(profile_data, colWidths=[2.5*inch, 4*inch])
        table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (0, -1), DARK_BURGUNDY),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.3*inch))

        # Risk assessment
        story.append(PageBreak())
        story.append(Paragraph("COMPREHENSIVE RISK ASSESSMENT", heading_style))
        financial_wellbeing = compute_financial_wellbeing_score(user_profile)
        if financial_wellbeing is not None:
            story.append(Paragraph(f"<b>Financial Wellbeing Score:</b> <font color='#6b0f1a'>{financial_wellbeing}/100</font>", body_style))
            story.append(Spacer(1, 0.1*inch))

        # Render categories sorted by severity
        severity_order = {'Important': 0, 'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
        risk_categories = [
            ('Financial Risk', risk_assessment.get('financial_risk', 'Medium'), risk_assessment.get('financial_risk_detail', '')),
            ('Health & Wellness', risk_assessment.get('health_risk', 'Medium'), risk_assessment.get('health_risk_detail', '')),
            ('Mental Health & Burnout', risk_assessment.get('mental_health_risk', 'Medium'), risk_assessment.get('mental_health_risk_detail', '')),
            ('Family & Dependents', risk_assessment.get('family_risk', 'Low'), risk_assessment.get('family_risk_detail', '')),
            ('Retirement Readiness', risk_assessment.get('retirement_risk', 'Medium'), risk_assessment.get('retirement_risk_detail', '')),
            ('Disability Protection', risk_assessment.get('disability_risk', 'Medium'), risk_assessment.get('disability_risk_detail', '')),
            ('Career & Growth', risk_assessment.get('career_risk', 'Low'), risk_assessment.get('career_risk_detail', '')),
            ('Work-Life Balance', risk_assessment.get('worklife_risk', 'Medium'), risk_assessment.get('worklife_risk_detail', '')),
        ]
        risk_categories.sort(key=lambda x: severity_order.get(x[1], 99))
        for name, level, detail in risk_categories:
            story.append(Paragraph(f"<b>{name}</b>", subheading_style))
            mapped = 'Important' if level == 'Critical' else level
            story.append(Paragraph(f"<font color='#6b0f1a'><b>Risk Level:</b></font> {mapped}", body_style))
            if detail:
                story.append(Paragraph(detail, body_style))
            story.append(Spacer(1, 0.18*inch))

        # Recommendations
        story.append(PageBreak())
        story.append(Paragraph("PERSONALIZED BENEFIT RECOMMENDATIONS", heading_style))
        normalized = []
        seen = set()
        for r in recommendations or []:
            bt = (r.get('benefit_type') or r.get('benefit') or '').strip()
            score = float(r.get('score', 0) or 0)
            rationale = (r.get('rationale') or '').strip()
            key = (bt, round(score, 1), rationale)
            if not bt or key in seen:
                continue
            seen.add(key)
            normalized.append({'benefit_type': bt, 'score': score, 'priority': (r.get('priority') or 'RECOMMENDED').upper(), 'rationale': rationale})
        priority_weight = {'CRITICAL': 0, 'RECOMMENDED': 1, 'OPTIONAL': 2}
        normalized.sort(key=lambda x: (priority_weight.get(x['priority'], 99), -x['score']))
        for rec in normalized:
            info = self._get_default_benefit_info(rec['benefit_type'])
            name = info.get('name') or rec['benefit_type'].replace('_', ' ').title()
            story.append(Paragraph(f"<b>{name}</b> - <font color='#6b0f1a'>Match Score: {rec['score']:.0f}/100</font>", body_style))
            why = rec.get('rationale') or 'Recommended based on your profile and needs.'
            story.append(Paragraph(f"<b>Why This Matters:</b> {why}", ParagraphStyle('Small', parent=styles['Normal'], fontSize=9, leading=12)))
            story.append(Spacer(1, 0.16*inch))

        # Action items + disclaimer
        story.append(PageBreak())
        story.append(Paragraph("NEXT STEPS & ACTION ITEMS", heading_style))
        items = [
            "Review CRITICAL priority benefits and enroll during open enrollment",
            "Meet with HR to discuss specific options and costs",
            "Compare provider networks and coverage details",
            "Calculate tax savings from FSA/HSA contributions",
            "Review beneficiaries for life insurance and retirement",
            "Set up automatic contributions to maximize match",
        ]
        for i, txt in enumerate(items, 1):
            story.append(Paragraph(f"{i}. {txt}", ParagraphStyle('Action', parent=styles['BodyText'], leftIndent=18, spaceAfter=6)))

        disclaimer = (
            "<i>Disclaimer: This report provides general guidance and is not legal or financial advice. "
            "Consult qualified professionals and your HR team before making benefit elections.</i>"
        )
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(disclaimer, ParagraphStyle('Small2', parent=styles['Normal'], fontSize=9, leading=12)))

        doc.build(story)
        return output_path


def calculate_risk_assessment(profile: Dict, answers: List) -> Dict:
    """Shallow wrapper using the same logic as before to compute risk categories."""
    # Minimal inline version: compute financial wellbeing and basic categories
    age = int(profile.get('age', 30) or 30)
    income = float(profile.get('annual_income', 50000) or 50000)
    debt = float(profile.get('total_debt', 0) or 0)
    savings = float(profile.get('savings', 0) or 0)
    expenses = float(profile.get('monthly_expenses', income * 0.6 / 12) or income * 0.6 / 12)

    dti = (debt / income) if income else 0
    ef_months = (savings / expenses) if expenses else 0
    fin_score = 0
    fin_score += 30 if dti > 0.5 else 20 if dti > 0.3 else 10 if dti > 0.15 else 0
    fin_score += 30 if ef_months < 1 else 20 if ef_months < 3 else 10 if ef_months < 6 else 0
    if fin_score > 50:
        financial_risk = 'Critical'; financial_detail = f'URGENT: DTI {dti:.1%}, {ef_months:.1f} mo. savings.'
    elif fin_score > 30:
        financial_risk = 'High'; financial_detail = f'High stress. DTI {dti:.1%}. Build 3-6 mo. fund.'
    elif fin_score > 15:
        financial_risk = 'Medium'; financial_detail = f'Moderate. Savings {ef_months:.1f} mo.; target 6.'
    else:
        financial_risk = 'Low'; financial_detail = f'Strong foundation. Savings {ef_months:.1f} mo.; DTI {dti:.1%}.'

    # Simple placeholders for other categories to avoid losing features
    result = {
        'financial_risk': financial_risk,
        'financial_risk_detail': financial_detail,
        'health_risk': 'Medium' if age > 40 else 'Low',
        'health_risk_detail': 'Age-adjusted preventive care recommended.' if age > 40 else 'Maintain healthy habits.',
        'mental_health_risk': 'Medium',
        'mental_health_risk_detail': 'Use available mental health benefits proactively.',
        'family_risk': 'Medium' if int(profile.get('num_children', 0) or 0) > 0 else 'Low',
        'family_risk_detail': 'Plan for dependents and childcare.' if int(profile.get('num_children', 0) or 0) > 0 else 'Limited dependent risk.',
        'retirement_risk': 'Medium',
        'retirement_risk_detail': 'Increase contributions if below 10%.',
        'disability_risk': 'High' if income > 100000 else 'Medium',
        'disability_risk_detail': 'Income protection is important.',
        'career_risk': 'Low',
        'career_risk_detail': 'Continue investing in growth.',
        'worklife_risk': 'Medium',
        'worklife_risk_detail': 'Balance workload and wellness.'
    }
    result['financial_wellbeing_score'] = compute_financial_wellbeing_score(profile)
    return result


def compute_financial_wellbeing_score(user_profile: Dict) -> Optional[int]:
    try:
        income = float(user_profile.get('annual_income', 0) or 0)
        debt = float(user_profile.get('total_debt', 0) or 0)
        monthly_expenses = float(user_profile.get('monthly_expenses', 0) or 0)
        savings = float(user_profile.get('savings', 0) or 0)
        dti = debt / max(1.0, income)
        emergency_months = (savings / monthly_expenses) if monthly_expenses > 0 else 0.0
        dti_score = max(0.0, 40.0 * (1.0 - min(dti, 1.0)))
        ef_score = min(40.0, emergency_months * (40.0 / 6.0))
        stability_score = 20.0 if int(user_profile.get('num_children', 0) or 0) == 0 else 15.0
        score = int(round(min(100.0, dti_score + ef_score + stability_score)))
        return score
    except Exception:
        return None

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


@app.route('/home')
def home():
    """Serve a simple home page linking to HR and Questionnaire"""
    return render_template('home.html')


@app.route('/hr')
def hr_portal():
    """Serve a stub HR page users can navigate to from Home"""
    return render_template('hr.html')


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
    
    # Allow overriding host/port via environment variables for flexibility
    port = int(os.environ.get('PORT', '5000'))
    host = os.environ.get('HOST', '127.0.0.1')
    app.run(debug=True, host=host, port=port)
