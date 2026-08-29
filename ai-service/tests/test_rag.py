import pytest
from app.services.vector_store import vector_store
from app.services.rag_engine import RAGEngine

@pytest.mark.asyncio
async def test_vector_store_initialization():
    await vector_store.initialize()
    assert vector_store.is_initialized is True
    assert len(vector_store.documents) > 0
    assert vector_store.embeddings_matrix is not None

@pytest.mark.asyncio
async def test_vector_similarity_search():
    await vector_store.initialize()
    results = await vector_store.search("mountain off road 4x4 suv for hilly area", top_k=3)
    assert len(results) > 0
    # Top result should be related to Prado or SUV / mountain guide
    top_doc = results[0]
    assert any(k in top_doc["title"].lower() or k in top_doc["content"].lower() for k in ["prado", "suv", "mountain", "4x4"])

@pytest.mark.asyncio
async def test_rag_query_pipeline():
    res = await RAGEngine.query("What is the security deposit and refund policy?")
    assert "answer" in res
    assert len(res["sources"]) > 0
    assert "deposit" in res["answer"].lower() or "refund" in res["answer"].lower()

@pytest.mark.asyncio
async def test_ai_car_recommendation():
    res = await RAGEngine.recommend_vehicle(
        trip_description="Family trip of 6 people with luggage going to Sajek Valley",
        passengers=6,
        terrain="Hills / Off-road"
    )
    assert "primary_recommendation" in res
    assert res["primary_recommendation"]["match_score"] > 50
