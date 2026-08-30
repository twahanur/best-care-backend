import pytest
from app.retrieval.sql_executor import sql_executor

@pytest.mark.asyncio
async def test_sql_executor_car_availability():
    res = await sql_executor.execute_template("car_availability", {"city": "Khulna"})
    assert len(res) > 0
    assert any("Khulna" in str(r.get("hub_city", "")) or "Khulna" in str(r.get("name", "")) for r in res)

@pytest.mark.asyncio
async def test_sql_executor_user_bookings():
    res = await sql_executor.execute_template("user_bookings", {}, user_id="usr_cust_1")
    assert len(res) > 0
    assert all(r["userId"] == "usr_cust_1" for r in res)

@pytest.mark.asyncio
async def test_sql_executor_blocks_mutation():
    with pytest.raises(ValueError):
        sql_executor._validate_safe_query("DROP TABLE cars;")
    with pytest.raises(ValueError):
        sql_executor._validate_safe_query("DELETE FROM bookings WHERE 1=1;")
