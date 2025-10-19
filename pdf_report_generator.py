"""
Enhanced PDF Report Generator with Burgundy Theme
Comprehensive benefit assessment reports with proper text wrapping
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os
from typing import Dict, List
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Burgundy color theme
BURGUNDY = colors.HexColor('#6b0f1a')
DARK_BURGUNDY = colors.HexColor('#4a0a11')
LIGHT_BURGUNDY = colors.HexColor('#d24545')

class BenefitReportGenerator:
    """Generate comprehensive PDF reports with benefit recommendations"""
    
    def __init__(self):
        # Initialize Supabase client
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if supabase_url and supabase_key:
            self.supabase: Client = create_client(supabase_url, supabase_key)
            print("✓ Connected to Supabase")
        else:
            self.supabase = None
            print("⚠ Supabase credentials not found, using default data")
    
    def fetch_benefit_details(self, benefit_type: str) -> Dict:
        """Fetch benefit details from Supabase database"""
        if not self.supabase:
            return self._get_default_benefit_info(benefit_type)
        
        try:
            search_term = benefit_type.replace('_', ' ')
            response = self.supabase.table('benefits').select('*').ilike('name', f'%{search_term}%').limit(1).execute()
            
            if response.data and len(response.data) > 0:
                benefit = response.data[0]
                return {
                    'name': benefit.get('name', benefit_type.replace('_', ' ').title()),
                    'description': benefit.get('description', ''),
                    'coverage': benefit.get('description', ''),
                    'typical_cost': f"${benefit.get('cost', 0)}/month" if benefit.get('cost') else 'Varies',
                    'priority': 'Medium'
                }
            else:
                return self._get_default_benefit_info(benefit_type)
        except Exception as e:
            print(f"Error fetching benefit {benefit_type}: {e}")
            return self._get_default_benefit_info(benefit_type)
    
    def _get_default_benefit_info(self, benefit_type: str) -> Dict:
        """Comprehensive default benefit information"""
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
            'pet_insurance': {'name': 'Pet Insurance', 'description': 'Veterinary coverage', 'coverage': 'Accidents, illnesses', 'typical_cost': '$30-60/month per pet', 'priority': 'Low'},
            'mental_health_stipend': {'name': 'Mental Health Stipend', 'description': 'Wellness support', 'coverage': 'Therapy, apps, coaching', 'typical_cost': '$100-500/month', 'priority': 'High'},
            'student_loan_repayment': {'name': 'Student Loan Assistance', 'description': 'Loan repayment help', 'coverage': 'Direct payments to loans', 'typical_cost': '$200-500/month', 'priority': 'Critical'},
            'sabbatical': {'name': 'Sabbatical Program', 'description': 'Extended paid break', 'coverage': '4-8 weeks after 5-7 years', 'typical_cost': 'Fully paid', 'priority': 'High'},
            'remote_work_stipend': {'name': 'Remote Work Stipend', 'description': 'Home office support', 'coverage': 'Equipment, internet', 'typical_cost': '$1000-2000/year', 'priority': 'High'},
            'learning_stipend': {'name': 'Learning Stipend', 'description': 'Education support', 'coverage': 'Courses, conferences', 'typical_cost': '$1000-3000/year', 'priority': 'High'},
        }
        
        return defaults.get(benefit_type, {
            'name': benefit_type.replace('_', ' ').title(),
            'description': 'Benefit coverage',
            'coverage': 'Contact HR for details',
            'typical_cost': 'Varies',
            'priority': 'Medium'
        })
    
    def generate_report(self, user_profile: Dict, recommendations: List[Dict], 
                       risk_assessment: Dict, output_path: str = 'benefit_report.pdf',
                       answered_questions: List[Dict] = None):
        """Generate comprehensive PDF report with proper formatting"""
        if answered_questions is None:
            answered_questions = []
        
        # Create PDF with proper margins
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
        
        # Custom styles with text wrapping
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=BURGUNDY,
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=28
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=DARK_BURGUNDY,
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            leading=20
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubheading',
            parent=styles['Heading3'],
            fontSize=13,
            textColor=BURGUNDY,
            spaceAfter=10,
            fontName='Helvetica-Bold',
            leading=16
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            wordWrap='CJK'  # Proper word wrapping
        )
        
        small_text = ParagraphStyle(
            'SmallText',
            parent=styles['Normal'],
            fontSize=9,
            leading=12,
            textColor=colors.black,
            alignment=TA_JUSTIFY
        )
        
        # Title Page
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph("COMPREHENSIVE BENEFIT ASSESSMENT REPORT", title_style))
        story.append(Spacer(1, 0.1*inch))
        
        date_text = f"Generated: {datetime.now().strftime('%B %d, %Y')}"
        story.append(Paragraph(date_text, ParagraphStyle('Date', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10, textColor=colors.grey)))
        story.append(Spacer(1, 0.5*inch))
        
        # User Profile Section
        story.append(Paragraph("PERSONAL PROFILE", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Profile table with proper widths
        profile_data = [
            ["Age:", str(user_profile.get('age', 'N/A'))],
            ["Marital Status:", (user_profile.get('marital_status') or 'N/A').title()],
            ["Number of Children:", str(user_profile.get('num_children', 0))],
            ["Annual Income:", f"${int(user_profile.get('annual_income', 0)):,}"],
            ["Monthly Expenses:", f"${int(user_profile.get('monthly_expenses', 0)):,}"],
            ["Total Debt:", f"${int(user_profile.get('total_debt', 0)):,}"],
            ["Savings:", f"${int(user_profile.get('savings', 0)):,}"],
        ]
        
        profile_table = Table(profile_data, colWidths=[2.5*inch, 4*inch])
        profile_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (0, -1), DARK_BURGUNDY),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(profile_table)
        story.append(Spacer(1, 0.3*inch))

        # Answered Questions Summary (requested on first page)
        if answered_questions:
            story.append(Paragraph("YOUR ANSWERS", heading_style))
            story.append(Spacer(1, 0.08*inch))

            # Build a two-column table: Question | Your Answer
            qa_rows = [["Question", "Your Answer"]]
            for qa in answered_questions:
                qtext = qa.get('text', qa.get('id', ''))
                ans = qa.get('answer', '')
                # Ensure strings
                qtext = str(qtext)
                ans = str(ans)
                qa_rows.append([qtext, ans])

            qa_table = Table(qa_rows, colWidths=[4.2*inch, 2.3*inch])
            qa_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
                ('TEXTCOLOR', (0, 0), (-1, 0), DARK_BURGUNDY),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.lightgrey),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(qa_table)
            story.append(Spacer(1, 0.2*inch))
        
        # COMPREHENSIVE RISK ASSESSMENT - Enhanced Section
        story.append(PageBreak())
        story.append(Paragraph("COMPREHENSIVE RISK ASSESSMENT", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        intro_text = """This comprehensive analysis evaluates your risk profile across eight critical dimensions 
        of financial and personal wellbeing. Each category has been carefully assessed based on your demographic 
        information, financial situation, and lifestyle indicators to provide personalized risk mitigation strategies."""
        story.append(Paragraph(intro_text, body_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Financial Wellbeing Score (0-100) using real inputs
        fws_components = []
        try:
            dti = (user_profile.get('total_debt', 0) or 0) / max(1.0, float(user_profile.get('annual_income', 0) or 0))
            emergency_months = 0
            monthly_expenses = float(user_profile.get('monthly_expenses', 0) or 0)
            savings = float(user_profile.get('savings', 0) or 0)
            if monthly_expenses > 0:
                emergency_months = savings / monthly_expenses
            # Score pieces: lower DTI better, higher emergency months better
            dti_score = max(0, 40 * (1 - min(dti, 1.0)))  # up to 40 pts
            ef_score = min(40, emergency_months * (40/6))  # 6 months => 40 pts
            stability_score = 20 if user_profile.get('num_children', 0) == 0 else 15  # simple proxy
            financial_wellbeing = int(round(min(100, dti_score + ef_score + stability_score)))
        except Exception:
            financial_wellbeing = None

        if financial_wellbeing is not None:
            story.append(Paragraph(f"<b>Financial Wellbeing Score:</b> <font color='#6b0f1a'>{financial_wellbeing}/100</font>", body_style))
            story.append(Spacer(1, 0.1*inch))

        # Risk Assessment Categories (sorted by severity)
        risk_categories = [
            ('Financial Risk', risk_assessment.get('financial_risk', 'Medium'), 
             risk_assessment.get('financial_risk_detail', risk_assessment.get('financial_detail', 'Moderate financial exposure'))),
            ('Health & Wellness', risk_assessment.get('health_risk', 'Medium'),
             risk_assessment.get('health_risk_detail', risk_assessment.get('health_detail', 'Standard health considerations'))),
            ('Mental Health & Burnout', risk_assessment.get('mental_health_risk', 'Medium'),
             risk_assessment.get('mental_health_risk_detail', 'Moderate stress factors')),
            ('Family & Dependents', risk_assessment.get('family_risk', 'Low'),
             risk_assessment.get('family_risk_detail', risk_assessment.get('family_detail', 'Family protection considerations'))),
            ('Retirement Readiness', risk_assessment.get('retirement_risk', 'Medium'),
             risk_assessment.get('retirement_risk_detail', risk_assessment.get('retirement_detail', 'Retirement planning status'))),
            ('Disability Protection', risk_assessment.get('disability_risk', 'Medium'),
             risk_assessment.get('disability_risk_detail', risk_assessment.get('disability_detail', 'Income protection needs'))),
            ('Career & Growth', risk_assessment.get('career_risk', 'Low'),
             risk_assessment.get('career_risk_detail', 'Professional development status')),
            ('Work-Life Balance', risk_assessment.get('worklife_risk', 'Medium'),
             risk_assessment.get('worklife_risk_detail', risk_assessment.get('worklife_detail', 'Balance and wellness factors')))
        ]

        severity_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
        risk_categories.sort(key=lambda x: severity_order.get(x[1], 99))
        
        for category_name, risk_level, detail in risk_categories:
            # Risk category header
            story.append(Paragraph(f"<b>{category_name}</b>", subheading_style))
            story.append(Spacer(1, 0.05*inch))
            
            # Risk level as simple text (no colored bars)
            risk_level_text = f"<font color='#6b0f1a'><b>Risk Level:</b></font> {risk_level}"
            story.append(Paragraph(risk_level_text, body_style))
            story.append(Spacer(1, 0.05*inch))
            
            # Risk details
            story.append(Paragraph(detail, body_style))
            story.append(Spacer(1, 0.2*inch))
        
        # Recommendations Section
        story.append(PageBreak())
        story.append(Paragraph("PERSONALIZED BENEFIT RECOMMENDATIONS", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Normalize and de-duplicate recommendations
        normalized_recs = self._normalize_recommendations(recommendations)
        # Group by priority
        critical = [r for r in normalized_recs if r.get('priority') == 'CRITICAL']
        recommended = [r for r in normalized_recs if r.get('priority') == 'RECOMMENDED']
        optional = [r for r in normalized_recs if r.get('priority') == 'OPTIONAL']
        
        # Critical Benefits
        if critical:
            story.append(Paragraph("CRITICAL PRIORITIES", subheading_style))
            story.append(Spacer(1, 0.05*inch))
            story.append(Paragraph("These benefits are essential for your situation and should be prioritized immediately.", body_style))
            story.append(Spacer(1, 0.1*inch))
            
            for rec in critical:
                self._add_benefit_recommendation(story, rec, body_style, small_text)
        
        # Recommended Benefits
        if recommended:
            story.append(Paragraph("STRONGLY RECOMMENDED", subheading_style))
            story.append(Spacer(1, 0.05*inch))
            story.append(Paragraph("These benefits provide significant value and protection for your circumstances.", body_style))
            story.append(Spacer(1, 0.1*inch))
            
            for rec in recommended:
                self._add_benefit_recommendation(story, rec, body_style, small_text)
        
        # Optional Benefits
        if optional:
            story.append(Paragraph("OPTIONAL CONSIDERATIONS", subheading_style))
            story.append(Spacer(1, 0.05*inch))
            story.append(Paragraph("These benefits may provide additional value based on your preferences.", body_style))
            story.append(Spacer(1, 0.1*inch))
            
            for rec in optional:
                self._add_benefit_recommendation(story, rec, body_style, small_text)
        
        # Action Items
        story.append(PageBreak())
        story.append(Paragraph("NEXT STEPS & ACTION ITEMS", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        action_items = [
            "Review all CRITICAL priority benefits and enroll immediately during open enrollment",
            "Schedule a meeting with HR to discuss your specific benefit options and costs",
            "Compare provider networks and coverage details for insurance benefits",
            "Calculate your tax savings from FSA/HSA contributions",
            "Review beneficiary designations for life insurance and retirement accounts",
            "Set up automatic contributions to maximize employer matching programs",
            "Reassess your benefit needs annually or after major life events"
        ]
        
        for i, item in enumerate(action_items, 1):
            item_style = ParagraphStyle('ActionItem', parent=body_style, leftIndent=20, spaceAfter=6)
            story.append(Paragraph(f"{i}. {item}", item_style))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Disclaimer
        disclaimer = """<i>Disclaimer: This report provides general guidance based on the information provided. 
        It is not intended as legal, financial, or professional advice. Please consult with qualified 
        professionals and your HR department before making benefit elections. Benefit availability, 
        costs, and coverage details may vary by employer and plan year.</i>"""
        story.append(Paragraph(disclaimer, small_text))
        
        # Build PDF
        doc.build(story)
        print(f"✓ PDF report generated: {output_path}")
        return output_path
    
    def _add_benefit_recommendation(self, story, rec, body_style, small_text):
        """Add a single benefit recommendation with proper formatting"""
        benefit_type = rec.get('benefit_type') or rec.get('benefit') or ''
        benefit_info = self.fetch_benefit_details(benefit_type)
        
        # Benefit name and score
        benefit_name = benefit_info.get('name') or benefit_type.replace('_', ' ').title()
        score = float(rec.get('score', 0) or 0)
        confidence = rec.get('confidence', 0)
        priority = (rec.get('priority') or 'RECOMMENDED').upper()
        
        # Create clean benefit header with score
        header_text = f"<b>{benefit_name}</b> - <font color='#6b0f1a'>Match Score: {score:.0f}/100</font>"
        story.append(Paragraph(header_text, body_style))
        story.append(Spacer(1, 0.08*inch))
        
        # Get rationale - use the actual rationale from recommendation
        rationale = rec.get('rationale') or 'Recommended based on your profile and needs'
        
        # Only show rationale (skip generic description/cost from Supabase)
        detail_text = f"<b>Why This Matters:</b> {rationale}"
        story.append(Paragraph(detail_text, small_text))
        story.append(Spacer(1, 0.2*inch))

    def _normalize_recommendations(self, recs: List[Dict]) -> List[Dict]:
        """Normalize keys, remove duplicates by (benefit_type, score, rationale), and sort by priority then score."""
        normalized = []
        seen = set()
        for r in recs or []:
            bt = (r.get('benefit_type') or r.get('benefit') or '').strip()
            score = float(r.get('score', 0) or 0)
            priority = (r.get('priority') or 'RECOMMENDED').upper()
            rationale = (r.get('rationale') or '').strip()
            key = (bt, round(score, 1), rationale)
            if not bt or key in seen:
                continue
            seen.add(key)
            normalized.append({
                'benefit_type': bt,
                'score': score,
                'priority': priority,
                'rationale': rationale,
                'confidence': r.get('confidence')
            })
        # Priority order: CRITICAL > RECOMMENDED > OPTIONAL > others, then score desc
        priority_weight = {'CRITICAL': 0, 'RECOMMENDED': 1, 'OPTIONAL': 2}
        normalized.sort(key=lambda x: (priority_weight.get(x['priority'], 99), -x['score']))
        return normalized


def calculate_risk_assessment(profile: Dict, answers: List) -> Dict:
    """Calculate comprehensive risk assessment based on user profile and answers"""
    
    # Extract profile data with safe defaults
    age = int(profile.get('age', 30)) if profile.get('age') else 30
    income = float(profile.get('annual_income', 50000)) if profile.get('annual_income') else 50000
    debt = float(profile.get('total_debt', 0)) if profile.get('total_debt') else 0
    savings = float(profile.get('savings', 0)) if profile.get('savings') else 0
    children = int(profile.get('num_children', 0)) if profile.get('num_children') else 0
    monthly_expenses = float(profile.get('monthly_expenses', income * 0.6 / 12)) if profile.get('monthly_expenses') else income * 0.6 / 12
    
    # Analyze answer patterns for behavioral risks
    risk_behaviors = []
    wellness_score = 5  # Default moderate wellness
    financial_literacy = 5  # Default moderate literacy
    
    for answer in answers:
        qid = answer.get('question_id', '')
        choice = answer.get('choice', '')
        
        # Identify risk behaviors from answers
        if 'burnout' in qid.lower() and choice in ['C', 'D']:
            risk_behaviors.append('burnout_high')
            wellness_score -= 2
        if 'gym' in qid.lower() and choice in ['C', 'D']:
            risk_behaviors.append('no_exercise')
            wellness_score -= 1
        if 'therapy' in qid.lower() and choice in ['C', 'D']:
            risk_behaviors.append('mental_health_neglect')
            wellness_score -= 1
        if 'budget' in qid.lower() and choice in ['C', 'D']:
            risk_behaviors.append('no_budget')
            financial_literacy -= 2
        if 'emergency' in qid.lower() and choice in ['C', 'D']:
            risk_behaviors.append('no_emergency_fund')
            financial_literacy -= 1
        if 'extreme_sports' in qid.lower() and choice == 'A':
            risk_behaviors.append('engages_risky_activities')
            
    # Ensure scores stay in valid range
    wellness_score = max(0, min(10, wellness_score))
    financial_literacy = max(0, min(10, financial_literacy))
    
    # Calculate key financial ratios
    debt_to_income = debt / income if income > 0 else 0
    savings_rate = (savings / income) if income > 0 else 0
    emergency_months = (savings / monthly_expenses) if monthly_expenses > 0 else 0
    
    # 1. FINANCIAL RISK ASSESSMENT
    financial_risk_score = 0
    
    if debt_to_income > 0.5:
        financial_risk_score += 30
    elif debt_to_income > 0.3:
        financial_risk_score += 20
    elif debt_to_income > 0.15:
        financial_risk_score += 10
        
    if emergency_months < 1:
        financial_risk_score += 30
    elif emergency_months < 3:
        financial_risk_score += 20
    elif emergency_months < 6:
        financial_risk_score += 10
        
    if 'no_budget' in risk_behaviors:
        financial_risk_score += 15
    if 'no_emergency_fund' in risk_behaviors:
        financial_risk_score += 15
        
    if financial_risk_score > 50:
        financial_risk = 'Critical'
        financial_detail = f'URGENT: Debt-to-income {debt_to_income:.1%}, only {emergency_months:.1f} months emergency savings. Financial counseling required immediately.'
    elif financial_risk_score > 30:
        financial_risk = 'High'
        financial_detail = f'High financial stress. Debt-to-income {debt_to_income:.1%}. Build emergency fund to 3-6 months expenses. Consider financial planning.'
    elif financial_risk_score > 15:
        financial_risk = 'Medium'
        financial_detail = f'Moderate financial health. Continue building emergency fund. Current: {emergency_months:.1f} months. Target: 6 months.'
    else:
        financial_risk = 'Low'
        financial_detail = f'Strong financial foundation. Emergency fund: {emergency_months:.1f} months. Debt well managed at {debt_to_income:.1%} of income.'
    
    # 2. HEALTH & WELLNESS RISK
    health_risk_score = 0
    
    if wellness_score < 3:
        health_risk_score += 40
    elif wellness_score < 5:
        health_risk_score += 25
    elif wellness_score < 7:
        health_risk_score += 10
        
    if 'no_exercise' in risk_behaviors:
        health_risk_score += 20
    if age > 40:
        health_risk_score += 10
    if children > 0:
        health_risk_score += 10  # Family needs preventive care
        
    if health_risk_score > 40:
        health_risk = 'Critical'
        health_detail = 'URGENT: Poor wellness habits. Start comprehensive health plan immediately: gym stipend, medical checkups, preventive care.'
    elif health_risk_score > 25:
        health_risk = 'High'
        health_detail = 'Health at risk. Prioritize gym membership, medical insurance, and regular checkups. Start small with 30min walks.'
    elif health_risk_score > 10:
        health_risk = 'Medium'
        health_detail = 'Room for improvement. Consider gym stipend and wellness programs. Build consistent exercise routine.'
    else:
        health_risk = 'Low'
        health_detail = 'Good health habits. Maintain routine and consider wellness perks for optimization.'
    
    # 3. MENTAL HEALTH & BURNOUT RISK
    mental_risk_score = 0
    
    if 'burnout_high' in risk_behaviors:
        mental_risk_score += 40
    if 'mental_health_neglect' in risk_behaviors:
        mental_risk_score += 30
    if wellness_score < 4:
        mental_risk_score += 20
    if debt_to_income > 0.4:
        mental_risk_score += 15  # Financial stress
        
    if mental_risk_score > 50:
        mental_risk = 'Critical'
        mental_detail = 'URGENT BURNOUT RISK: Immediate action required. Start therapy, take sabbatical, reduce hours. Mental health crisis intervention needed.'
    elif mental_risk_score > 30:
        mental_risk = 'High'
        mental_detail = 'High burnout risk. Prioritize therapy stipend, unlimited life days, and mental health support immediately.'
    elif mental_risk_score > 15:
        mental_risk = 'Medium'
        mental_detail = 'Moderate stress. Consider therapy stipend, meditation apps, and work-life balance improvements.'
    else:
        mental_risk = 'Low'
        mental_detail = 'Good mental health. Continue self-care and use available mental health benefits proactively.'
    
    # 4. FAMILY & DEPENDENT RISK
    family_risk_score = 0
    
    if children > 2:
        family_risk_score += 30
    elif children > 0:
        family_risk_score += 20
        
    if children > 0 and debt_to_income > 0.3:
        family_risk_score += 20
    if children > 0 and emergency_months < 3:
        family_risk_score += 25
    if children > 0 and income < 60000:
        family_risk_score += 15
        
    if family_risk_score > 50:
        family_risk = 'Critical'
        family_detail = f'URGENT: {children} dependents with high debt and low savings. Life insurance, medical, dental, and childcare stipend REQUIRED NOW.'
    elif family_risk_score > 30:
        family_risk = 'High'
        family_detail = f'Family at risk. {children} children need protection. Prioritize life insurance, medical, dental, and education savings.'
    elif family_risk_score > 15:
        family_risk = 'Medium'
        family_detail = f'Family planning needed. Consider life insurance, medical coverage, and childcare benefits for {children} children.'
    else:
        family_risk = 'Low'
        family_detail = 'Limited dependent risk. Basic coverage sufficient. Consider future family planning benefits.'
    
    # 5. RETIREMENT READINESS RISK
    retirement_risk_score = 0
    # Only compute a rough target if age and income are present and reasonable
    retirement_target = None
    if income > 0 and 18 <= age <= 65:
        retirement_target = income * max(0, (65 - age)) * 0.15
    
    if savings_rate < 0.05 and income > 0:
        retirement_risk_score += 40
    elif savings_rate < 0.10 and income > 0:
        retirement_risk_score += 25
    elif savings_rate < 0.15 and income > 0:
        retirement_risk_score += 10
        
    if age > 40 and income > 0 and savings < income * 3:
        retirement_risk_score += 30
    elif age > 30 and income > 0 and savings < income:
        retirement_risk_score += 20
        
    if retirement_risk_score > 50:
        retirement_risk = 'Critical'
        if retirement_target is not None:
            retirement_detail = f'URGENT: Far behind retirement goals. Est. target ${retirement_target:,.0f}. Increase contributions and seek advice.'
        else:
            retirement_detail = 'URGENT: Far behind retirement goals. Increase contributions and seek advice.'
    elif retirement_risk_score > 30:
        retirement_risk = 'High'
        retirement_detail = 'Behind on retirement. Increase 401k contribution by 5-10%. Use employer match.' if retirement_target is None else \
            f'Behind on retirement. Est. target ${retirement_target:,.0f}. Increase 401k contribution by 5-10%. Use employer match.'
    elif retirement_risk_score > 15:
        retirement_risk = 'Medium'
        retirement_detail = 'Retirement on track but could improve. Consider increasing contributions 2-3%.' if retirement_target is None else \
            f'Retirement on track but could improve. Est. target ${retirement_target:,.0f}. Consider increasing contributions 2-3%.'
    else:
        retirement_risk = 'Low'
        retirement_detail = 'Excellent retirement progress. Continue current strategy.'
    
    # 6. DISABILITY & INCOME PROTECTION RISK
    disability_risk_score = 0
    
    if income > 100000:
        disability_risk_score += 25
    elif income > 75000:
        disability_risk_score += 20
    elif income > 50000:
        disability_risk_score += 15
        
    if children > 0:
        disability_risk_score += 20
    if debt_to_income > 0.3:
        disability_risk_score += 15
    if 'engages_risky_activities' in risk_behaviors:
        disability_risk_score += 20
    if emergency_months < 3:
        disability_risk_score += 15
        
    if disability_risk_score > 50:
        disability_risk = 'Critical'
        disability_detail = f'URGENT: ${income:,.0f} income with dependents/debt and minimal savings. Disability insurance REQUIRED NOW.'
    elif disability_risk_score > 35:
        disability_risk = 'High'
        disability_detail = f'High income risk. Disability insurance essential to protect ${income:,.0f} income. Target 60-70% replacement.'
    elif disability_risk_score > 20:
        disability_risk = 'Medium'
        disability_detail = 'Disability insurance recommended. Consider short-term and long-term coverage.'
    else:
        disability_risk = 'Low'
        disability_detail = 'Lower income risk but still consider basic disability coverage.'
    
    # 7. CAREER & GROWTH RISK
    career_risk_score = 0
    
    if age < 35 and financial_literacy < 4:
        career_risk_score += 20
    if income < 50000 and age > 30:
        career_risk_score += 25
    
    # Check for growth mindset from answers
    growth_signals = sum(1 for a in answers if a.get('question_id') in ['Q46_learning_goals', 'Q54_side_hustle'] and a.get('choice') == 'A')
    if growth_signals == 0:
        career_risk_score += 15
        
    if career_risk_score > 30:
        career_risk = 'High'
        career_detail = 'Career stagnation risk. Invest in learning stipend, side projects, and skill development immediately.'
    elif career_risk_score > 15:
        career_risk = 'Medium'
        career_detail = 'Career growth opportunities available. Consider learning stipend and professional development.'
    else:
        career_risk = 'Low'
        career_detail = 'Good career trajectory. Continue investing in growth and skill development.'
    
    # 8. WORK-LIFE BALANCE RISK
    worklife_risk_score = wellness_score  # Lower wellness = higher risk
    
    if 'burnout_high' in risk_behaviors:
        worklife_risk_score -= 3
    if monthly_expenses > income * 0.7:
        worklife_risk_score -= 2  # Financial stress affects work-life balance
        
    if worklife_risk_score < 2:
        worklife_risk = 'Critical'
        worklife_detail = 'URGENT: Severe work-life imbalance. Sabbatical, unlimited life days, and remote work critical. Consider career change.'
    elif worklife_risk_score < 4:
        worklife_risk = 'High'
        worklife_detail = 'Poor work-life balance. Prioritize unlimited life days, workcation policy, and mental health support.'
    elif worklife_risk_score < 6:
        worklife_risk = 'Medium'
        worklife_detail = 'Room for improvement. Consider remote work stipend and flexible benefits.'
    else:
        worklife_risk = 'Low'
        worklife_detail = 'Good work-life balance. Maintain boundaries and use available benefits.'
    
    return {
        'financial_risk': financial_risk,
        'financial_risk_detail': financial_detail,
        'health_risk': health_risk,
        'health_risk_detail': health_detail,
        'mental_health_risk': mental_risk,
        'mental_health_risk_detail': mental_detail,
        'family_risk': family_risk,
        'family_risk_detail': family_detail,
        'retirement_risk': retirement_risk,
        'retirement_risk_detail': retirement_detail,
        'disability_risk': disability_risk,
        'disability_risk_detail': disability_detail,
        'career_risk': career_risk,
        'career_risk_detail': career_detail,
        'worklife_risk': worklife_risk,
        'worklife_risk_detail': worklife_detail
    }


# Example usage
if __name__ == "__main__":
    generator = BenefitReportGenerator()
    
    # Sample data
    user_profile = {
        'age': 32,
        'marital_status': 'married',
        'num_children': 2,
        'annual_income': 75000
    }
    
    recommendations = [
        {
            'benefit_type': 'medical',
            'score': 95,
            'confidence': 0.92,
            'priority': 'CRITICAL',
            'rationale': 'Essential coverage for family health needs'
        },
        {
            'benefit_type': '401k',
            'score': 90,
            'confidence': 0.88,
            'priority': 'CRITICAL',
            'rationale': 'Critical for retirement security at your age'
        }
    ]
    
    risk_assessment = {
        'financial_risk': 'Medium',
        'financial_detail': 'Moderate debt-to-income ratio with family expenses',
        'health_risk': 'Low',
        'health_detail': 'Young family with standard health needs',
        'mental_health_risk': 'Medium',
        'mental_health_detail': 'Work-life balance challenges with young children',
        'family_risk': 'High',
        'family_detail': 'High dependency risk with two young children',
        'retirement_risk': 'Medium',
        'retirement_detail': 'Good age to start aggressive saving',
        'disability_risk': 'High',
        'disability_detail': 'Critical income protection needed for family',
        'career_risk': 'Low',
        'career_detail': 'Strong career trajectory and growth potential',
        'worklife_risk': 'Medium',
        'worklife_detail': 'Balancing career growth with family responsibilities'
    }
    
    generator.generate_report(user_profile, recommendations, risk_assessment, 'test_report_v2.pdf', answered_questions=[
        {'id': 'Q1_risk_behavior', 'text': 'Which sounds more appealing for a weekend?', 'answer': 'Quiet activities'},
        {'id': 'Q2_health_consciousness', 'text': 'How do you typically handle a headache?', 'answer': 'Take medicine immediately and rest'},
    ])
