"""
Adaptive Benefit Questionnaire Engine
Uses Information Theory and Bayesian Inference for optimal question selection.

Author: BullDawg Hackers
Date: October 2025
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
import math


# ============================================================================
# DATA STRUCTURES
# ============================================================================

class BenefitType(Enum):
    """All benefit types we can recommend"""
    MEDICAL = "medical"
    LIFE = "life_insurance"
    DISABILITY = "disability"
    DENTAL = "dental"
    VISION = "vision"
    LONG_TERM_CARE = "long_term_care"
    RETIREMENT_401K = "401k"
    HSA = "hsa"
    HEALTHCARE_FSA = "healthcare_fsa"
    DEPENDENT_CARE_FSA = "dependent_care_fsa"
    ACCIDENT = "accident_insurance"
    CRITICAL_ILLNESS = "critical_illness"
    HOSPITAL_INDEMNITY = "hospital_indemnity"
    LEGAL_SERVICES = "legal_services"
    IDENTITY_THEFT = "identity_theft"
    PET_INSURANCE = "pet_insurance"
    COMMUTER_BENEFITS = "commuter_benefits"


@dataclass
class UserDemographics:
    """Demographics from Google API"""
    name: str
    age: int
    gender: str
    location: str
    zip_code: str
    marital_status: Optional[str] = None
    num_children: int = 0
    

@dataclass
class UserFinancials:
    """Financial data from Plaid API"""
    annual_income: float
    monthly_expenses: float
    total_debt: float
    savings: float
    investment_accounts: float
    spending_categories: Dict[str, float] = field(default_factory=dict)
    income_volatility: float = 0.0  # Standard deviation


@dataclass
class Question:
    """Represents a binary choice question"""
    id: str
    text: str
    choice_a: str
    choice_b: str
    correlations_a: Dict[BenefitType, float]
    correlations_b: Dict[BenefitType, float]
    dimensions: List[str]
    expected_ig: float = 0.0


@dataclass
class Answer:
    """User's answer to a question"""
    question_id: str
    choice: str  # 'A' or 'B'
    confidence_weight: float = 1.0


@dataclass
class BenefitRecommendation:
    """Final recommendation for a benefit"""
    benefit_type: BenefitType
    score: float  # 0-100
    confidence: float  # 0-1
    priority: str  # 'critical', 'recommended', 'optional', 'not_needed'
    recommendation: Dict
    rationale: str


# ============================================================================
# CORRELATION MATRICES
# ============================================================================

# Define correlation matrices for each question
# Format: {BenefitType: correlation_coefficient}
# Positive = increases need, Negative = decreases need

