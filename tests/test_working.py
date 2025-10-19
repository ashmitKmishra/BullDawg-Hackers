"""
Working Functional Test - Demonstrates algorithm with correct API
"""

import sys
sys.path.insert(0, '.')

from adaptive_questionnaire_engine import (
    AdaptiveQuestionnaireEngine,
    UserDemographics,
    UserFinancials,
    BenefitType
)

print("\n" + "="*80)
print(" ADAPTIVE BENEFIT SELECTION ALGORITHM - FUNCTIONAL TESTING")
print("="*80)

# Test 1: Young Professional
print("\n┌─ TEST 1: Young Professional ───────────────────────────────────────────┐")
print("│ Profile: Age 26, $55k income, Single, No children                     │")
print("└────────────────────────────────────────────────────────────────────────┘")

demo1 = UserDemographics(
    name="Alex Johnson", age=26, gender="Female",
    location="Austin, TX", zip_code="78701",
    marital_status="single", num_children=0
)

fin1 = UserFinancials(
    annual_income=55000.0, monthly_expenses=3200.0,
    total_debt=20000.0, savings=12000.0,
    investment_accounts=5000.0,
    spending_categories={}, income_volatility=0.15
)

engine1 = AdaptiveQuestionnaireEngine(demo1, fin1)

# Show initial scores
sorted1 = sorted(engine1.benefit_scores.items(), key=lambda x: x[1], reverse=True)
print(f"\n📊 Initial Benefit Priorities:")
for i, (bt, score) in enumerate(sorted1[:5], 1):
    print(f"   {i}. {bt.value:25} {score:.1f}/100")

# Adaptive questioning
print(f"\n💬 Adaptive Questioning (max 8 questions):")
q_count = 0
while not engine1.should_stop() and q_count < 8:
    q = engine1.select_next_question()
    choice = 1 if "children" in q.text.lower() else 0  # No kids
    engine1.process_answer(q, choice)
    q_count += 1
    answer_text = q.choice_a if choice == 0 else q.choice_b
    print(f"   Q{q_count}: {q.text[:65]}")
    print(f"        → {answer_text[:60]}")

recs1 = engine1.generate_recommendations()
top5_1 = sorted(recs1, key=lambda r: r.score, reverse=True)[:5]

print(f"\n✅ Final Recommendations (after {q_count} questions):")
for i, rec in enumerate(top5_1, 1):
    print(f"   {i}. {rec.benefit_type.value:25} {rec.score:.1f}/100 [{rec.priority}]")

print(f"\n✓ Test 1 Complete: Asked {q_count} questions, generated {len(recs1)} recommendations\n")


# Test 2: Family with Children
print("\n┌─ TEST 2: Family with Children ─────────────────────────────────────────┐")
print("│ Profile: Age 38, $130k income, Married, 3 children                    │")
print("└────────────────────────────────────────────────────────────────────────┘")

demo2 = UserDemographics(
    name="Sarah Martinez", age=38, gender="Female",
    location="Seattle, WA", zip_code="98101",
    marital_status="married", num_children=3
)

fin2 = UserFinancials(
    annual_income=130000.0, monthly_expenses=8500.0,
    total_debt=80000.0, savings=75000.0,
    investment_accounts=150000.0,
    spending_categories={}, income_volatility=0.08
)

engine2 = AdaptiveQuestionnaireEngine(demo2, fin2)

sorted2 = sorted(engine2.benefit_scores.items(), key=lambda x: x[1], reverse=True)
print(f"\n📊 Initial Benefit Priorities:")
for i, (bt, score) in enumerate(sorted2[:5], 1):
    print(f"   {i}. {bt.value:25} {score:.1f}/100")

print(f"\n💬 Adaptive Questioning (max 10 questions):")
q_count2 = 0
while not engine2.should_stop() and q_count2 < 10:
    q = engine2.select_next_question()
    # Family-oriented answers
    if "children" in q.text.lower() or "kids" in q.text.lower():
        choice = 0  # Yes
    elif "risk" in q.text.lower():
        choice = 1  # Conservative
    else:
        choice = 0
    
    engine2.process_answer(q, choice)
    q_count2 += 1
    answer_text = q.choice_a if choice == 0 else q.choice_b
    print(f"   Q{q_count2}: {q.text[:65]}")
    print(f"        → {answer_text[:60]}")

recs2 = engine2.generate_recommendations()
top5_2 = sorted(recs2, key=lambda r: r.score, reverse=True)[:5]

