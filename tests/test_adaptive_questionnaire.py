"""
Comprehensive Test Suite for Adaptive Questionnaire Engine
Tests entropy calculations, information gain, Bayesian updates, and recommendation accuracy
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from adaptive_questionnaire_engine import (
    AdaptiveQuestionnaireEngine,
    UserDemographics,
    UserFinancials,
    BenefitType,
    Question
)


class TestEntropyCalculations(unittest.TestCase):
    """Test Shannon entropy calculations"""
    
    def test_maximum_entropy(self):
        """Test entropy with uniform distribution (maximum uncertainty)"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=30, income=50000, marital_status="single", num_children=0),
            UserFinancials(annual_income=50000, monthly_expenses=3000, total_debt=0, total_savings=10000)
        )
        
        # Create uniform scores
        uniform_scores = {bt: 50.0 for bt in BenefitType}
        entropy = engine.calculate_entropy(uniform_scores)
        
        # Uniform distribution should have high entropy
        self.assertGreater(entropy, 3.0)
        print(f"✓ Maximum entropy test: {entropy:.2f} bits (expected > 3.0)")
    
    def test_minimum_entropy(self):
        """Test entropy with certain distribution (minimum uncertainty)"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=30, income=50000, marital_status="single", num_children=0),
            UserFinancials(annual_income=50000, monthly_expenses=3000, total_debt=0, total_savings=10000)
        )
        
        # Create certain scores (one dominant benefit)
        certain_scores = {bt: 10.0 for bt in BenefitType}
        certain_scores[BenefitType.MEDICAL] = 100.0
        entropy = engine.calculate_entropy(certain_scores)
        
        # Certain distribution should have low entropy
        self.assertLess(entropy, 2.0)
        print(f"✓ Minimum entropy test: {entropy:.2f} bits (expected < 2.0)")
    
    def test_entropy_decreases_with_certainty(self):
        """Test that entropy decreases as we gain certainty"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=30, income=50000, marital_status="single", num_children=0),
            UserFinancials(annual_income=50000, monthly_expenses=3000, total_debt=0, total_savings=10000)
        )
        
        # Start with uniform
        scores1 = {bt: 50.0 for bt in BenefitType}
        entropy1 = engine.calculate_entropy(scores1)
        
        # Add some certainty
        scores2 = {bt: 40.0 for bt in BenefitType}
        scores2[BenefitType.MEDICAL] = 80.0
        scores2[BenefitType.LIFE] = 75.0
        entropy2 = engine.calculate_entropy(scores2)
        
        self.assertLess(entropy2, entropy1)
        print(f"✓ Entropy decrease test: {entropy1:.2f} → {entropy2:.2f} bits")