QUESTION_CORRELATIONS = {
    "Q1_risk_behavior": {
        "A": {  # Adventure sports
            BenefitType.ACCIDENT: 0.72,
            BenefitType.LIFE: 0.58,
            BenefitType.DISABILITY: 0.51,
            BenefitType.CRITICAL_ILLNESS: 0.38,
            BenefitType.MEDICAL: 0.41,
        },
        "B": {  # Quiet activities
            BenefitType.VISION: 0.42,
            BenefitType.LONG_TERM_CARE: 0.31,
            BenefitType.ACCIDENT: -0.35,
        }
    },
    "Q2_health_consciousness": {
        "A": {  # Power through
            BenefitType.MEDICAL: -0.45,
            BenefitType.ACCIDENT: 0.38,
            BenefitType.CRITICAL_ILLNESS: 0.41,
        },
        "B": {  # Medicine and rest
            BenefitType.MEDICAL: 0.62,
            BenefitType.HEALTHCARE_FSA: 0.55,
            BenefitType.VISION: 0.48,
        }
    },
    "Q3_work_travel": {
        "A": {  # Rent car, explore
            BenefitType.ACCIDENT: 0.51,
            BenefitType.DISABILITY: 0.44,
            BenefitType.LIFE: 0.39,
        },
        "B": {  # Rideshare, hotel
            BenefitType.COMMUTER_BENEFITS: 0.48,
        }
    },
    "Q4_financial_planning": {
        "A": {  # Invest
            BenefitType.RETIREMENT_401K: 0.68,
            BenefitType.HSA: 0.61,
            BenefitType.MEDICAL: 0.35,  # HDHP preference
        },
        "B": {  # Pay debt / save
            BenefitType.DISABILITY: 0.54,
            BenefitType.LIFE: 0.48,
        }
    },
    "Q5_family_priorities": {
        "A": {  # College savings
            BenefitType.LIFE: 0.71,
            BenefitType.RETIREMENT_401K: 0.58,
        },
        "B": {  # Experiences now
            BenefitType.DEPENDENT_CARE_FSA: 0.61,
            BenefitType.HEALTHCARE_FSA: 0.47,
        }
    },
    "Q6_stress_management": {
        "A": {  # Exercise
            BenefitType.LONG_TERM_CARE: -0.22,
            BenefitType.MEDICAL: -0.15,
        },
        "B": {  # TV / games
            BenefitType.VISION: 0.44,
            BenefitType.LONG_TERM_CARE: 0.31,
        }
    },
    "Q7_career_commitment": {
        "A": {  # Would relocate
            BenefitType.LIFE: 0.42,
            BenefitType.DISABILITY: 0.38,
        },
        "B": {  # Only if necessary
            BenefitType.DEPENDENT_CARE_FSA: 0.48,
        }
    },
    "Q8_tech_adoption": {
        "A": {  # Early adopter
            BenefitType.HSA: 0.44,
            BenefitType.MEDICAL: 0.28,  # Telemedicine
        },
        "B": {  # Wait for reviews
            BenefitType.MEDICAL: 0.42,  # Traditional
        }
    },
    "Q9_pet_ownership": {
        "A": {  # Yes, have/want pets
            BenefitType.PET_INSURANCE: 0.91,
        },
        "B": {  # No pets
            BenefitType.PET_INSURANCE: -0.95,
        }
    },
    "Q10_dental_habits": {
        "A": {  # Preventive (2x/year)
            BenefitType.DENTAL: 0.71,
        },
        "B": {  # Reactive (only when problem)
            BenefitType.DENTAL: 0.38,
        }
    },
}


# ============================================================================
# QUESTION BANK
# ============================================================================

