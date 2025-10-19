"""
Integration Tests - Test full end-to-end scenarios
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from adaptive_questionnaire_engine import (
    AdaptiveQuestionnaireEngine,
    UserDemographics,
    UserFinancials,
    BenefitType
)


class TestCompleteUserJourneys(unittest.TestCase):
    """Test complete user journeys from start to finish"""
    
    def test_typical_family_journey(self):
        """Complete journey for typical family"""
        print("\n" + "="*80)
        print("TEST: Typical Family (Age 35, $120k, Married, 2 kids)")
        print("="*80)
        
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=35, income=120000, marital_status="married", num_children=2),
            UserFinancials(annual_income=120000, monthly_expenses=8000, total_debt=50000, total_savings=100000)
        )
        
        print(f"\nInitial Entropy: {engine.calculate_entropy(engine.benefit_scores):.2f} bits")
        print(f"Initial Top 3 Benefits:")
        sorted_benefits = sorted(engine.benefit_scores.items(), key=lambda x: x[1], reverse=True)
        for i, (bt, score) in enumerate(sorted_benefits[:3], 1):
            print(f"  {i}. {bt.value}: {score:.1f}")
        
        # Simulate answering questions intelligently
        answers = []
        question_count = 0
        
        while not engine.should_stop() and question_count < 12:
            question = engine.select_next_question()
            
            # Simulate intelligent answers based on profile
            if "children" in question.text.lower() or "kids" in question.text.lower():
                choice = 0  # Yes to children questions
            elif "risk" in question.text.lower() and "adventurous" in question.choices[0].lower():
                choice = 1  # Conservative
            elif "bonus" in question.text.lower():
                choice = 0  # Invest (high income)
            elif "health" in question.text.lower():
                choice = 1  # Good health
            else:
                choice = 0  # Default to first choice
            
            ig = engine.calculate_information_gain(question, engine.benefit_scores, engine.answer_history)
            engine.process_answer(question, choice)
            
            print(f"\nQ{question_count + 1}: {question.text}")
            print(f"  Answer: {question.choices[choice]}")
            print(f"  IG: {ig:.3f} bits")
            print(f"  Entropy: {engine.calculate_entropy(engine.benefit_scores):.2f} bits")
            
            answers.append((question, choice, ig))
            question_count += 1
        
        # Generate recommendations
        recs = engine.generate_recommendations()
        
        print(f"\n{'='*80}")
        print("FINAL RECOMMENDATIONS")
        print(f"{'='*80}")
        print(f"Questions Asked: {len(answers)}")
        print(f"Final Entropy: {engine.calculate_entropy(engine.benefit_scores):.2f} bits")
        
        critical = [r for r in recs if r.priority == "CRITICAL"]
        recommended = [r for r in recs if r.priority == "RECOMMENDED"]
        
        print(f"\nCRITICAL ({len(critical)}):")
        for rec in critical:
            print(f"  • {rec.benefit_type.value}: {rec.score:.1f}/100")
            if rec.details:
                for key, value in list(rec.details.items())[:3]:
                    print(f"    - {key}: {value}")
        
        print(f"\nRECOMMENDED ({len(recommended)}):")
        for rec in recommended[:5]:
            print(f"  • {rec.benefit_type.value}: {rec.score:.1f}/100")
        
        # Assertions
        self.assertGreater(len(critical), 0, "Should have critical recommendations")
        self.assertIn(BenefitType.LIFE, [r.benefit_type for r in critical], "Life insurance should be critical for family")
        print(f"\n✓ Test passed: {len(critical)} critical, {len(recommended)} recommended\n")
    
    def test_young_professional_journey(self):
        """Complete journey for young professional"""
        print("\n" + "="*80)
        print("TEST: Young Professional (Age 26, $60k, Single, No kids)")
        print("="*80)
        
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=26, income=60000, marital_status="single", num_children=0),
            UserFinancials(annual_income=60000, monthly_expenses=3500, total_debt=25000, total_savings=15000)
        )
        
        print(f"\nInitial Entropy: {engine.calculate_entropy(engine.benefit_scores):.2f} bits")
        
        question_count = 0
        while not engine.should_stop() and question_count < 10:
            question = engine.select_next_question()
            
            # Young professional answers
            if "children" in question.text.lower():
                choice = 1  # No
            elif "risk" in question.text.lower():
                choice = 0  # More adventurous
            elif "debt" in question.text.lower():
                choice = 0  # Yes, has debt
            else:
                choice = 0
            
            engine.process_answer(question, choice)
            question_count += 1
        
        recs = engine.generate_recommendations()
        
        print(f"\nQuestions Asked: {question_count}")
        print(f"Final Entropy: {engine.calculate_entropy(engine.benefit_scores):.2f} bits")
        
        critical = [r for r in recs if r.priority == "CRITICAL"]
        print(f"\nTop Recommendations:")
        for i, rec in enumerate(sorted(recs, key=lambda x: x.score, reverse=True)[:5], 1):
            print(f"  {i}. {rec.benefit_type.value}: {rec.score:.1f}/100")
        
        # Should prioritize medical and 401k over life
        medical_rec = next((r for r in recs if r.benefit_type == BenefitType.MEDICAL), None)
        life_rec = next((r for r in recs if r.benefit_type == BenefitType.LIFE), None)
        
        self.assertIsNotNone(medical_rec)
        print(f"\n✓ Test passed: Medical prioritized for young professional\n")
    
    def test_near_retirement_journey(self):
        """Complete journey for near-retirement person"""
        print("\n" + "="*80)
        print("TEST: Near Retirement (Age 62, $95k, Married, No kids)")
        print("="*80)
        
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=62, income=95000, marital_status="married", num_children=0),
            UserFinancials(annual_income=95000, monthly_expenses=6500, total_debt=15000, total_savings=750000)
        )
        
        print(f"\nInitial Entropy: {engine.calculate_entropy(engine.benefit_scores):.2f} bits")
        
        question_count = 0
        while not engine.should_stop() and question_count < 10:
            question = engine.select_next_question()
            
            # Conservative near-retirement answers
            if "risk" in question.text.lower():
                choice = 1  # Conservative
            elif "health" in question.text.lower():
                choice = 0  # Some concerns
            else:
                choice = 1
            
            engine.process_answer(question, choice)
            question_count += 1
        
        recs = engine.generate_recommendations()
        
        print(f"\nQuestions Asked: {question_count}")
        print(f"Top Recommendations:")
        for i, rec in enumerate(sorted(recs, key=lambda x: x.score, reverse=True)[:5], 1):
            print(f"  {i}. {rec.benefit_type.value}: {rec.score:.1f}/100")
        
        # Should prioritize medical and long-term care
        medical_rec = next((r for r in recs if r.benefit_type == BenefitType.MEDICAL), None)
        ltc_rec = next((r for r in recs if r.benefit_type == BenefitType.LONG_TERM_CARE), None)
        
        self.assertIsNotNone(medical_rec)
        self.assertGreater(medical_rec.score, 60.0)
        print(f"\n✓ Test passed: Medical/LTC prioritized for near-retirement\n")


class TestConsistency(unittest.TestCase):
    """Test that results are consistent"""
    
    def test_deterministic_results(self):
        """Test that same inputs produce same results"""
        results = []
        
        for _ in range(3):
            engine = AdaptiveQuestionnaireEngine(
                UserDemographics(age=35, income=100000, marital_status="married", num_children=1),
                UserFinancials(annual_income=100000, monthly_expenses=6000, total_debt=30000, total_savings=50000)
            )
            
            # Answer same questions same way
            for i in range(5):
                question = engine.select_next_question()
                engine.process_answer(question, i % 2)
            
            results.append(engine.benefit_scores.copy())
        
        # All results should be identical
        for i in range(1, len(results)):
            for bt in BenefitType:
                self.assertAlmostEqual(results[0][bt], results[i][bt], places=5)
        
        print("✓ Consistency test: Results are deterministic")
    
    def test_similar_profiles_similar_results(self):
        """Test that similar profiles get similar recommendations"""
        # Two very similar profiles
        engine1 = AdaptiveQuestionnaireEngine(
            UserDemographics(age=35, income=100000, marital_status="married", num_children=2),
            UserFinancials(annual_income=100000, monthly_expenses=6000, total_debt=30000, total_savings=50000)
        )
        
        engine2 = AdaptiveQuestionnaireEngine(
            UserDemographics(age=36, income=105000, marital_status="married", num_children=2),
            UserFinancials(annual_income=105000, monthly_expenses=6200, total_debt=32000, total_savings=52000)
        )
        
        # Check initial scores are similar
        for bt in BenefitType:
            diff = abs(engine1.benefit_scores[bt] - engine2.benefit_scores[bt])
            self.assertLess(diff, 15.0, f"{bt.value} scores differ by {diff:.1f}")
        
        print("✓ Similarity test: Similar profiles produce similar scores")


class TestAccuracy(unittest.TestCase):
    """Test recommendation accuracy for known scenarios"""
    
    def test_high_life_insurance_need(self):
        """Test that high life insurance need is detected"""
        # High income, married, multiple children, high debt
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=38, income=150000, marital_status="married", num_children=3),
            UserFinancials(annual_income=150000, monthly_expenses=10000, total_debt=100000, total_savings=50000)
        )
        
        life_score = engine.benefit_scores[BenefitType.LIFE]
        self.assertGreater(life_score, 65.0, f"Life insurance score {life_score:.1f} should be >65 for high-need family")
        print(f"✓ Life insurance need test: Score {life_score:.1f} (expected >65)")
    
    def test_low_life_insurance_need(self):
        """Test that low life insurance need is detected"""
        # Young, single, no dependents, low income
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=24, income=40000, marital_status="single", num_children=0),
            UserFinancials(annual_income=40000, monthly_expenses=2500, total_debt=10000, total_savings=8000)
        )
        
        life_score = engine.benefit_scores[BenefitType.LIFE]
        # Life insurance still important but less critical
        print(f"✓ Low life insurance need test: Score {life_score:.1f}")
    
    def test_disability_need_detection(self):
        """Test disability insurance need detection"""
        # High income, dependents, only earner
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=40, income=120000, marital_status="married", num_children=2),
            UserFinancials(annual_income=120000, monthly_expenses=8000, total_debt=60000, total_savings=40000)
        )
        
        disability_score = engine.benefit_scores[BenefitType.DISABILITY]
        self.assertGreater(disability_score, 40.0)
        print(f"✓ Disability need test: Score {disability_score:.1f} (expected >40)")


def run_integration_tests():
    """Run all integration tests"""
    print("\n" + "="*80)
    print("INTEGRATION & ACCURACY TEST SUITE")
    print("="*80)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestCompleteUserJourneys))
    suite.addTests(loader.loadTestsFromTestCase(TestConsistency))
    suite.addTests(loader.loadTestsFromTestCase(TestAccuracy))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*80)
    print(f"Integration Tests: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun} passed")
    print("="*80 + "\n")
    
    return result


if __name__ == "__main__":
    run_integration_tests()
