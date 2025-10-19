"""
Quick Validation Test Suite - Tests core functionality with correct data structures
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adaptive_questionnaire_engine import (
    AdaptiveQuestionnaireEngine,
    UserDemographics,
    UserFinancials,
    BenefitType
)

def create_demo_user(name="Test User", age=35, income=100000):
    """Helper to create demo user with correct structure"""
    demographics = UserDemographics(
        name=name,
        age=age,
        gender="Male",
        location="New York, NY",
        zip_code="10001",
        marital_status="married",
        num_children=2
    )
    
    financials = UserFinancials(
        annual_income=float(income),
        monthly_expenses=float(income * 0.6 / 12),
        total_debt=float(income * 0.4),
        savings=float(income * 0.8),
        investment_accounts=float(income * 0.5),
        spending_categories={"housing": 2000.0, "food": 800.0, "transport": 500.0},
        income_volatility=0.1
    )
    
    return demographics, financials


def test_basic_initialization():
    """Test: Can we initialize the engine?"""
    print("\n🧪 Test 1: Basic Initialization")
    demographics, financials = create_demo_user()
    engine = AdaptiveQuestionnaireEngine(demographics, financials)
    print(f"   ✓ Engine initialized successfully")
    print(f"   ✓ Question bank has {len(engine.question_bank)} questions")
    print(f"   ✓ Tracking {len(engine.benefit_scores)} benefit types")
    return True


def test_entropy_calculation():
    """Test: Can we calculate entropy?"""
    print("\n🧪 Test 2: Entropy Calculation")
    demographics, financials = create_demo_user()
    engine = AdaptiveQuestionnaireEngine(demographics, financials)
    
    entropy = engine.calculate_entropy(engine.benefit_scores)
    print(f"   ✓ Initial entropy: {entropy:.2f} bits")
    
    if entropy > 0 and entropy < 20:
        print(f"   ✓ Entropy is in valid range")
        return True
    else:
        print(f"   ✗ Entropy {entropy} is out of expected range")
        return False


def test_question_selection():
    """Test: Can we select questions?"""
    print("\n🧪 Test 3: Question Selection")
    demographics, financials = create_demo_user()
    engine = AdaptiveQuestionnaireEngine(demographics, financials)
    
    question = engine.select_next_question()
    print(f"   ✓ Selected question: {question.text[:60]}...")
    print(f"   ✓ Question has {len(question.choices)} choices")
    
    ig = engine.calculate_information_gain(question, engine.benefit_scores, [])
    print(f"   ✓ Information gain: {ig:.3f} bits")
    
    return ig > 0


def test_answer_processing():
    """Test: Can we process answers?"""
    print("\n🧪 Test 4: Answer Processing")
    demographics, financials = create_demo_user()
    engine = AdaptiveQuestionnaireEngine(demographics, financials)
    
    initial_entropy = engine.calculate_entropy(engine.benefit_scores)
    
    question = engine.select_next_question()
    engine.process_answer(question, 0)
    
    final_entropy = engine.calculate_entropy(engine.benefit_scores)
    
    print(f"   ✓ Entropy: {initial_entropy:.2f} → {final_entropy:.2f} bits")
    print(f"   ✓ Answer recorded in history: {len(engine.answer_history)} answers")
    
    return len(engine.answer_history) == 1


def test_recommendation_generation():
    """Test: Can we generate recommendations?"""
    print("\n🧪 Test 5: Recommendation Generation")
    demographics, financials = create_demo_user()
    engine = AdaptiveQuestionnaireEngine(demographics, financials)
    
    # Answer a few questions
    for i in range(5):
        question = engine.select_next_question()
        engine.process_answer(question, i % 2)
    
    recs = engine.generate_recommendations()
    
    print(f"   ✓ Generated {len(recs)} recommendations")
    
    critical = [r for r in recs if r.priority == "CRITICAL"]
    recommended = [r for r in recs if r.priority == "RECOMMENDED"]
    
    print(f"   ✓ Critical: {len(critical)}, Recommended: {len(recommended)}")
    
    if recs:
        top_rec = recs[0]
        print(f"   ✓ Top recommendation: {top_rec.benefit_type.value} (Score: {top_rec.score:.1f})")
    
    return len(recs) > 0


def test_full_session():
    """Test: Complete adaptive questioning session"""
    print("\n🧪 Test 6: Full Adaptive Session")
    demographics, financials = create_demo_user(name="John Smith", age=38, income=125000)
    engine = AdaptiveQuestionnaireEngine(demographics, financials)
    
    initial_entropy = engine.calculate_entropy(engine.benefit_scores)
    print(f"   Initial entropy: {initial_entropy:.2f} bits")
    
    questions_asked = 0
    while not engine.should_stop() and questions_asked < 12:
        question = engine.select_next_question()
        # Simulate intelligent answers
        choice = 0 if "children" in question.text.lower() else 1
        engine.process_answer(question, choice)
        questions_asked += 1
    
    final_entropy = engine.calculate_entropy(engine.benefit_scores)
    recs = engine.generate_recommendations()
    
    print(f"   ✓ Asked {questions_asked} questions")
    print(f"   ✓ Final entropy: {final_entropy:.2f} bits")
    print(f"   ✓ Entropy reduced by {initial_entropy - final_entropy:.2f} bits")
    print(f"   ✓ Generated {len(recs)} recommendations")
    
    # Show top 3
    print(f"   Top 3 recommendations:")
    for i, rec in enumerate(recs[:3], 1):
        print(f"      {i}. {rec.benefit_type.value}: {rec.score:.1f}/100")
    
    return questions_asked > 0 and len(recs) > 0


def test_different_profiles():
    """Test: Different user profiles get different recommendations"""
    print("\n🧪 Test 7: Different User Profiles")
    
    # Young single
    demo1, fin1 = create_demo_user(name="Young Professional", age=25, income=50000)
    demo1.marital_status = "single"
    demo1.num_children = 0
    engine1 = AdaptiveQuestionnaireEngine(demo1, fin1)
    
    # Family with kids
    demo2, fin2 = create_demo_user(name="Family Person", age=38, income=120000)
    demo2.marital_status = "married"
    demo2.num_children = 3
    engine2 = AdaptiveQuestionnaireEngine(demo2, fin2)
    
    life1 = engine1.benefit_scores[BenefitType.LIFE]
    life2 = engine2.benefit_scores[BenefitType.LIFE]
    
    print(f"   Young single - Life insurance score: {life1:.1f}")
    print(f"   Family (3 kids) - Life insurance score: {life2:.1f}")
    
    if life2 > life1:
        print(f"   ✓ Family correctly has higher life insurance priority")
        return True
    else:
        print(f"   ⚠ Expected family to have higher life insurance score")
        return False


def test_performance():
    """Test: Check performance metrics"""
    print("\n🧪 Test 8: Performance")
    import time
    
    demographics, financials = create_demo_user()
    
    # Test initialization speed
    start = time.time()
    engine = AdaptiveQuestionnaireEngine(demographics, financials)
    init_time = (time.time() - start) * 1000
    print(f"   Initialization: {init_time:.2f}ms")
    
    # Test entropy calculation speed
    start = time.time()
    for _ in range(100):
        engine.calculate_entropy(engine.benefit_scores)
    entropy_time = (time.time() - start) * 10  # per call in ms
    print(f"   Entropy calculation: {entropy_time:.3f}ms average")
    
    # Test question selection speed
    start = time.time()
    question = engine.select_next_question()
    selection_time = (time.time() - start) * 1000
    print(f"   Question selection: {selection_time:.2f}ms")
    
    # Test full session speed
    start = time.time()
    for i in range(10):
        if not engine.should_stop():
            q = engine.select_next_question()
            engine.process_answer(q, i % 2)
    session_time = (time.time() - start) * 1000
    print(f"   Full 10-question session: {session_time:.1f}ms")
    
    # Check if we meet targets
    meets_targets = (entropy_time < 5.0 and selection_time < 200 and session_time < 3000)
    if meets_targets:
        print(f"   ✓ All performance targets met")
    
    return meets_targets


def run_validation_tests():
    """Run all validation tests"""
    print("\n" + "="*80)
    print("ADAPTIVE QUESTIONNAIRE ENGINE - QUICK VALIDATION")
    print("="*80)
    
    tests = [
        test_basic_initialization,
        test_entropy_calculation,
        test_question_selection,
        test_answer_processing,
        test_recommendation_generation,
        test_full_session,
        test_different_profiles,
        test_performance
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append((test.__doc__.split(":")[1].strip(), result))
        except Exception as e:
            print(f"   ✗ ERROR: {e}")
            results.append((test.__doc__.split(":")[1].strip(), False))
    
    # Summary
    print("\n" + "="*80)
    print("VALIDATION SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:10} - {test_name}")
    
    print("="*80)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("="*80 + "\n")
    
    if passed == total:
        print("🎉 ALL VALIDATION TESTS PASSED! Algorithm is working correctly.\n")
    elif passed >= total * 0.8:
        print("⚠ Most tests passed. Review failures above.\n")
    else:
        print("❌ Multiple failures. Algorithm needs attention.\n")
    
    return passed == total


if __name__ == "__main__":
    success = run_validation_tests()
    sys.exit(0 if success else 1)