def build_question_bank() -> List[Question]:
    """Build the complete question bank with correlations"""
    questions = [
        Question(
            id="Q1_risk_behavior",
            text="Which sounds more appealing for a weekend?",
            choice_a="Skydiving / Rock climbing / Adventure sports",
            choice_b="Reading / Museum / Quiet activities",
            correlations_a=QUESTION_CORRELATIONS["Q1_risk_behavior"]["A"],
            correlations_b=QUESTION_CORRELATIONS["Q1_risk_behavior"]["B"],
            dimensions=["risk_tolerance", "activity_level", "accident_risk"],
            expected_ig=2.1
        ),
        Question(
            id="Q2_health_consciousness",
            text="How do you typically handle a headache?",
            choice_a="Ignore it and power through",
            choice_b="Take medicine immediately and rest",
            correlations_a=QUESTION_CORRELATIONS["Q2_health_consciousness"]["A"],
            correlations_b=QUESTION_CORRELATIONS["Q2_health_consciousness"]["B"],
            dimensions=["health_behavior", "medical_utilization"],
            expected_ig=1.9
        ),
        Question(
            id="Q3_work_travel",
            text="On a typical work trip, you'd rather:",
            choice_a="Rent a car and explore independently",
            choice_b="Use rideshare and stick to the hotel",
            correlations_a=QUESTION_CORRELATIONS["Q3_work_travel"]["A"],
            correlations_b=QUESTION_CORRELATIONS["Q3_work_travel"]["B"],
            dimensions=["independence", "risk_exposure"],
            expected_ig=1.8
        ),
        Question(
            id="Q4_financial_planning",
            text="You just got a $5,000 bonus. What do you do?",
            choice_a="Invest it for long-term growth",
            choice_b="Pay off debt or save for emergency",
            correlations_a=QUESTION_CORRELATIONS["Q4_financial_planning"]["A"],
            correlations_b=QUESTION_CORRELATIONS["Q4_financial_planning"]["B"],
            dimensions=["financial_planning", "risk_tolerance"],
            expected_ig=1.7
        ),
        Question(
            id="Q5_family_priorities",
            text="Imagine you have kids. Your top priority would be:",
            choice_a="Saving for their college education",
            choice_b="Making sure they have great experiences now",
            correlations_a=QUESTION_CORRELATIONS["Q5_family_priorities"]["A"],
            correlations_b=QUESTION_CORRELATIONS["Q5_family_priorities"]["B"],
            dimensions=["family_planning", "financial_priorities"],
            expected_ig=1.6
        ),
        Question(
            id="Q6_stress_management",
            text="After a stressful day, you prefer to:",
            choice_a="Exercise or do something active",
            choice_b="Watch TV or play video games",
            correlations_a=QUESTION_CORRELATIONS["Q6_stress_management"]["A"],
            correlations_b=QUESTION_CORRELATIONS["Q6_stress_management"]["B"],
            dimensions=["lifestyle", "health_behaviors"],
            expected_ig=1.5
        ),
        Question(
            id="Q7_career_commitment",
            text="If your dream job required relocation, would you:",
            choice_a="Move immediately for the opportunity",
            choice_b="Only consider if absolutely necessary",
            correlations_a=QUESTION_CORRELATIONS["Q7_career_commitment"]["A"],
            correlations_b=QUESTION_CORRELATIONS["Q7_career_commitment"]["B"],
            dimensions=["career_stability", "family_ties"],
            expected_ig=1.4
        ),
        Question(
            id="Q8_tech_adoption",
            text="When a new tech gadget launches, you:",
            choice_a="Pre-order and get it on day one",
            choice_b="Wait for reviews and discounts",
            correlations_a=QUESTION_CORRELATIONS["Q8_tech_adoption"]["A"],
            correlations_b=QUESTION_CORRELATIONS["Q8_tech_adoption"]["B"],
            dimensions=["innovation", "financial_prudence"],
            expected_ig=1.2
        ),
        Question(
            id="Q9_pet_ownership",
            text="Do you have or want pets?",
            choice_a="Yes, pets are family",
            choice_b="No, prefer not to have pets",
            correlations_a=QUESTION_CORRELATIONS["Q9_pet_ownership"]["A"],
            correlations_b=QUESTION_CORRELATIONS["Q9_pet_ownership"]["B"],
            dimensions=["pet_ownership"],
            expected_ig=1.1
        ),
        Question(
            id="Q10_dental_habits",
            text="How often do you visit the dentist?",
            choice_a="Twice a year or more (preventive)",
            choice_b="Only when there's a problem",
            correlations_a=QUESTION_CORRELATIONS["Q10_dental_habits"]["A"],
            correlations_b=QUESTION_CORRELATIONS["Q10_dental_habits"]["B"],
            dimensions=["preventive_care"],
            expected_ig=1.0
        ),
    ]
    
    return questions


# ============================================================================
# DEMOGRAPHIC PRIORS
# ============================================================================