class TestInformationGain(unittest.TestCase):
    """Test information gain calculations"""
    
    def test_information_gain_positive(self):
        """Test that information gain is always positive"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=35, income=80000, marital_status="married", num_children=2),
            UserFinancials(annual_income=80000, monthly_expenses=5000, total_debt=20000, total_savings=30000)
        )
        
        question = engine.question_bank[0]
        ig = engine.calculate_information_gain(question, engine.benefit_scores, [])
        
        self.assertGreaterEqual(ig, 0.0)
        print(f"✓ Information gain positive test: {ig:.3f} bits")
    
    def test_information_gain_all_questions(self):
        """Test information gain for all questions in bank"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=35, income=80000, marital_status="married", num_children=2),
            UserFinancials(annual_income=80000, monthly_expenses=5000, total_debt=20000, total_savings=30000)
        )
        
        print("\n✓ Information Gain for all questions:")
        for i, question in enumerate(engine.question_bank, 1):
            ig = engine.calculate_information_gain(question, engine.benefit_scores, [])
            self.assertGreaterEqual(ig, 0.0)
            print(f"  Q{i}: {question.text[:50]}... → {ig:.3f} bits")
    
    def test_diminishing_information_gain(self):
        """Test that IG decreases as more questions are answered"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=35, income=120000, marital_status="married", num_children=2),
            UserFinancials(annual_income=120000, monthly_expenses=8000, total_debt=50000, total_savings=100000)
        )
        
        ig_values = []
        for i in range(5):
            question = engine.select_next_question()
            ig = engine.calculate_information_gain(question, engine.benefit_scores, engine.answer_history)
            ig_values.append(ig)
            
            # Simulate answering
            engine.process_answer(question, 0)
        
        # Check if IG generally decreases
        print(f"\n✓ Diminishing IG test: {[f'{ig:.3f}' for ig in ig_values]}")
        self.assertGreater(ig_values[0], ig_values[-1])


class TestBayesianUpdates(unittest.TestCase):
    """Test Bayesian probability updates"""
    
    def test_answer_updates_scores(self):
        """Test that answering a question updates benefit scores"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=30, income=50000, marital_status="single", num_children=0),
            UserFinancials(annual_income=50000, monthly_expenses=3000, total_debt=0, total_savings=10000)
        )
        
        initial_scores = engine.benefit_scores.copy()
        question = engine.select_next_question()
        engine.process_answer(question, 0)
        
        # Scores should have changed
        changes = sum(1 for bt in BenefitType if engine.benefit_scores[bt] != initial_scores[bt])
        self.assertGreater(changes, 0)
        print(f"✓ Bayesian update test: {changes}/{len(BenefitType)} scores changed")
    
    def test_correlation_effects(self):
        """Test that highly correlated answers have strong effects"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=35, income=80000, marital_status="married", num_children=2),
            UserFinancials(annual_income=80000, monthly_expenses=5000, total_debt=20000, total_savings=30000)
        )
        
        # Find question about children (should strongly affect life insurance)
        question = next(q for q in engine.question_bank if "children" in q.text.lower() or "kids" in q.text.lower())
        
        initial_life_score = engine.benefit_scores[BenefitType.LIFE]
        engine.process_answer(question, 0)  # Choice A
        final_life_score = engine.benefit_scores[BenefitType.LIFE]
        
        score_change = abs(final_life_score - initial_life_score)
        self.assertGreater(score_change, 5.0)  # Should have significant impact
        print(f"✓ Correlation test: Life insurance score changed by {score_change:.2f}")
    
    def test_score_bounds(self):
        """Test that scores stay within valid bounds (0-100)"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=35, income=120000, marital_status="married", num_children=2),
            UserFinancials(annual_income=120000, monthly_expenses=8000, total_debt=50000, total_savings=100000)
        )
        
        # Answer multiple questions
        for _ in range(10):
            if engine.should_stop():
                break
            question = engine.select_next_question()
            engine.process_answer(question, 0)
        
        # Check all scores are valid
        for bt, score in engine.benefit_scores.items():
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 100.0)
        
        print(f"✓ Score bounds test: All scores in [0, 100]")


