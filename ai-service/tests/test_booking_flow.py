import pytest
from app.booking.booking_handler import booking_handler
from app.query.entity_extractor import entity_extractor

@pytest.mark.asyncio
async def test_full_single_turn_booking():
    query = "ascha ta hole khulne theke dhaka te agamikal SUV book koro. amk jeno sonadanga theke sokal 11 tay pick kore."
    entities = entity_extractor.extract(query)
    
    res = await booking_handler.process_turn(
        query=query,
        entities=entities,
        language="banglish",
        current_state_dict={}
    )
    
    assert res["booking_state"]["status"] == "confirming"
    assert "Toyota Land Cruiser Prado TX" in res["booking_state"]["car_name"] or res["booking_state"]["car_category"] == "SUV"
    assert res["booking_state"]["pickup_time"] == "11:00"
    assert "Confirm" in res["message"] or "confirm" in res["message"]

    # Next user turn: confirms
    confirm_query = "Haan confirm koro"
    confirm_entities = entity_extractor.extract(confirm_query)
    confirm_res = await booking_handler.process_turn(
        query=confirm_query,
        entities=confirm_entities,
        language="banglish",
        current_state_dict=res["booking_state"]
    )
    
    assert confirm_res["booking_state"]["status"] == "booked"
    assert confirm_res["booking_state"]["booking_code"] is not None
    assert "RC-BK-" in confirm_res["booking_state"]["booking_code"]

@pytest.mark.asyncio
async def test_multi_turn_step_by_step_booking():
    # Turn 1: User asks to book for 4th
    q1 = "amk 4 tarik akta car book koro"
    e1 = entity_extractor.extract(q1)
    r1 = await booking_handler.process_turn(query=q1, entities=e1, language="banglish", current_state_dict={})
    assert r1["booking_state"]["status"] == "collecting"
    assert "car" in r1["booking_action"]["missing"]
    
    # Turn 2: User specifies car: "Tucson ta nao"
    q2 = "Tucson ta nao"
    e2 = entity_extractor.extract(q2)
    r2 = await booking_handler.process_turn(query=q2, entities=e2, language="banglish", current_state_dict=r1["booking_state"])
    assert r2["booking_state"]["car_name"] == "Hyundai Tucson AWD"
    assert "pickup_location" in r2["booking_action"]["missing"]
    
    # Turn 3: User specifies location: "Gulshan theke"
    q3 = "Gulshan theke"
    e3 = entity_extractor.extract(q3)
    r3 = await booking_handler.process_turn(query=q3, entities=e3, language="banglish", current_state_dict=r2["booking_state"])
    assert r3["booking_state"]["pickup_location"] == "Gulshan"
    assert "pickup_time" in r3["booking_action"]["missing"]

    # Turn 4: User specifies time: "8 tay"
    q4 = "8 tay"
    e4 = entity_extractor.extract(q4)
    r4 = await booking_handler.process_turn(query=q4, entities=e4, language="banglish", current_state_dict=r3["booking_state"])
    assert r4["booking_state"]["status"] == "confirming"
    assert r4["booking_state"]["pickup_time"] == "08:00"

    # Turn 5: User confirms: "haan confirm koro"
    q5 = "haan confirm koro"
    e5 = entity_extractor.extract(q5)
    r5 = await booking_handler.process_turn(query=q5, entities=e5, language="banglish", current_state_dict=r4["booking_state"])
    assert r5["booking_state"]["status"] == "booked"
    assert "RC-BK-" in r5["booking_state"]["booking_code"]