def get_demographic_priors(demographics: UserDemographics) -> Dict[BenefitType, float]:
    """
    Calculate prior probabilities based on demographics.
    Returns scores 0-100 for each benefit.
    """
    priors = {}
    age = demographics.age
    has_children = demographics.num_children > 0
    
    # Medical - everyone needs, varies by age
    if age < 30:
        priors[BenefitType.MEDICAL] = 65
    elif age < 50:
        priors[BenefitType.MEDICAL] = 75
    else:
        priors[BenefitType.MEDICAL] = 85
    
    # Life Insurance - increases with age and family
    base_life = 40 + (age * 0.5)
    if has_children:
        base_life += 30
    if demographics.marital_status == "married":
        base_life += 10
    priors[BenefitType.LIFE] = min(base_life, 95)
    
    # Disability - peaks mid-career
    if age < 25:
        priors[BenefitType.DISABILITY] = 40
    elif age < 55:
        priors[BenefitType.DISABILITY] = 70
    else:
        priors[BenefitType.DISABILITY] = 50
    
    # Dental & Vision - moderate baseline
    priors[BenefitType.DENTAL] = 60
    priors[BenefitType.VISION] = 55
    
    # Long-term care - increases with age
    if age < 40:
        priors[BenefitType.LONG_TERM_CARE] = 10
    elif age < 55:
        priors[BenefitType.LONG_TERM_CARE] = 35
    else:
        priors[BenefitType.LONG_TERM_CARE] = 65
    
    # 401k - inversely related to age (urgency)
    priors[BenefitType.RETIREMENT_401K] = max(90 - age, 40)
    
    # HSA - moderate baseline
    priors[BenefitType.HSA] = 50
    
    # FSA - depends on family
    priors[BenefitType.HEALTHCARE_FSA] = 45
    if has_children:
        priors[BenefitType.DEPENDENT_CARE_FSA] = 75
    else:
        priors[BenefitType.DEPENDENT_CARE_FSA] = 10
    
    # Voluntary benefits - low baseline
    priors[BenefitType.ACCIDENT] = 30
    priors[BenefitType.CRITICAL_ILLNESS] = 25
    priors[BenefitType.HOSPITAL_INDEMNITY] = 20
    priors[BenefitType.LEGAL_SERVICES] = 15
    priors[BenefitType.IDENTITY_THEFT] = 25
    priors[BenefitType.PET_INSURANCE] = 20
    priors[BenefitType.COMMUTER_BENEFITS] = 30
    
    return priors


def adjust_priors_with_financials(
    priors: Dict[BenefitType, float],
    financials: UserFinancials
) -> Dict[BenefitType, float]:
    """
    Adjust prior probabilities based on financial data from Plaid.
    """
    adjusted = priors.copy()
    
    # Calculate financial metrics
    savings_rate = financials.savings / (financials.annual_income / 12) if financials.annual_income > 0 else 0
    debt_to_income = financials.total_debt / financials.annual_income if financials.annual_income > 0 else 0
    
    # High income → can afford more coverage
    if financials.annual_income > 120000:
        adjusted[BenefitType.LIFE] = min(adjusted[BenefitType.LIFE] + 10, 100)
        adjusted[BenefitType.DISABILITY] = min(adjusted[BenefitType.DISABILITY] + 10, 100)
    
    # High savings rate → HSA suitable
    if savings_rate > 3:  # 3+ months emergency fund
        adjusted[BenefitType.HSA] = min(adjusted[BenefitType.HSA] + 20, 100)
        adjusted[BenefitType.MEDICAL] = max(adjusted[BenefitType.MEDICAL] - 10, 30)  # HDHP OK
    
    # High debt → need disability protection
    if debt_to_income > 0.4:
        adjusted[BenefitType.DISABILITY] = min(adjusted[BenefitType.DISABILITY] + 15, 100)
        adjusted[BenefitType.LIFE] = min(adjusted[BenefitType.LIFE] + 15, 100)
    
    # Healthcare spending from Plaid
    healthcare_spend = financials.spending_categories.get("healthcare", 0)
    if healthcare_spend > 500:  # High monthly healthcare spending
        adjusted[BenefitType.MEDICAL] = min(adjusted[BenefitType.MEDICAL] + 15, 100)
        adjusted[BenefitType.HEALTHCARE_FSA] = min(adjusted[BenefitType.HEALTHCARE_FSA] + 20, 100)
    
    # Investment accounts → sophisticated investor
    if financials.investment_accounts > 50000:
        adjusted[BenefitType.RETIREMENT_401K] = min(adjusted[BenefitType.RETIREMENT_401K] + 15, 100)
        adjusted[BenefitType.HSA] = min(adjusted[BenefitType.HSA] + 10, 100)
    
    return adjusted


