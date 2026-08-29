import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["service"] == "ai-rag-microservice"

@pytest.mark.asyncio
async def test_rag_query_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/rag/query", json={"query": "What is the insurance policy?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["sources"]) > 0

@pytest.mark.asyncio
async def test_lead_qualification_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/lead/score-and-qualify",
            json={
                "customer_name": "Test Client",
                "customer_email": "test@client.com",
                "vehicle_category": "SUV",
                "duration_days": 5,
                "estimated_budget": 500.0,
                "is_corporate": False
            }
        )
    assert response.status_code == 200
    data = response.json()
    assert "lead_score" in data
    assert "classification" in data