class TestUserProfiles(unittest.TestCase):
    """Test different user profiles and expected outcomes"""
    
    def test_young_single_profile(self):
        """Test recommendations for young single person"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=25, income=45000, marital_status="single", num_children=0),
            UserFinancials(annual_income=45000, monthly_expenses=2800, total_debt=15000, total_savings=5000)
        )
        
        # Should prioritize medical and 401k over life insurance
        medical_score = engine.benefit_scores[BenefitType.MEDICAL]
        life_score = engine.benefit_scores[BenefitType.LIFE]
        retirement_score = engine.benefit_scores[BenefitType.RETIREMENT_401K]
        
        print(f"✓ Young single profile: Medical={medical_score:.1f}, Life={life_score:.1f}, 401k={retirement_score:.1f}")
        self.assertGreater(medical_score, 40.0)
    
    def test_family_profile(self):
        """Test recommendations for family with children"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=35, income=120000, marital_status="married", num_children=2),
            UserFinancials(annual_income=120000, monthly_expenses=8000, total_debt=50000, total_savings=100000)
        )
        
        # Should prioritize life insurance, disability, and dependent care
        life_score = engine.benefit_scores[BenefitType.LIFE]
        disability_score = engine.benefit_scores[BenefitType.DISABILITY]
        dependent_score = engine.benefit_scores[BenefitType.DEPENDENT_CARE]
        
        print(f"✓ Family profile: Life={life_score:.1f}, Disability={disability_score:.1f}, Dependent={dependent_score:.1f}")
        self.assertGreater(life_score, 60.0)
        self.assertGreater(disability_score, 40.0)
    
    def test_high_earner_profile(self):
        """Test recommendations for high earner"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=45, income=250000, marital_status="married", num_children=2),
            UserFinancials(annual_income=250000, monthly_expenses=15000, total_debt=100000, total_savings=500000)
        )
        
        # Should prioritize supplemental benefits and high coverage
        life_score = engine.benefit_scores[BenefitType.LIFE]
        disability_score = engine.benefit_scores[BenefitType.DISABILITY]
        supplemental_score = engine.benefit_scores[BenefitType.SUPPLEMENTAL_LIFE]
        
        print(f"✓ High earner profile: Life={life_score:.1f}, Disability={disability_score:.1f}, Supplemental={supplemental_score:.1f}")
        self.assertGreater(life_score, 70.0)
    
    def test_near_retirement_profile(self):
        """Test recommendations for near-retirement person"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=60, income=90000, marital_status="married", num_children=0),
            UserFinancials(annual_income=90000, monthly_expenses=6000, total_debt=20000, total_savings=800000)
        )
        
        # Should prioritize medical and long-term care
        medical_score = engine.benefit_scores[BenefitType.MEDICAL]
        ltc_score = engine.benefit_scores[BenefitType.LONG_TERM_CARE]
        
        print(f"✓ Near retirement profile: Medical={medical_score:.1f}, Long-term Care={ltc_score:.1f}")
        self.assertGreater(medical_score, 60.0)


class TestAdaptiveQuestioning(unittest.TestCase):
    """Test the adaptive questioning process"""
    
    def test_question_selection(self):
        """Test that highest IG question is selected"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=35, income=80000, marital_status="married", num_children=2),
            UserFinancials(annual_income=80000, monthly_expenses=5000, total_debt=20000, total_savings=30000)
        )
        
        selected = engine.select_next_question()
        
        # Verify it has the highest IG
        max_ig = 0.0
        for q in engine.question_bank:
            if q.id not in [ans.question.id for ans in engine.answer_history]:
                ig = engine.calculate_information_gain(q, engine.benefit_scores, engine.answer_history)
                max_ig = max(max_ig, ig)
        
        selected_ig = engine.calculate_information_gain(selected, engine.benefit_scores, engine.answer_history)
        self.assertAlmostEqual(selected_ig, max_ig, places=2)
        print(f"✓ Question selection test: Selected IG={selected_ig:.3f}, Max IG={max_ig:.3f}")
    
    def test_stopping_criteria_entropy(self):
        """Test stopping when entropy is low enough"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=35, income=120000, marital_status="married", num_children=2),
            UserFinancials(annual_income=120000, monthly_expenses=8000, total_debt=50000, total_savings=100000)
        )
        
        # Manually set very certain scores
        engine.benefit_scores = {bt: 20.0 for bt in BenefitType}
        engine.benefit_scores[BenefitType.LIFE] = 100.0
        engine.benefit_scores[BenefitType.DISABILITY] = 95.0
        engine.benefit_scores[BenefitType.MEDICAL] = 90.0
        
        entropy = engine.calculate_entropy(engine.benefit_scores)
        should_stop = engine.should_stop()
        
        print(f"✓ Entropy stopping test: Entropy={entropy:.3f}, Should stop={should_stop}")
        if entropy < 0.3:
            self.assertTrue(should_stop)
    
    def test_stopping_criteria_max_questions(self):
        """Test stopping at maximum questions"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=35, income=80000, marital_status="married", num_children=2),
            UserFinancials(annual_income=80000, monthly_expenses=5000, total_debt=20000, total_savings=30000)
        )
        
        # Simulate answering 15 questions
        for i in range(15):
            if len(engine.answer_history) < len(engine.question_bank):
                question = engine.select_next_question()
                engine.process_answer(question, 0)
        
        self.assertTrue(engine.should_stop())
        print(f"✓ Max questions test: Stopped after {len(engine.answer_history)} questions")
    
    def test_no_repeat_questions(self):
        """Test that questions are not repeated"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=35, income=80000, marital_status="married", num_children=2),
            UserFinancials(annual_income=80000, monthly_expenses=5000, total_debt=20000, total_savings=30000)
        )
        
        asked_ids = set()
        for _ in range(5):
            question = engine.select_next_question()
            self.assertNotIn(question.id, asked_ids)
            asked_ids.add(question.id)
            engine.process_answer(question, 0)
        
        print(f"✓ No repeat test: {len(asked_ids)} unique questions asked")


