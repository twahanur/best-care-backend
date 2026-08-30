import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_chat_availability_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "query": "Khulna te available car dekhao",
            "session_id": "test_sess_1",
            "user_id": "usr_cust_1"
        }
        response = await ac.post("/rag/chat", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["intent"] == "car_availability"
        assert data["query_type"] == "structured"
        assert len(data["message"]) > 0

@pytest.mark.asyncio
async def test_chat_booking_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "query": "amk 4 tarik akta car book koro",
            "session_id": "test_sess_booking_1",
            "user_id": "usr_cust_1"
        }
        response = await ac.post("/rag/chat", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["intent"] == "booking_create"
        assert data["query_type"] == "booking_action"
        assert data["booking_action"]["status"] == "collecting"
