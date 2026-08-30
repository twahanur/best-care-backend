import pytest
from app.query.intent_classifier import intent_classifier
from app.query.query_planner import query_planner

def test_intent_classification():
    assert intent_classifier.classify("Khulna te available car dekhao") == "car_availability"
    assert intent_classifier.classify("amk 4 tarik ekta car book koro") == "booking_create"
    assert intent_classifier.classify("amar booking status dekhao") == "booking_lookup"
    assert intent_classifier.classify("amar payment er status ki?") == "payment_status"
    assert intent_classifier.classify("security deposit koto?") == "policy_inquiry"
    assert intent_classifier.classify("sajek jabo kon gari bhalo?") == "trip_recommendation"
    assert intent_classifier.classify("total revenue koto?", user_role="ADMIN") == "admin_revenue"

def test_query_planner_routing():
    plan_avail = query_planner.plan("Khulna te available car dekhao")
    assert plan_avail.query_type == "structured"
    assert plan_avail.requires_sql is True

    plan_booking = query_planner.plan("amk 4 tarik ekta car book koro")
    assert plan_booking.query_type == "booking_action"
    assert plan_booking.requires_booking_action is True

    plan_policy = query_planner.plan("deposit refund policy ki?")
    assert plan_policy.query_type == "semantic"
    assert plan_policy.requires_vector is True

    plan_hybrid = query_planner.plan("sajek jabo kon gari bhalo?")
    assert plan_hybrid.query_type == "hybrid"
    assert plan_hybrid.requires_sql is True
    assert plan_hybrid.requires_vector is True
