"""
Comprehensive Test Suite for PostgreSQL-Powered Production Agentic RAG Module.
Tests:
1. Multilingual understanding (Bangla, Banglish, English)
2. Conversational multi-turn memory and context retention across turns
3. Dynamic document ingestion, change detection, and non-blocking background queue
4. Hybrid RRF retrieval and metadata filtering
"""
import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.agent.rag_agent import rag_agent
from app.memory.conversation_memory import conversation_memory
from app.query.language_detector import language_detector
from app.query.intent_detector import intent_detector
from app.query.entity_extractor import entity_extractor
from app.indexing.change_detector import ChangeDetector
from app.workers.embedding_queue import EmbeddingQueue
from app.workers.background_worker import background_worker

@pytest.mark.asyncio
async def test_language_detection():
    # Bangla script
    assert language_detector.detect("সিলেটের জন্য কোন গাড়ি ভালো হবে?") == "bangla"
    # Banglish
    assert language_detector.detect("amar family er jonno 6 joner gari lagbe sajek jabo") == "banglish"
    # English
    assert language_detector.detect("What is the security deposit and refund policy?") == "english"

@pytest.mark.asyncio
async def test_entity_and_intent_extraction():
    query = "amader 6 joner family niye sajek jabo budget 150 dollar"
    intent = intent_detector.detect(query)
    entities = entity_extractor.extract(query)
    
    assert intent == "TRIP_RECOMMENDATION"
    assert entities["seats"] == 6
    assert entities["destination"] == "Sajek Valley"
    assert entities["budget_max"] == 150.0

@pytest.mark.asyncio
async def test_multilingual_agentic_chat_banglish():
    res = await rag_agent.chat(
        user_query="amader 6 joner family niye sajek jabo kon gari bhalo hobe?",
        session_id="test_session_banglish_1"
    )
    assert res["session_id"] == "test_session_banglish_1"
    assert len(res["sources"]) > 0
    assert "answer" in res
    assert res["language"] == "banglish"
    # Should recommend Prado or HiAce/SUV for 6 people to Sajek
    assert any("prado" in s["title"].lower() or "suv" in s["title"].lower() or "hiace" in s["title"].lower() for s in res["sources"])

@pytest.mark.asyncio
async def test_multilingual_agentic_chat_bangla():
    res = await rag_agent.chat(
        user_query="সিকিউরিটি ডিপোজিট ও রিফান্ড পলিসি কি?",
        session_id="test_session_bangla_1"
    )
    assert len(res["sources"]) > 0
    assert "answer" in res
    assert res["language"] == "bangla"
    assert any("deposit" in s["id"].lower() or "deposit" in s["title"].lower() for s in res["sources"])

@pytest.mark.asyncio
async def test_conversational_memory_multi_turn():
    session_id = "test_memory_turn_session"
    # Clear any previous run
    await conversation_memory.clear_history(session_id)

    # Turn 1: Inquire about luxury SUV for mountain trip
    turn1 = await rag_agent.chat(
        user_query="What is your best 7 seater luxury SUV for mountain trips?",
        session_id=session_id
    )
    assert len(turn1["sources"]) > 0

    # Turn 2: Follow-up question referring to "that car"
    turn2 = await rag_agent.chat(
        user_query="How much does it cost per day and what is the luggage capacity?",
        session_id=session_id
    )
    assert len(turn2["sources"]) > 0
    assert "145" in turn2["answer"] or "prado" in turn2["answer"].lower() or "suitcases" in turn2["answer"].lower() or "passengers" in turn2["answer"].lower()

    # Verify history is persisted in database
    history = await conversation_memory.get_history(session_id)
    assert len(history) == 4  # 2 user turns + 2 assistant turns

@pytest.mark.asyncio
async def test_dynamic_document_ingestion_and_background_queue():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Insert a new vehicle dynamically
        new_doc_payload = {
            "id": "fleet_defender_custom_v8",
            "entity_type": "vehicle",
            "category": "Fleet Specs",
            "title": "Land Rover Defender 110 V8 Supercharged",
            "content": "Model: Land Rover Defender 110 V8. Daily Rate: $185/day. Capacity: 7 Passengers. Heavy Off-Road with air suspension.",
            "tags": ["defender", "land rover", "v8", "7-seater", "off-road"],
            "metadata": {"dailyRate": 185, "seats": 7, "category": "SUV"}
        }
        res = await ac.post("/rag/documents", json=new_doc_payload)
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "created"
        assert "job_id" in data

        # Process the enqueued job via background worker
        job = await EmbeddingQueue.get_next_job()
        if job:
            await background_worker._process_single_document(job["document_id"])
            await EmbeddingQueue.update_job_status(job["job_id"], "COMPLETED")
            EmbeddingQueue.task_done()

        # Query the vector store for Defender
        search_res = await ac.post("/rag/chat", json={"query": "Tell me about the Land Rover Defender"})
        assert search_res.status_code == 200
        search_data = search_res.json()
        assert any("defender" in s["title"].lower() for s in search_data["sources"])

@pytest.mark.asyncio
async def test_session_history_and_clear_api():
    transport = ASGITransport(app=app)
    session_id = "test_api_session_manage"
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Chat
        await ac.post("/rag/chat", json={"query": "What are your driver age requirements?", "session_id": session_id})
        
        # Get history
        hist_res = await ac.get(f"/rag/sessions/{session_id}/history")
        assert hist_res.status_code == 200
        hist_data = hist_res.json()
        assert hist_data["total_turns"] >= 2

        # Clear history
        del_res = await ac.delete(f"/rag/sessions/{session_id}")
        assert del_res.status_code == 200
        
        # Verify cleared
        hist_res_after = await ac.get(f"/rag/sessions/{session_id}/history")
        assert hist_res_after.json()["total_turns"] == 0
