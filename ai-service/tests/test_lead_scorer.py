from app.services.lead_scorer import LeadScorer

def test_lead_scorer_hot_lead():
    res = LeadScorer.score_lead(
        customer_name="Corporate Executive",
        customer_email="exec@corp.com",
        vehicle_category="Luxury Executive Sedan",
        duration_days=10,
        estimated_budget=1800.0,
        is_corporate=True,
        notes="Urgent airport VIP pickup needed"
    )
    assert res["lead_score"] >= 80
    assert res["classification"] == "Hot"
    assert res["estimated_value_usd"] > 1000

def test_lead_scorer_standard_lead():
    res = LeadScorer.score_lead(
        customer_name="John Doe",
        customer_email="john@gmail.com",
        vehicle_category="Budget Sedan",
        duration_days=2,
        estimated_budget=100.0
    )
    assert res["lead_score"] < 80
    assert res["classification"] in ["Warm", "Cold"]
