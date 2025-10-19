"""
PDF Report Generator with Supabase Integration
Generates comprehensive benefit assessment reports with risk analysis
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from typing import Dict, List
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

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
            # Query benefits table using 'name' column with fuzzy matching
            search_term = benefit_type.replace('_', ' ')
            response = self.supabase.table('benefits').select('*').ilike('name', f'%{search_term}%').limit(1).execute()
            
            if response.data and len(response.data) > 0:
                benefit = response.data[0]
                # Map Supabase columns to expected format
                return {
                    'name': benefit.get('name', benefit_type.replace('_', ' ').title()),
                    'description': benefit.get('description', ''),
                    'coverage': benefit.get('description', ''),  # Use description for coverage
                    'typical_cost': f"${benefit.get('cost', 0)}/month" if benefit.get('cost') else 'Varies',
                    'priority': 'Medium'  # Default priority
                }
            else:
                return self._get_default_benefit_info(benefit_type)
        except Exception as e:
            print(f"Error fetching benefit {benefit_type}: {e}")
            return self._get_default_benefit_info(benefit_type)
    
    def _get_default_benefit_info(self, benefit_type: str) -> Dict:
        """Default benefit information if database query fails"""
        defaults = {
            'medical': {
                'name': 'Medical Insurance',
                'description': 'Comprehensive health coverage for medical expenses',
                'coverage': 'Hospital visits, doctor appointments, prescriptions, preventive care',
                'typical_cost': '$200-500/month',
                'priority': 'Critical'
            },
            'dental': {
                'name': 'Dental Insurance',
                'description': 'Coverage for dental care and procedures',
                'coverage': 'Cleanings, fillings, root canals, orthodontics',
                'typical_cost': '$30-50/month',
                'priority': 'High'
            },
            'vision': {
                'name': 'Vision Insurance',
                'description': 'Eye care and vision correction coverage',
                'coverage': 'Eye exams, glasses, contact lenses',
                'typical_cost': '$10-20/month',
                'priority': 'Medium'
            },
            'life_insurance': {
                'name': 'Life Insurance',
                'description': 'Financial protection for your family',
                'coverage': 'Death benefit, income replacement',
                'typical_cost': '$20-100/month',
                'priority': 'High'
            },
            'disability': {
                'name': 'Disability Insurance',
                'description': 'Income protection if unable to work',
                'coverage': '60-70% salary replacement',
                'typical_cost': '$30-80/month',
                'priority': 'High'
            },
            '401k': {
                'name': '401(k) Retirement Plan',
                'description': 'Tax-advantaged retirement savings',
                'coverage': 'Employer match, investment options',
                'typical_cost': '3-15% of salary',
                'priority': 'Critical'
            },
            'hsa': {
                'name': 'Health Savings Account (HSA)',
                'description': 'Tax-free medical expense savings',
                'coverage': 'Triple tax advantage, rolls over annually',
                'typical_cost': 'Variable contributions',
                'priority': 'Medium'
            },
            'healthcare_fsa': {
                'name': 'Healthcare FSA',
                'description': 'Pre-tax funds for medical expenses',
                'coverage': 'Copays, prescriptions, medical supplies',
                'typical_cost': 'Up to $3,050/year',
                'priority': 'Medium'
            },
            'dependent_care_fsa': {
                'name': 'Dependent Care FSA',
                'description': 'Pre-tax childcare funds',
                'coverage': 'Daycare, after-school programs',
                'typical_cost': 'Up to $5,000/year',
                'priority': 'High (if children)'
            },
            'pet_insurance': {
                'name': 'Pet Insurance',
                'description': 'Veterinary care coverage',
                'coverage': 'Accidents, illnesses, surgeries',
                'typical_cost': '$30-60/month per pet',
                'priority': 'Low (if pets)'
            },
            'identity_theft': {
                'name': 'Identity Theft Protection',
                'description': 'Credit monitoring and fraud protection',
                'coverage': 'Credit monitoring, fraud resolution',
                'typical_cost': '$10-25/month',
                'priority': 'Medium'
            },
            'legal_services': {
                'name': 'Legal Services Plan',
                'description': 'Access to legal consultation',
                'coverage': 'Consultations, document review, representation',
                'typical_cost': '$15-30/month',
                'priority': 'Low'
            },
            'critical_illness': {
                'name': 'Critical Illness Insurance',
                'description': 'Lump sum for serious diagnoses',
                'coverage': 'Cancer, heart attack, stroke',
                'typical_cost': '$30-80/month',
                'priority': 'Medium'
            },
            'hospital_indemnity': {
                'name': 'Hospital Indemnity',
                'description': 'Cash payments for hospital stays',
                'coverage': 'Per-day hospital benefits',
                'typical_cost': '$20-40/month',
                'priority': 'Low'
            },
            'accident_insurance': {
                'name': 'Accident Insurance',
                'description': 'Coverage for accidental injuries',
                'coverage': 'ER visits, fractures, burns',
                'typical_cost': '$15-35/month',
                'priority': 'Low'
            },
            'long_term_care': {
                'name': 'Long-Term Care Insurance',
                'description': 'Extended care coverage',
                'coverage': 'Nursing homes, assisted living',
                'typical_cost': '$100-300/month',
                'priority': 'Low (if young)'
            },
            'commuter_benefits': {
                'name': 'Commuter Benefits',
                'description': 'Pre-tax transit and parking',
                'coverage': 'Public transit, parking',
                'typical_cost': 'Up to $315/month',
                'priority': 'Medium (if commute)'
            },
            'supplemental_life': {
                'name': 'Supplemental Life Insurance',
                'description': 'Additional life coverage',
                'coverage': 'Extra death benefit',
                'typical_cost': '$10-50/month',
                'priority': 'Medium'
            },
            # Lifestyle & Wellness
            'mental_health_stipend': {
                'name': 'Mental Health Stipend',
                'description': '$100-500/month for therapy, meditation apps, wellness coaching',
                'coverage': 'Therapy sessions, mental health apps (Calm, Headspace), wellness coaching, stress management',
                'typical_cost': '$100-500/month',
                'priority': 'High'
            },
            'pawternity_leave': {
                'name': 'Pet Insurance & Pawternity Leave',
                'description': 'Coverage for pets + days off when adopting',
                'coverage': 'Veterinary care, adoption leave (2-5 days), pet wellness',
                'typical_cost': '$30-60/month + paid leave',
                'priority': 'Medium'
            },
            'sabbatical': {
                'name': 'Sabbatical Program',
                'description': 'Paid 4-8 week break after X years of service',
                'coverage': 'Full pay during extended time off for rest, travel, personal projects',
                'typical_cost': 'Fully paid (after 5-7 years)',
                'priority': 'High'
            },
            'fertility_support': {
                'name': 'Fertility & Family Planning',
                'description': 'IVF coverage, adoption assistance, egg freezing',
                'coverage': 'Up to $50k for IVF, adoption support, fertility treatments, egg/sperm freezing',
                'typical_cost': 'Employer-covered up to limits',
                'priority': 'High'
            },
            'menopause_support': {
                'name': 'Menopause Support',
                'description': 'Specialized care, flexible scheduling during symptoms',
                'coverage': 'Hormone therapy, specialist care, flexible work arrangements, wellness programs',
                'typical_cost': '$50-200/month + flexibility',
                'priority': 'Medium'
            },
            # Financial Wellness
            'student_loan_repayment': {
                'name': 'Student Loan Repayment Assistance',
                'description': '$200-500/month contribution toward student loans',
                'coverage': 'Direct payments to loan servicers, up to $5,250/year tax-free',
                'typical_cost': '$200-500/month employer contribution',
                'priority': 'Critical'
            },
            'emergency_savings_match': {
                'name': 'Emergency Savings Match',
                'description': 'Company matches emergency fund contributions',
                'coverage': 'Employer matches emergency savings deposits 50-100%, up to $1000/year',
                'typical_cost': 'Employer match varies',
                'priority': 'High'
            },
            'financial_coaching': {
                'name': 'Financial Coaching',
                'description': 'Free 1-on-1 sessions with certified financial planners',
                'coverage': 'Budget planning, debt management, investment advice, retirement planning',
                'typical_cost': 'Fully covered (4-12 sessions/year)',
                'priority': 'Medium'
            },
            'crypto_stock_benefits': {
                'name': 'Crypto & Stock Trading Benefits',
                'description': 'Company equity in crypto, or stock trading education',
                'coverage': 'Stock grants, crypto education, trading platform access, investment workshops',
                'typical_cost': 'Equity grants + education',
                'priority': 'Medium'
            },
            # Work-Life Integration
            'unlimited_life_days': {
                'name': 'Unlimited "Life Days"',
                'description': 'Beyond PTO: moving day, mental health day, pet emergencies',
                'coverage': 'Flexible time off for life events: moving, pet care, family needs, mental health',
                'typical_cost': 'No deduction from PTO',
                'priority': 'High'
            },
            'remote_work_stipend': {
                'name': 'Remote Work Stipend',
                'description': '$1000-2000/year for home office setup',
                'coverage': 'Desk, chair, monitor, internet, ergonomic equipment, coworking membership',
                'typical_cost': '$1000-2000/year',
                'priority': 'High'
            },
            'coworking_membership': {
                'name': 'Co-Working Space Membership',
                'description': 'Access to WeWork-style spaces globally',
                'coverage': 'Hot desks, meeting rooms, global coworking network access',
                'typical_cost': '$200-400/month (employer-paid)',
                'priority': 'Medium'
            },
            'workcation_policy': {
                'name': 'Workcation Policy',
                'description': 'Work from anywhere for 2-4 weeks/year',
                'coverage': 'Travel while working, digital nomad support, global work flexibility',
                'typical_cost': 'No extra cost (requires WiFi)',
                'priority': 'Medium'
            },
            # Learning & Growth
            'learning_stipend': {
                'name': 'Learning Stipend',
                'description': '$1000-3000/year for courses, conferences, certifications',
                'coverage': 'Udemy, Coursera, bootcamps, conferences, books (not just job-related!)',
                'typical_cost': '$1000-3000/year',
                'priority': 'High'
            },
            'side_project_support': {
                'name': 'Side Project Support',
                'description': 'Budget + time allocation for personal passion projects',
                'coverage': '20% time for side projects, funding for materials/tools, mentorship',
                'typical_cost': '$500-2000/year + time',
                'priority': 'Medium'
            },
            'language_learning': {
                'name': 'Language Learning',
                'description': 'Duolingo/Rosetta Stone + tutoring for multilingual growth',
                'coverage': 'Language app subscriptions, 1-on-1 tutoring, immersion programs',
                'typical_cost': '$100-300/month',
                'priority': 'Low'
            },
            # Community & Purpose
            'volunteer_time_off': {
                'name': 'Volunteer Time Off (VTO)',
                'description': '40+ hours/year for causes you care about',
                'coverage': 'Paid time off for volunteering, company-organized service days, nonprofit support',
                'typical_cost': '40-80 paid hours/year',
                'priority': 'Medium'
            },
            'donation_matching': {
                'name': 'Donation Matching',
                'description': 'Company matches charitable donations 2:1 or 3:1',
                'coverage': 'Employer matches donations to nonprofits, up to $5000/year match',
                'typical_cost': 'Employer match varies',
                'priority': 'Low'
            },
            'social_impact_projects': {
                'name': 'Social Impact Projects',
                'description': 'Paid time to work on sustainability/DEI initiatives',
                'coverage': 'Dedicated time for ESG projects, DEI work, sustainability initiatives',
                'typical_cost': '5-10% of work time',
                'priority': 'Low'
            }
        }
        
        return defaults.get(benefit_type, {
            'name': benefit_type.replace('_', ' ').title(),
            'description': 'Benefit coverage',
            'coverage': 'Contact HR for details',
            'typical_cost': 'Varies',
            'priority': 'Unknown'
        })
    
    def generate_report(self, user_profile: Dict, recommendations: List[Dict], 
                       risk_assessment: Dict, output_path: str = 'benefit_report.pdf'):
        """Generate comprehensive PDF report"""
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Container for PDF elements
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading3'],
            fontSize=13,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=8,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        )
        
        # TITLE PAGE
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph("COMPREHENSIVE BENEFIT ASSESSMENT REPORT", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Date and info
        date_text = f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        story.append(Paragraph(date_text, ParagraphStyle('Date', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10)))
        story.append(Spacer(1, 0.5*inch))
        
        # User Profile Section
        story.append(Paragraph("EMPLOYEE PROFILE", heading_style))
        
        # Convert string values to floats for formatting
        annual_income = float(user_profile.get('annual_income', 0)) if user_profile.get('annual_income') else 0
        monthly_expenses = float(user_profile.get('monthly_expenses', 0)) if user_profile.get('monthly_expenses') else 0
        total_debt = float(user_profile.get('total_debt', 0)) if user_profile.get('total_debt') else 0
        savings = float(user_profile.get('savings', 0)) if user_profile.get('savings') else 0
        
        profile_data = [
            ['Name:', user_profile.get('name', 'N/A')],
            ['Age:', str(user_profile.get('age', 'N/A'))],
            ['Marital Status:', user_profile.get('marital_status', 'N/A').title()],
            ['Number of Children:', str(user_profile.get('num_children', 0))],
            ['Annual Income:', f"${annual_income:,.2f}"],
            ['Monthly Expenses:', f"${monthly_expenses:,.2f}"],
            ['Total Debt:', f"${total_debt:,.2f}"],
            ['Savings:', f"${savings:,.2f}"]
        ]
        
        profile_table = Table(profile_data, colWidths=[2*inch, 4*inch])
        profile_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0f8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(profile_table)
        story.append(Spacer(1, 0.3*inch))
        
        # RISK ASSESSMENT SECTION
        story.append(PageBreak())
        story.append(Paragraph("COMPREHENSIVE RISK ASSESSMENT", heading_style))
        story.append(Paragraph("Based on your profile and responses, here is your personalized risk analysis across 8 critical areas:", body_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Risk checkboxes - All 8 categories
        risk_data = [
            ['☐', '<b>Financial Risk</b>', risk_assessment.get('financial_risk', 'Medium'), 
             risk_assessment.get('financial_risk_detail', 'Monitor debt-to-income ratio')],
            ['☐', '<b>Health Risk</b>', risk_assessment.get('health_risk', 'Medium'),
             risk_assessment.get('health_risk_detail', 'Consider preventive care')],
            ['☐', '<b>Mental Health & Burnout</b>', risk_assessment.get('mental_health_risk', 'Medium'),
             risk_assessment.get('mental_health_risk_detail', 'Monitor stress and work-life balance')],
            ['☐', '<b>Family Risk</b>', risk_assessment.get('family_risk', 'Low'),
             risk_assessment.get('family_risk_detail', 'Ensure adequate life insurance')],
            ['☐', '<b>Retirement Risk</b>', risk_assessment.get('retirement_risk', 'Medium'),
             risk_assessment.get('retirement_risk_detail', 'Maximize retirement savings')],
            ['☐', '<b>Disability Risk</b>', risk_assessment.get('disability_risk', 'Medium'),
             risk_assessment.get('disability_risk_detail', 'Protect your income stream')],
            ['☐', '<b>Career Growth Risk</b>', risk_assessment.get('career_risk', 'Low'),
             risk_assessment.get('career_risk_detail', 'Invest in continuous learning')],
            ['☐', '<b>Work-Life Balance</b>', risk_assessment.get('worklife_risk', 'Medium'),
             risk_assessment.get('worklife_risk_detail', 'Prioritize flexibility and wellness')],
        ]
        
        risk_table = Table(risk_data, colWidths=[0.4*inch, 1.8*inch, 1*inch, 3.3*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            # Color code risk levels - Red for High/Critical, Orange for Medium
            ('TEXTCOLOR', (2, 0), (2, -1), colors.HexColor('#d32f2f')),
        ]))
        story.append(risk_table)
        story.append(Spacer(1, 0.3*inch))
        
        # RECOMMENDED BENEFITS
        story.append(PageBreak())
        story.append(Paragraph("RECOMMENDED BENEFITS", heading_style))
        story.append(Paragraph(
            "Based on your assessment, we recommend the following benefits. "
            "Check the boxes as you enroll in each benefit:",
            body_style
        ))
        story.append(Spacer(1, 0.2*inch))
        
        # Sort recommendations by priority/score
        sorted_recs = sorted(recommendations, key=lambda x: x.get('score', 0), reverse=True)
        
        for idx, rec in enumerate(sorted_recs[:10], 1):  # Top 10 recommendations
            benefit_type = rec.get('benefit', '').lower()
            benefit_info = self.fetch_benefit_details(benefit_type)
            
            # Benefit header with checkbox
            benefit_title = f"☐  {idx}. {benefit_info.get('name', benefit_type.title())}"
            story.append(Paragraph(benefit_title, subheading_style))
            
            # Use ML-calculated priority from recommendation, not hard-coded default
            ml_priority = rec.get('priority', 'N/A')
            
            # Benefit details table
            details_data = [
                ['Priority:', ml_priority],  # Use ML priority instead of default
                ['Confidence:', f"{rec.get('confidence', 0)*100:.0f}%"],
                ['Description:', benefit_info.get('description', 'N/A')],
                ['Coverage:', benefit_info.get('coverage', 'N/A')],
                ['Typical Cost:', benefit_info.get('typical_cost', 'Varies')],
                ['Why Recommended:', rec.get('rationale', 'Based on your profile')[:200]]
            ]
            
            details_table = Table(details_data, colWidths=[1.5*inch, 5*inch])
            details_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(details_table)
            story.append(Spacer(1, 0.15*inch))
        
        # ACTION ITEMS
        story.append(PageBreak())
        story.append(Paragraph("NEXT STEPS & ACTION ITEMS", heading_style))
        
        action_items = [
            "☐ Review this report carefully and discuss with your family",
            "☐ Compare benefit costs during open enrollment",
            "☐ Schedule a meeting with HR to ask questions",
            "☐ Enroll in selected benefits before the deadline",
            "☐ Update beneficiary information for all insurance policies",
            "☐ Set up automatic contributions for retirement accounts",
            "☐ Review and update benefits annually during open enrollment",
            "☐ Keep this report for your records"
        ]
        
        for item in action_items:
            story.append(Paragraph(item, ParagraphStyle('ActionItem', parent=body_style, leftIndent=20, spaceAfter=8)))
        
        story.append(Spacer(1, 0.3*inch))
        
        # DISCLAIMER
        story.append(Paragraph("DISCLAIMER", heading_style))
        disclaimer_text = (
            "This report is generated based on the information you provided and is intended for informational purposes only. "
            "It does not constitute financial, legal, or medical advice. Please consult with qualified professionals "
            "before making important financial or insurance decisions. Benefit availability, costs, and coverage details "
            "may vary. Contact your HR department or benefits administrator for specific plan information and enrollment deadlines."
        )
        story.append(Paragraph(disclaimer_text, ParagraphStyle('Disclaimer', parent=body_style, fontSize=9, textColor=colors.grey)))
        
        # Footer on all pages
        def add_page_number(canvas, doc):
            page_num = canvas.getPageNumber()
            text = f"Page {page_num}"
            canvas.setFont('Helvetica', 9)
            canvas.setFillColor(colors.grey)
            canvas.drawRightString(7.5*inch, 0.5*inch, text)
            canvas.drawString(0.75*inch, 0.5*inch, "Benefit Assessment Report - Confidential")
        
        # Build PDF
        doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
        print(f"✓ PDF report generated: {output_path}")
        return output_path


def calculate_risk_assessment(profile: Dict, answers: List) -> Dict:
    """Calculate comprehensive risk assessment based on user profile and answers"""
    
    # Convert string values to numbers with safe defaults
    age = int(profile.get('age', 30)) if profile.get('age') else 30
    income = float(profile.get('annual_income', 50000)) if profile.get('annual_income') else 50000
    debt = float(profile.get('total_debt', 0)) if profile.get('total_debt') else 0
    savings = float(profile.get('savings', 0)) if profile.get('savings') else 0
    children = int(profile.get('num_children', 0)) if profile.get('num_children') else 0
    monthly_expenses = float(profile.get('monthly_expenses', 3000)) if profile.get('monthly_expenses') else 3000
    
    # Analyze answer patterns for behavioral risks
    risk_behaviors = []
    wellness_score = 5  # 0-10 scale
    financial_literacy = 5
    
    for answer in answers:
        q_id = answer.get('question_id', '')
        choice = answer.get('choice', '')
        
        # Mental health & burnout signals
        if q_id == 'Q48_burnout_risk' and choice == 'A':
            wellness_score -= 3
            risk_behaviors.append('burnout_high')
        if q_id == 'Q42_mental_health' and choice == 'B':
            wellness_score -= 2
            risk_behaviors.append('mental_health_neglect')
            
        # Financial risk behaviors
        if q_id == 'Q44_emergency_fund' and choice == 'A':
            financial_literacy -= 3
            risk_behaviors.append('no_emergency_fund')
        if q_id == 'Q50_financial_literacy' and choice == 'A':
            financial_literacy -= 2
            risk_behaviors.append('low_financial_confidence')
        if q_id == 'Q43_student_debt' and choice == 'A':
            risk_behaviors.append('student_debt_burden')
            
        # Health neglect signals
        if q_id == 'Q55_health_neglect' and choice == 'A':
            risk_behaviors.append('health_neglect')
        if q_id == 'Q52_risky_behavior' and choice == 'A':
            risk_behaviors.append('engages_risky_activities')
            
        # Work-life balance
        if q_id == 'Q51_life_priorities' and choice == 'B':
            wellness_score += 1
    
    # 1. FINANCIAL RISK - Enhanced with behavioral data
    debt_to_income = debt / income if income > 0 else 0
    emergency_months = savings / monthly_expenses if monthly_expenses > 0 else 0
    
    financial_risk_score = 0
    if debt_to_income > 0.5:
        financial_risk_score += 40
    elif debt_to_income > 0.3:
        financial_risk_score += 25
    elif debt_to_income > 0.15:
        financial_risk_score += 10
        
    if emergency_months < 3:
        financial_risk_score += 35
    elif emergency_months < 6:
        financial_risk_score += 15
        
    if 'no_emergency_fund' in risk_behaviors:
        financial_risk_score += 10
    if 'student_debt_burden' in risk_behaviors:
        financial_risk_score += 15
    if financial_literacy < 3:
        financial_risk_score += 10
    
    if financial_risk_score > 60:
        financial_risk = 'Critical'
        financial_detail = f'URGENT: Debt-to-income {debt_to_income:.1%}, only {emergency_months:.1f} months emergency savings. Immediate action needed on debt reduction and emergency fund.'
    elif financial_risk_score > 40:
        financial_risk = 'High'
        financial_detail = f'Debt-to-income {debt_to_income:.1%}, {emergency_months:.1f} months savings. Priority: Build 6-month emergency fund and create debt payoff plan.'
    elif financial_risk_score > 20:
        financial_risk = 'Medium'
        financial_detail = f'Manageable debt levels. Continue building emergency fund to 6+ months. Consider financial coaching.'
    else:
        financial_risk = 'Low'
        financial_detail = f'Strong financial foundation. Debt-to-income {debt_to_income:.1%}, {emergency_months:.1f} months emergency fund. Focus on wealth building.'
    
    # 2. HEALTH & WELLNESS RISK - Enhanced with behavioral data
    health_risk_score = 0
    
    if age > 55:
        health_risk_score += 30
    elif age > 45:
        health_risk_score += 20
    elif age > 35:
        health_risk_score += 10
        
    if 'health_neglect' in risk_behaviors:
        health_risk_score += 25
    if 'engages_risky_activities' in risk_behaviors:
        health_risk_score += 20
    if wellness_score < 3:
        health_risk_score += 20
    elif wellness_score < 5:
        health_risk_score += 10
        
    if health_risk_score > 50:
        health_risk = 'Critical'
        health_detail = 'Serious health concerns identified. Schedule comprehensive physical immediately. Consider critical illness insurance.'
    elif health_risk_score > 35:
        health_risk = 'High'
        health_detail = 'Multiple health risk factors. Overdue for checkup. Preventive care and comprehensive insurance essential.'
    elif health_risk_score > 20:
        health_risk = 'Medium'
        health_detail = 'Moderate health risks. Schedule annual physical. Focus on preventive care and healthy habits.'
    else:
        health_risk = 'Low'
        health_detail = 'Good health indicators. Maintain preventive care routine and healthy lifestyle.'
    
    # 3. MENTAL HEALTH & BURNOUT RISK - NEW
    mental_risk_score = 0
    
    if 'burnout_high' in risk_behaviors:
        mental_risk_score += 40
    if 'mental_health_neglect' in risk_behaviors:
        mental_risk_score += 25
    if wellness_score < 3:
        mental_risk_score += 20
    if income > 100000 and 'burnout_high' in risk_behaviors:
        mental_risk_score += 15  # High achievers often neglect mental health
        
    if mental_risk_score > 50:
        mental_risk = 'Critical'
        mental_detail = 'URGENT: Severe burnout risk. Consider sabbatical, therapy, or mental health leave. Mental health stipend critical.'
    elif mental_risk_score > 35:
        mental_risk = 'High'
        mental_detail = 'High burnout risk. Invest in mental health support immediately. Unlimited life days and wellness benefits recommended.'
    elif mental_risk_score > 20:
        mental_risk = 'Medium'
        mental_detail = 'Watch for burnout signs. Consider therapy or wellness coaching. Take regular mental health days.'
    else:
        mental_risk = 'Low'
        mental_detail = 'Good mental health practices. Continue prioritizing wellness and work-life balance.'
    
    # 4. FAMILY & DEPENDENT RISK - Enhanced
    family_risk_score = 0
    
    if children > 2:
        family_risk_score += 30
    elif children > 0:
        family_risk_score += 20
        
    if debt > 100000 and children > 0:
        family_risk_score += 25
    elif debt > 50000 and children > 0:
        family_risk_score += 15
        
    income_per_dependent = income / max(1, children + 1)
    if children > 0 and income_per_dependent < 30000:
        family_risk_score += 20
        
    if family_risk_score > 50:
        family_risk = 'Critical'
        family_detail = f'URGENT: {children} dependents with limited resources. Life insurance REQUIRED. Dependent care FSA critical.'
    elif family_risk_score > 35:
        family_risk = 'High'
        family_detail = f'{children} dependent(s) require significant protection. Life insurance 8-10x income. Max out dependent care benefits.'
    elif family_risk_score > 20:
        family_risk = 'Medium'
        family_detail = f'Family protection needed. Ensure adequate life insurance and dependent care coverage.'
    else:
        family_risk = 'Low'
        family_detail = 'No or minimal dependents. Focus on personal financial security and future planning.'
    
    # 5. RETIREMENT RISK - Enhanced
    retirement_risk_score = 0
    
    years_to_retirement = max(65 - age, 1)
    retirement_target = income * age / 10
    retirement_gap = retirement_target - savings
    
    if age > 50 and savings < retirement_target * 0.5:
        retirement_risk_score += 45
    elif age > 40 and savings < retirement_target * 0.6:
        retirement_risk_score += 35
    elif age > 30 and savings < retirement_target * 0.7:
        retirement_risk_score += 25
    elif savings < retirement_target:
        retirement_risk_score += 15
        
    if debt_to_income > 0.3:
        retirement_risk_score += 15
    if financial_literacy < 3:
        retirement_risk_score += 10
        
    if retirement_risk_score > 50:
        retirement_risk = 'Critical'
        retirement_detail = f'URGENT: {years_to_retirement} years to retirement, ${retirement_gap:,.0f} behind target. Max out 401k immediately. Consider delaying retirement.'
    elif retirement_risk_score > 35:
        retirement_risk = 'High'
        retirement_detail = f'Behind on retirement savings. Need ${retirement_gap:,.0f} more. Increase 401k to 15%+ of income. Seek financial coaching.'
    elif retirement_risk_score > 20:
        retirement_risk = 'Medium'
        retirement_detail = f'Retirement on track but could improve. Target ${retirement_target:,.0f}. Consider increasing contributions 2-3%.'
    else:
        retirement_risk = 'Low'
        retirement_detail = f'Excellent retirement progress. On pace for comfortable retirement. Continue current strategy.'
    
    # 6. DISABILITY & INCOME PROTECTION RISK - Enhanced
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
    
    # 7. CAREER & GROWTH RISK - NEW
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
    
    # 8. WORK-LIFE BALANCE RISK - NEW
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


if __name__ == '__main__':
    # Test the report generator
    print("Testing PDF Report Generator with Supabase...")
    
    test_profile = {
        'name': 'John Doe',
        'age': 35,
        'marital_status': 'married',
        'num_children': 2,
        'annual_income': 85000,
        'monthly_expenses': 5500,
        'total_debt': 120000,
        'savings': 25000
    }
    
    test_recommendations = [
        {'benefit': 'medical', 'score': 0.95, 'confidence': 0.98, 'rationale': 'Essential health coverage for family'},
        {'benefit': '401k', 'score': 0.90, 'confidence': 0.95, 'rationale': 'Employer match available'},
        {'benefit': 'life_insurance', 'score': 0.88, 'confidence': 0.92, 'rationale': 'Protect family with 2 children'},
        {'benefit': 'dental', 'score': 0.85, 'confidence': 0.90, 'rationale': 'Family dental care needs'},
        {'benefit': 'disability', 'score': 0.82, 'confidence': 0.88, 'rationale': 'Income protection for family'},
    ]
    
    risk_assessment = calculate_risk_assessment(test_profile, [])
    
    generator = BenefitReportGenerator()
    generator.generate_report(test_profile, test_recommendations, risk_assessment, 'test_report.pdf')
    
    print("\n✓ Test report generated: test_report.pdf")