# ============================================================================
# INFORMATION GAIN CALCULATION
# ============================================================================

def calculate_entropy(benefit_scores: Dict[BenefitType, float]) -> float:
    """
    Calculate Shannon entropy of current benefit distribution.
    
    Args:
        benefit_scores: Dictionary of benefit scores (0-100)
    
    Returns:
        float: Entropy in bits
    """
    entropy = 0.0
    
    for score in benefit_scores.values():
        # Convert score to probability
        p = score / 100.0
        
        # Avoid log(0)
        if p > 0 and p < 1:
            entropy += -(p * math.log2(p) + (1-p) * math.log2(1-p))
    
    return entropy


def calculate_information_gain(
    question: Question,
    current_scores: Dict[BenefitType, float],
    question_history: List[str]
) -> float:
    """
    Calculate expected information gain for asking this question.
    
    Returns:
        float: Expected information gain in bits
    """
    # Skip if already asked
    if question.id in question_history:
        return 0.0
    
    current_entropy = calculate_entropy(current_scores)
    
    # Estimate probability of each choice (assume 50-50 for simplicity)
    p_choice_a = 0.5
    p_choice_b = 0.5
    
    # Simulate choosing A
    scores_if_a = simulate_answer(current_scores, question, 'A')
    entropy_if_a = calculate_entropy(scores_if_a)
    
    # Simulate choosing B
    scores_if_b = simulate_answer(current_scores, question, 'B')
    entropy_if_b = calculate_entropy(scores_if_b)
    
    # Expected entropy after asking
    expected_entropy = p_choice_a * entropy_if_a + p_choice_b * entropy_if_b
    
    # Information gain
    ig = current_entropy - expected_entropy
    
    return max(ig, 0.0)


def simulate_answer(
    current_scores: Dict[BenefitType, float],
    question: Question,
    choice: str
) -> Dict[BenefitType, float]:
    """Simulate what scores would be if user chose this answer"""
    simulated = current_scores.copy()
    
    correlations = question.correlations_a if choice == 'A' else question.correlations_b
    weight = 10.0  # Correlation weight
    
    for benefit, correlation in correlations.items():
        adjustment = correlation * weight
        simulated[benefit] = np.clip(simulated[benefit] + adjustment, 0, 100)
    
    return simulated


# ============================================================================
# ADAPTIVE QUESTIONING ENGINE
# ============================================================================