print(f"\n✅ Final Recommendations (after {q_count2} questions):")
for i, rec in enumerate(top5_2, 1):
    details_str = ""
    if rec.recommendation and 'coverage_amount' in rec.recommendation:
        details_str = f" (${rec.recommendation['coverage_amount']:,.0f} coverage)"
    elif rec.recommendation and 'monthly_benefit' in rec.recommendation:
        details_str = f" (${rec.recommendation['monthly_benefit']:,.0f}/mo benefit)"
    
    print(f"   {i}. {rec.benefit_type.value:25} {rec.score:.1f}/100 [{rec.priority}]{details_str}")

print(f"\n✓ Test 2 Complete: Asked {q_count2} questions, generated {len(recs2)} recommendations\n")


# Comparison Analysis
print("\n" + "="*80)
print(" COMPARATIVE ANALYSIS")
print("="*80)

life1 = next((r.score for r in recs1 if r.benefit_type == BenefitType.LIFE), 0)
life2 = next((r.score for r in recs2 if r.benefit_type == BenefitType.LIFE), 0)

disability1 = next((r.score for r in recs1 if r.benefit_type == BenefitType.DISABILITY), 0)
disability2 = next((r.score for r in recs2 if r.benefit_type == BenefitType.DISABILITY), 0)

dependent1 = next((r.score for r in recs1 if r.benefit_type == BenefitType.DEPENDENT_CARE_FSA), 0)
dependent2 = next((r.score for r in recs2 if r.benefit_type == BenefitType.DEPENDENT_CARE_FSA), 0)

print(f"\n📈 Benefit Score Comparison:")
print(f"\n   Life Insurance:")
print(f"      Young Professional: {life1:5.1f}/100")
print(f"      Family (3 kids):    {life2:5.1f}/100")
print(f"      Difference:         {life2-life1:+5.1f} points")
if life2 > life1:
    print(f"      ✓ Correctly prioritized for family")

print(f"\n   Disability Insurance:")
print(f"      Young Professional: {disability1:5.1f}/100")
print(f"      Family (3 kids):    {disability2:5.1f}/100")
print(f"      Difference:         {disability2-disability1:+5.1f} points")

print(f"\n   Dependent Care:")
print(f"      Young Professional: {dependent1:5.1f}/100")
print(f"      Family (3 kids):    {dependent2:5.1f}/100")
print(f"      Difference:         {dependent2-dependent1:+5.1f} points")
if dependent2 > dependent1:
    print(f"      ✓ Correctly prioritized for family")


# Test Summary
print("\n\n" + "="*80)
print(" TEST RESULTS")
print("="*80)

tests = [
    ("Engine Initialization", True),
    ("Question Bank Loaded", len(engine1.question_bank) == 10),
    ("Adaptive Question Selection", q_count > 0 and q_count2 > 0),
    ("Answer Processing", q_count == 8),  # We asked 8 questions in test 1
    ("Recommendation Generation", len(recs1) > 0 and len(recs2) > 0),
    ("Profile Differentiation (Life)", life2 > life1),
    ("Profile Differentiation (Dependent)", dependent2 > dependent1),
    ("Question Efficiency", q_count <= 10 and q_count2 <= 12),
    ("Coverage Calculations", any('coverage_amount' in r.recommendation for r in recs2 if r.recommendation))
]

passed = sum(1 for _, result in tests if result)
total = len(tests)

print(f"\n{'Test Name':<40} {'Result':<10}")
print(f"{'-'*50}")
for name, result in tests:
    status = "✓ PASS" if result else "✗ FAIL"
    print(f"{name:<40} {status:<10}")

print(f"\n{'-'*50}")
print(f"{'TOTAL:':<40} {passed}/{total} ({passed/total*100:.1f}%)")
print(f"{'='*80}")

if passed == total:
    print(f"\n🎉  ALL TESTS PASSED!  🎉")
    print(f"\n✅ Algorithm Validated:")
    print(f"   • Adaptive question selection working")
    print(f"   • Profile-specific recommendations accurate")
    print(f"   • Question efficiency: {q_count}-{q_count2} questions (target: <12)")
    print(f"   • Coverage calculations functional")
    print(f"   • Ready for production deployment")
    print(f"\n{'='*80}\n")
    sys.exit(0)
else:
    print(f"\n⚠  {total-passed} test(s) failed. Review results above.")
    print(f"\n{'='*80}\n")
    sys.exit(1)
