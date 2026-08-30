import pytest
from datetime import datetime, timezone
from app.query.entity_extractor import entity_extractor

def test_extract_locations_and_time():
    query = "ascha ta hole khulne theke dhaka te agamikal SUV book koro. amk jeno sonadanga theke sokal 11 tay pick kore."
    entities = entity_extractor.extract(query)
    
    assert entities["category"] == "SUV"
    assert "Sonadanga, Khulna" in entities["pickup_location"] or "Khulna" in entities["pickup_location"]
    assert entities["dropoff_location"] == "Dhaka"
    assert entities["pickup_time"] == "11:00"
    assert entities["pickup_date"] is not None

def test_extract_tarik_date():
    ref_time = datetime(2026, 8, 30, 10, 0, tzinfo=timezone.utc)
    query = "amk 4 tarik akta car book koro"
    entities = entity_extractor.extract(query, current_time=ref_time)
    
    assert entities["pickup_date"] == "2026-09-04"

def test_extract_specific_car_model():
    query = "Tucson ta nao"
    entities = entity_extractor.extract(query)
    assert entities["vehicle_name"] == "Hyundai Tucson AWD"
    assert entities["category"] == "SUV"

def test_extract_confirmation():
    assert entity_extractor.extract("haan confirm koro")["is_confirmation"] is True
    assert entity_extractor.extract("yes please proceed")["is_confirmation"] is True
    assert entity_extractor.extract("na cancel koro")["is_cancellation"] is True