class AdaptiveQuestionnaireEngine:
    """Main engine for adaptive benefit questioning"""
    
    def __init__(
        self,
        demographics: UserDemographics,
        financials: UserFinancials
    ):
        self.demographics = demographics
        self.financials = financials
        self.question_bank = build_question_bank()
        
        # Initialize benefit scores with priors
        self.benefit_scores = get_demographic_priors(demographics)
        self.benefit_scores = adjust_priors_with_financials(self.benefit_scores, financials)
        
        # Track questioning
        self.questions_asked: List[Question] = []
        self.answers: List[Answer] = []
        self.question_history: List[str] = []
        
        # Configuration
        self.min_questions = 8
        self.max_questions = 15
        self.confidence_threshold = 0.85
        self.entropy_threshold = 0.3
    
    def select_next_question(self) -> Optional[Question]:
        """
        Select the next question with maximum information gain.
        
        Returns:
            Question object or None if stopping criterion met
        """
        # Check stopping criterion
        if self.should_stop():
            return None
        
        # Calculate IG for all unasked questions
        question_igs = []
        for question in self.question_bank:
            if question.id not in self.question_history:
                ig = calculate_information_gain(
                    question,
                    self.benefit_scores,
                    self.question_history
                )
                question_igs.append((question, ig))
        
        # No more questions available
        if not question_igs:
            return None
        
        # Select question with max IG
        best_question = max(question_igs, key=lambda x: x[1])[0]
        
        return best_question
    
    def process_answer(self, question: Question, choice: str):
        """
        Update benefit scores based on user's answer.
        
        Args:
            question: The question that was answered
            choice: 'A' or 'B'
        """
        # Create answer object
        answer = Answer(
            question_id=question.id,
            choice=choice,
            confidence_weight=1.0 + (len(self.answers) * 0.1)  # Increases with each question
        )
        
        # Get correlations for chosen answer
        correlations = question.correlations_a if choice == 'A' else question.correlations_b
        
        # Bayesian update of benefit scores
        weight = answer.confidence_weight * 8.0  # Base weight
        
        for benefit, correlation in correlations.items():
            adjustment = correlation * weight
            self.benefit_scores[benefit] = np.clip(
                self.benefit_scores[benefit] + adjustment,
                0,
                100
            )
        
        # Track
        self.questions_asked.append(question)
        self.answers.append(answer)
        self.question_history.append(question.id)
    
    def should_stop(self) -> bool:
        """
        Determine if we should stop questioning.
        
        Returns:
            bool: True if should stop
        """
        num_questions = len(self.questions_asked)
        
        # Must ask minimum questions
        if num_questions < self.min_questions:
            return False
        
        # Hit maximum
        if num_questions >= self.max_questions:
            return True
        
        # Check entropy
        current_entropy = calculate_entropy(self.benefit_scores)
        if current_entropy < self.entropy_threshold:
            return True
        
        # Check for diminishing returns
        if num_questions >= self.min_questions:
            # Calculate recent IG
            if len(self.questions_asked) >= 3:
                recent_questions = self.questions_asked[-3:]
                avg_recent_ig = sum(q.expected_ig for q in recent_questions) / 3
                if avg_recent_ig < 0.2:
                    return True
        
        return False
    
    def generate_recommendations(self) -> List[BenefitRecommendation]:
        """
        Generate final benefit recommendations based on scores.
        
        Returns:
            List of BenefitRecommendation objects
        """
        recommendations = []
        
        for benefit, score in self.benefit_scores.items():
            # Calculate confidence (inverse of entropy for this benefit)
            p = score / 100.0
            if p > 0 and p < 1:
                benefit_entropy = -(p * math.log2(p) + (1-p) * math.log2(1-p))
                confidence = 1.0 - (benefit_entropy / 1.0)  # Normalize to 0-1
            else:
                confidence = 1.0
            
            # Determine priority
            if score >= 75:
                priority = "critical"
            elif score >= 55:
                priority = "recommended"
            elif score >= 35:
                priority = "optional"
            else:
                priority = "not_needed"
            
            # Generate specific recommendation
            recommendation_details = self._generate_benefit_details(
                benefit,
                score,
                self.demographics,
                self.financials
            )
            
            # Generate rationale
            rationale = self._generate_rationale(benefit, score, priority)
            
            rec = BenefitRecommendation(
                benefit_type=benefit,
                score=round(score, 1),
                confidence=round(confidence, 2),
                priority=priority,
                recommendation=recommendation_details,
                rationale=rationale
            )
            
            recommendations.append(rec)
        
        # Sort by score descending
        recommendations.sort(key=lambda x: x.score, reverse=True)
        
        return recommendations
    
    def _generate_benefit_details(
        self,
        benefit: BenefitType,
        score: float,
        demographics: UserDemographics,
        financials: UserFinancials
    ) -> Dict:
        """Generate specific coverage details for a benefit"""
        
        if benefit == BenefitType.LIFE:
            # Life insurance: 8-10x income
            base = financials.annual_income * 8
            multiplier = 1 + (score - 50) / 100
            coverage = base * multiplier + (demographics.num_children * 100000)
            
            return {
                "coverage_amount": round(coverage, -3),
                "type": "Term Life",
                "duration": f"{min(65 - demographics.age, 30)} years",
                "estimated_monthly_premium": round(coverage / 10000 * 7, 0)
            }
        
        elif benefit == BenefitType.DISABILITY:
            monthly_benefit = (financials.annual_income / 12) * (0.60 + score/500)
            
            return {
                "monthly_benefit": round(monthly_benefit, -2),
                "elimination_period": "90 days",
                "benefit_period": "To age 65",
                "estimated_monthly_premium": round(monthly_benefit * 0.02, 0)
            }
        
        elif benefit == BenefitType.MEDICAL:
            if score >= 75:
                return {
                    "plan_type": "PPO Low Deductible",
                    "tier": "Gold",
                    "deductible": 1000,
                    "out_of_pocket_max": 5000,
                    "estimated_monthly_premium": 450
                }
            elif score >= 50:
                return {
                    "plan_type": "PPO Standard",
                    "tier": "Silver",
                    "deductible": 2500,
                    "out_of_pocket_max": 7000,
                    "estimated_monthly_premium": 350
                }
            else:
                return {
                    "plan_type": "HDHP + HSA",
                    "tier": "Bronze",
                    "deductible": 5000,
                    "out_of_pocket_max": 8000,
                    "estimated_monthly_premium": 250
                }
        
        elif benefit == BenefitType.HSA:
            # Max contribution based on family status
            max_contribution = 8300 if demographics.num_children > 0 else 4150
            recommended = min(max_contribution, financials.annual_income * 0.05)
            
            return {
                "recommended_annual_contribution": round(recommended, -2),
                "tax_savings": round(recommended * 0.22, 0),  # Assume 22% bracket
                "investment_options": "Yes"
            }
        
        elif benefit == BenefitType.RETIREMENT_401K:
            # Contribute enough to get full match
            recommended_rate = min(15, max(6, score / 6))  # 6-15% of income
            
            return {
                "recommended_contribution_rate": f"{round(recommended_rate)}%",
                "annual_amount": round(financials.annual_income * recommended_rate / 100, -2),
                "employer_match": "Up to 6%"
            }
        
        else:
            # Generic recommendation
            return {
                "coverage": "Standard" if score >= 50 else "Basic",
                "estimated_monthly_premium": round(score * 0.5, 0)
            }
    
    def _generate_rationale(self, benefit: BenefitType, score: float, priority: str) -> str:
        """Generate human-readable rationale for recommendation"""
        
        if benefit == BenefitType.LIFE and priority == "critical":
            return f"High coverage recommended based on income (${self.financials.annual_income:,.0f}), {self.demographics.num_children} dependent(s), and financial obligations."
        
        elif benefit == BenefitType.DISABILITY and priority in ["critical", "recommended"]:
            return "Income protection is important given your career stage and limited emergency savings."
        
        elif benefit == BenefitType.MEDICAL and score >= 75:
            return "Comprehensive medical coverage recommended based on predicted healthcare utilization and preventive care needs."
        
        elif benefit == BenefitType.HSA and score >= 55:
            return "HSA recommended for tax advantages and long-term healthcare savings potential."
        
        elif benefit == BenefitType.PET_INSURANCE and priority == "not_needed":
            return "No pet ownership indicated or planned."
        
        else:
            return f"Recommendation based on your profile and preferences (score: {score:.0f}/100)."