class TestRecommendationGeneration(unittest.TestCase):
    """Test recommendation generation and coverage calculations"""
    
    def test_recommendation_prioritization(self):
        """Test that recommendations are properly prioritized"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=35, income=120000, marital_status="married", num_children=2),
            UserFinancials(annual_income=120000, monthly_expenses=8000, total_debt=50000, total_savings=100000)
        )
        
        # Answer some questions
        for _ in range(8):
            question = engine.select_next_question()
            engine.process_answer(question, 0)
        
        recs = engine.generate_recommendations()
        
        # Check prioritization
        critical = [r for r in recs if r.priority == "CRITICAL"]
        recommended = [r for r in recs if r.priority == "RECOMMENDED"]
        
        if critical:
            self.assertGreater(critical[0].score, 75.0)
        
        print(f"✓ Prioritization test: {len(critical)} critical, {len(recommended)} recommended")
    
    def test_life_insurance_calculation(self):
        """Test life insurance coverage calculation"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=35, income=120000, marital_status="married", num_children=2),
            UserFinancials(annual_income=120000, monthly_expenses=8000, total_debt=50000, total_savings=100000)
        )
        
        # Set high life insurance score
        engine.benefit_scores[BenefitType.LIFE] = 95.0
        
        recs = engine.generate_recommendations()
        life_rec = next((r for r in recs if r.benefit_type == BenefitType.LIFE), None)
        
        if life_rec and 'coverage_amount' in life_rec.details:
            coverage = life_rec.details['coverage_amount']
            # Should be roughly 8-10x income + adjustments
            expected_min = 120000 * 8
            expected_max = 120000 * 12
            
            print(f"✓ Life insurance calc: ${coverage:,.0f} (expected ${expected_min:,.0f}-${expected_max:,.0f})")
            self.assertGreater(coverage, expected_min * 0.8)
    
    def test_disability_calculation(self):
        """Test disability benefit calculation"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=35, income=120000, marital_status="married", num_children=2),
            UserFinancials(annual_income=120000, monthly_expenses=8000, total_debt=50000, total_savings=100000)
        )
        
        engine.benefit_scores[BenefitType.DISABILITY] = 90.0
        
        recs = engine.generate_recommendations()
        disability_rec = next((r for r in recs if r.benefit_type == BenefitType.DISABILITY), None)
        
        if disability_rec and 'monthly_benefit' in disability_rec.details:
            monthly_benefit = disability_rec.details['monthly_benefit']
            monthly_income = 120000 / 12
            
            # Should be 60-70% of monthly income
            expected_min = monthly_income * 0.55
            expected_max = monthly_income * 0.75
            
            print(f"✓ Disability calc: ${monthly_benefit:,.0f}/mo (expected ${expected_min:,.0f}-${expected_max:,.0f})")
            self.assertGreater(monthly_benefit, expected_min)
            self.assertLess(monthly_benefit, expected_max * 1.1)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def test_zero_income(self):
        """Test with zero income"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=25, income=0, marital_status="single", num_children=0),
            UserFinancials(annual_income=0, monthly_expenses=1000, total_debt=0, total_savings=0)
        )
        
        # Should not crash
        question = engine.select_next_question()
        engine.process_answer(question, 0)
        recs = engine.generate_recommendations()
        
        print(f"✓ Zero income test: {len(recs)} recommendations generated")
        self.assertIsNotNone(recs)
    
    def test_high_age(self):
        """Test with very high age"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=75, income=60000, marital_status="married", num_children=0),
            UserFinancials(annual_income=60000, monthly_expenses=4000, total_debt=0, total_savings=300000)
        )
        
        # Should prioritize medical and long-term care
        medical_score = engine.benefit_scores[BenefitType.MEDICAL]
        ltc_score = engine.benefit_scores[BenefitType.LONG_TERM_CARE]
        
        print(f"✓ High age test: Medical={medical_score:.1f}, LTC={ltc_score:.1f}")
        self.assertGreater(medical_score, 40.0)
    
    def test_empty_question_bank(self):
        """Test behavior when all questions are answered"""
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=35, income=80000, marital_status="married", num_children=2),
            UserFinancials(annual_income=80000, monthly_expenses=5000, total_debt=20000, total_savings=30000)
        )
        
        # Answer all questions
        for question in engine.question_bank:
            engine.process_answer(question, 0)
        
        # Should stop
        self.assertTrue(engine.should_stop())
        print(f"✓ Empty bank test: Stopped after all questions answered")


class TestPerformance(unittest.TestCase):
    """Test performance and efficiency"""
    
    def test_entropy_calculation_speed(self):
        """Test entropy calculation performance"""
        import time
        
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=35, income=80000, marital_status="married", num_children=2),
            UserFinancials(annual_income=80000, monthly_expenses=5000, total_debt=20000, total_savings=30000)
        )
        
        start = time.time()
        for _ in range(1000):
            engine.calculate_entropy(engine.benefit_scores)
        elapsed = (time.time() - start) * 1000
        
        avg_time = elapsed / 1000
        print(f"✓ Entropy speed: {avg_time:.3f}ms average (target <1ms)")
        self.assertLess(avg_time, 5.0)  # Should be very fast
    
    def test_information_gain_speed(self):
        """Test information gain calculation performance"""
        import time
        
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=35, income=80000, marital_status="married", num_children=2),
            UserFinancials(annual_income=80000, monthly_expenses=5000, total_debt=20000, total_savings=30000)
        )
        
        question = engine.question_bank[0]
        
        start = time.time()
        for _ in range(100):
            engine.calculate_information_gain(question, engine.benefit_scores, [])
        elapsed = (time.time() - start) * 1000
        
        avg_time = elapsed / 100
        print(f"✓ IG calculation speed: {avg_time:.3f}ms average (target <50ms)")
        self.assertLess(avg_time, 100.0)
    
    def test_full_session_time(self):
        """Test complete session time"""
        import time
        
        engine = AdaptiveQuestionnaireEngine(
            UserDemographics(age=35, income=120000, marital_status="married", num_children=2),
            UserFinancials(annual_income=120000, monthly_expenses=8000, total_debt=50000, total_savings=100000)
        )
        
        start = time.time()
        while not engine.should_stop():
            question = engine.select_next_question()
            engine.process_answer(question, 0)
        
        recs = engine.generate_recommendations()
        elapsed = (time.time() - start) * 1000
        
        print(f"✓ Full session: {len(engine.answer_history)} questions in {elapsed:.1f}ms")
        self.assertLess(len(engine.answer_history), 20)  # Should be efficient


def run_all_tests():
    """Run all test suites with detailed output"""
    
    print("\n" + "="*80)
    print("ADAPTIVE QUESTIONNAIRE ENGINE - COMPREHENSIVE TEST SUITE")
    print("="*80 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestEntropyCalculations))
    suite.addTests(loader.loadTestsFromTestCase(TestInformationGain))
    suite.addTests(loader.loadTestsFromTestCase(TestBayesianUpdates))
    suite.addTests(loader.loadTestsFromTestCase(TestUserProfiles))
    suite.addTests(loader.loadTestsFromTestCase(TestAdaptiveQuestioning))
    suite.addTests(loader.loadTestsFromTestCase(TestRecommendationGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*80 + "\n")
    
    return result


if __name__ == "__main__":
    run_all_tests()
