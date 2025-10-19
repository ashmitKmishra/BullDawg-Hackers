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
                       risk_assessment: Dict, output_path: str = 'benefit_report.pdf'):
        """Generate comprehensive PDF report with proper formatting"""
        
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
            leading=20,
            borderColor=BURGUNDY,
            borderWidth=1,
            borderPadding=8,
            backColor=colors.HexColor('#f8f9fa')
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
            textColor=colors.grey,
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
            ["Marital Status:", user_profile.get('marital_status', 'N/A').title()],
            ["Number of Children:", str(user_profile.get('num_children', 0))],
            ["Annual Income:", f"${user_profile.get('annual_income', 0):,}"],
        ]
        
        profile_table = Table(profile_data, colWidths=[2.5*inch, 4*inch])
        profile_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (0, -1), DARK_BURGUNDY),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(profile_table)
        story.append(Spacer(1, 0.3*inch))
        
        # COMPREHENSIVE RISK ASSESSMENT - Enhanced Section
        story.append(PageBreak())
        story.append(Paragraph("COMPREHENSIVE RISK ASSESSMENT", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        intro_text = """This comprehensive analysis evaluates your risk profile across eight critical dimensions 
        of financial and personal wellbeing. Each category has been carefully assessed based on your demographic 
        information, financial situation, and lifestyle indicators to provide personalized risk mitigation strategies."""
        story.append(Paragraph(intro_text, body_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Risk Assessment Categories
        risk_categories = [
            ('Financial Risk', risk_assessment.get('financial_risk', 'Medium'), 
             risk_assessment.get('financial_detail', 'Moderate financial exposure')),
            ('Health & Wellness', risk_assessment.get('health_risk', 'Medium'),
             risk_assessment.get('health_detail', 'Standard health considerations')),
            ('Mental Health & Burnout', risk_assessment.get('mental_health_risk', 'Medium'),
             risk_assessment.get('mental_health_detail', 'Moderate stress factors')),
            ('Family & Dependents', risk_assessment.get('family_risk', 'Low'),
             risk_assessment.get('family_detail', 'Family protection considerations')),
            ('Retirement Readiness', risk_assessment.get('retirement_risk', 'Medium'),
             risk_assessment.get('retirement_detail', 'Retirement planning status')),
            ('Disability Protection', risk_assessment.get('disability_risk', 'Medium'),
             risk_assessment.get('disability_detail', 'Income protection needs')),
            ('Career & Growth', risk_assessment.get('career_risk', 'Low'),
             risk_assessment.get('career_detail', 'Professional development status')),
            ('Work-Life Balance', risk_assessment.get('worklife_risk', 'Medium'),
             risk_assessment.get('worklife_detail', 'Balance and wellness factors'))
        ]
        
        for category_name, risk_level, detail in risk_categories:
            # Risk category header
            story.append(Paragraph(f"<b>{category_name}</b>", subheading_style))
            
            # Risk level with color coding
            risk_color = {
                'Low': colors.green,
                'Medium': colors.orange,
                'High': colors.red,
                'Critical': DARK_BURGUNDY
            }.get(risk_level, colors.grey)
            
            risk_table_data = [[
                Paragraph(f"<b>Risk Level:</b> {risk_level}", body_style),
                ""
            ]]
            
            risk_table = Table(risk_table_data, colWidths=[6.5*inch])
            risk_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), risk_color),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('ROUNDEDCORNERS', [5, 5, 5, 5]),
            ]))
            story.append(risk_table)
            story.append(Spacer(1, 0.05*inch))
            
            # Risk details
            story.append(Paragraph(detail, body_style))
            story.append(Spacer(1, 0.15*inch))
        
        # Recommendations Section
        story.append(PageBreak())
        story.append(Paragraph("PERSONALIZED BENEFIT RECOMMENDATIONS", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Group by priority
        critical = [r for r in recommendations if r.get('priority') == 'CRITICAL']
        recommended = [r for r in recommendations if r.get('priority') == 'RECOMMENDED']
        optional = [r for r in recommendations if r.get('priority') == 'OPTIONAL']
        
        # Critical Benefits
        if critical:
            story.append(Paragraph("🔴 CRITICAL PRIORITIES", subheading_style))
            story.append(Spacer(1, 0.05*inch))
            story.append(Paragraph("These benefits are essential for your situation and should be prioritized immediately.", body_style))
            story.append(Spacer(1, 0.1*inch))
            
            for rec in critical:
                self._add_benefit_recommendation(story, rec, body_style, small_text)
        
        # Recommended Benefits
        if recommended:
            story.append(Paragraph("🟡 STRONGLY RECOMMENDED", subheading_style))
            story.append(Spacer(1, 0.05*inch))
            story.append(Paragraph("These benefits provide significant value and protection for your circumstances.", body_style))
            story.append(Spacer(1, 0.1*inch))
            
            for rec in recommended:
                self._add_benefit_recommendation(story, rec, body_style, small_text)
        
        # Optional Benefits
        if optional:
            story.append(Paragraph("🟢 OPTIONAL CONSIDERATIONS", subheading_style))
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
        benefit_type = rec.get('benefit_type', '')
        benefit_info = self.fetch_benefit_details(benefit_type)
        
        # Benefit name and score
        benefit_name = benefit_info.get('name', benefit_type.replace('_', ' ').title())
        score = rec.get('score', 0)
        confidence = rec.get('confidence', 0)
        
        # Create benefit header table
        header_data = [[
            Paragraph(f"<b>{benefit_name}</b>", body_style),
            Paragraph(f"<b>Score: {score:.0f}/100</b>", ParagraphStyle('Score', parent=body_style, alignment=TA_CENTER, textColor=BURGUNDY))
        ]]
        
        header_table = Table(header_data, colWidths=[5*inch, 1.5*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BOX', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 0.05*inch))
        
        # Benefit details
        description = benefit_info.get('description', 'N/A')
        cost = benefit_info.get('typical_cost', 'Varies')
        rationale = rec.get('rationale', 'Recommended based on your profile')
        
        detail_text = f"<b>Description:</b> {description}<br/><b>Typical Cost:</b> {cost}<br/><b>Why Recommended:</b> {rationale}"
        story.append(Paragraph(detail_text, small_text))
        story.append(Spacer(1, 0.15*inch))

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
    
    generator.generate_report(user_profile, recommendations, risk_assessment, 'test_report_v2.pdf')