# ============================================================================
# MAIN EXECUTION FLOW
# ============================================================================

def run_adaptive_questionnaire(
    demographics: UserDemographics,
    financials: UserFinancials
) -> Dict:
    """
    Main function to run the adaptive questionnaire.
    
    Args:
        demographics: User demographic data from Google API
        financials: User financial data from Plaid API
    
    Returns:
        Dict containing recommendations and metadata
    """
    # Initialize engine
    engine = AdaptiveQuestionnaireEngine(demographics, financials)
    
    print(f"\n{'='*60}")
    print(f"ADAPTIVE BENEFIT QUESTIONNAIRE")
    print(f"{'='*60}")
    print(f"User: {demographics.name}, Age: {demographics.age}")
    print(f"Income: ${financials.annual_income:,.0f}")
    print(f"\nInitial entropy: {calculate_entropy(engine.benefit_scores):.2f} bits")
    print(f"{'='*60}\n")
    
    # Adaptive questioning loop
    question_num = 1
    while True:
        # Select next question
        next_question = engine.select_next_question()
        
        if next_question is None:
            print(f"\n✓ Stopping criterion met after {len(engine.questions_asked)} questions")
            break
        
        # Present question (in production, this would be UI)
        print(f"\nQuestion {question_num}:")
        print(f"{next_question.text}")
        print(f"  A) {next_question.choice_a}")
        print(f"  B) {next_question.choice_b}")
        
        # Simulate user answer (in production, get from UI)
        # For demo, randomly choose
        import random
        choice = random.choice(['A', 'B'])
        print(f"→ User selected: {choice}")
        
        # Process answer
        engine.process_answer(next_question, choice)
        
        # Show entropy reduction
        current_entropy = calculate_entropy(engine.benefit_scores)
        print(f"  Entropy: {current_entropy:.2f} bits")
        
        question_num += 1
    
    # Generate recommendations
    recommendations = engine.generate_recommendations()
    
    # Format output
    output = {
        "user": {
            "name": demographics.name,
            "age": demographics.age,
            "income": financials.annual_income
        },
        "algorithm_stats": {
            "questions_asked": len(engine.questions_asked),
            "final_entropy": round(calculate_entropy(engine.benefit_scores), 2),
            "entropy_reduction": round(
                calculate_entropy(get_demographic_priors(demographics)) - 
                calculate_entropy(engine.benefit_scores),
                2
            )
        },
        "recommendations": {
            "critical": [],
            "recommended": [],
            "optional": [],
            "not_needed": []
        }
    }
    
    # Organize by priority
    for rec in recommendations:
        rec_dict = {
            "benefit": rec.benefit_type.value,
            "score": rec.score,
            "confidence": rec.confidence,
            "details": rec.recommendation,
            "rationale": rec.rationale
        }
        output["recommendations"][rec.priority].append(rec_dict)
    
    return output


# ============================================================================
# DEMO / TESTING
# ============================================================================

if __name__ == "__main__":
    # Sample data (in production, from Google + Plaid APIs)
    demo_demographics = UserDemographics(
        name="John Smith",
        age=35,
        gender="male",
        location="Atlanta, GA",
        zip_code="30301",
        marital_status="married",
        num_children=2
    )
    
    demo_financials = UserFinancials(
        annual_income=120000,
        monthly_expenses=5500,
        total_debt=250000,  # Mortgage
        savings=25000,
        investment_accounts=45000,
        spending_categories={
            "healthcare": 350,
            "groceries": 800,
            "transportation": 400
        }
    )
    
    # Run questionnaire
    results = run_adaptive_questionnaire(demo_demographics, demo_financials)
    
    # Print results
    print(f"\n{'='*60}")
    print("FINAL RECOMMENDATIONS")
    print(f"{'='*60}\n")
    
    print(f"Questions Asked: {results['algorithm_stats']['questions_asked']}")
    print(f"Entropy Reduction: {results['algorithm_stats']['entropy_reduction']:.2f} bits\n")
    
    for priority in ["critical", "recommended", "optional"]:
        if results["recommendations"][priority]:
            print(f"\n{priority.upper()}:")
            for rec in results["recommendations"][priority]:
                print(f"\n  • {rec['benefit'].replace('_', ' ').title()}")
                print(f"    Score: {rec['score']}/100 (Confidence: {rec['confidence']*100:.0f}%)")
                print(f"    {rec['rationale']}")
                if rec['details']:
                    print(f"    Details: {json.dumps(rec['details'], indent=6)}")
    
    print(f"\n{'='*60}\n")
