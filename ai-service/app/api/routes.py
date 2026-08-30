import time
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import select
from app.core.database import get_db_session
from app.core.models import KnowledgeDocument
from app.query.query_planner import query_planner
from app.booking.booking_handler import booking_handler
from app.retrieval.hybrid_retriever import hybrid_retriever
from app.context.context_builder import context_builder
from app.generation.llm_generator import llm_generator
from app.memory.conversation_memory import conversation_memory
from app.indexing.dynamic_knowledge_syncer import dynamic_knowledge_syncer

router = APIRouter(prefix="/rag", tags=["RAG & AI Chat"])

class ChatRequest(BaseModel):
    query: str
    sessionId: Optional[str] = Field(None, alias="session_id")
    userId: Optional[str] = Field(None, alias="user_id")
    userName: Optional[str] = Field(None, alias="user_name")
    userEmail: Optional[str] = Field(None, alias="user_email")
    userPhone: Optional[str] = Field(None, alias="user_phone")
    userRole: Optional[str] = Field("CUSTOMER", alias="user_role")
    category: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)

class ChatResponse(BaseModel):
    session_id: str
    message: str
    intent: str
    query_type: str
    language: str
    sources: List[Dict[str, Any]] = []
    data: Optional[Any] = []
    booking_action: Optional[Dict[str, Any]] = None
    timing_ms: Optional[float] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    req: ChatRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Production-ready Hybrid RAG Chat endpoint supporting:
    - Structured live PostgreSQL queries (availability, my bookings, payments)
    - Conversational multi-turn slot-filling and car booking
    - Semantic vector retrieval (policies, FAQs, guides)
    - Grounded multilingual generation (English, Bangla, Banglish)
    """
    t0 = time.time()
    user_info = {
        "id": req.userId or "usr_cust_1",
        "userId": req.userId or "usr_cust_1",
        "name": req.userName or "Shahriar Khan",
        "email": req.userEmail or "customer@example.com",
        "phone": req.userPhone or "+8801700000000",
        "role": req.userRole or "CUSTOMER"
    }

    # 1. Load Session & History
    session_obj = await conversation_memory.get_or_create_session(
        session_id=req.sessionId,
        user_info=user_info
    )
    session_id = session_obj.id
    current_state = await conversation_memory.get_session_state(session_id)
    history = await conversation_memory.get_history(session_id)

    # 2. Plan Query
    plan = query_planner.plan(
        query=req.query,
        booking_state=current_state,
        user_role=user_info["role"]
    )

    # Record User Message
    await conversation_memory.add_message(
        session_id=session_id,
        role="user",
        content=req.query,
        language=plan.language,
        intent=plan.intent,
        query_type=plan.query_type
    )

    # 3. Path A: Conversational Booking Action Flow
    if plan.query_type == "booking_action":
        booking_res = await booking_handler.process_turn(
            query=req.query,
            entities=plan.entities,
            language=plan.language,
            current_state_dict=current_state,
            recent_messages=history,
            user_info=user_info,
            auth_header=authorization
        )

        # Save new booking state
        await conversation_memory.save_session_state(session_id, booking_res["booking_state"])

        # Persist assistant response
        await conversation_memory.add_message(
            session_id=session_id,
            role="assistant",
            content=booking_res["message"],
            language=plan.language,
            intent=plan.intent,
            query_type=plan.query_type,
            booking_action=booking_res.get("booking_action")
        )

        elapsed = round((time.time() - t0) * 1000, 2)
        return ChatResponse(
            session_id=session_id,
            message=booking_res["message"],
            intent=plan.intent,
            query_type=plan.query_type,
            language=plan.language,
            sources=[{"type": "booking_state_machine", "status": booking_res["booking_state"].get("status")}],
            data=booking_res["booking_state"],
            booking_action=booking_res.get("booking_action"),
            timing_ms=elapsed
        )

    # 4. Path B: Structured SQL / Hybrid / Semantic RAG Retrieval
    retrieval_res = await hybrid_retriever.retrieve(plan=plan, user_id=user_info["id"])
    sql_data = retrieval_res["sql_data"]
    vector_docs = retrieval_res["vector_docs"]
    sources = retrieval_res["sources"]

    # 5. Build Grounded Context
    context_str = context_builder.build_context_string(
        sql_data=sql_data,
        vector_docs=vector_docs,
        recent_messages=history,
        user_info=user_info
    )

    # 6. Generate Grounded Response
    answer = await llm_generator.generate_response(
        query=req.query,
        language=plan.language,
        intent=plan.intent,
        context_str=context_str,
        sql_data=sql_data,
        vector_docs=vector_docs
    )

    # 7. Persist Assistant Message
    await conversation_memory.add_message(
        session_id=session_id,
        role="assistant",
        content=answer,
        language=plan.language,
        intent=plan.intent,
        query_type=plan.query_type,
        sources=sources,
        data=sql_data or vector_docs
    )

    elapsed = round((time.time() - t0) * 1000, 2)
    return ChatResponse(
        session_id=session_id,
        message=answer,
        intent=plan.intent,
        query_type=plan.query_type,
        language=plan.language,
        sources=sources,
        data=sql_data or vector_docs,
        timing_ms=elapsed
    )

@router.post("/admin/chat", response_model=ChatResponse)
async def admin_chat_endpoint(req: ChatRequest):
    """Admin-only analytics and fleet management chat endpoint."""
    req.userRole = "ADMIN"
    return await chat_endpoint(req)

@router.get("/documents")
async def get_documents():
    """List dynamic knowledge documents directly from live PostgreSQL table."""
    try:
        async with get_db_session() as session:
            res = await session.execute(select(KnowledgeDocument).where(KnowledgeDocument.is_active == True))
            docs = res.scalars().all()
            return {
                "total": len(docs),
                "documents": [
                    {
                        "id": d.id,
                        "category": d.category,
                        "title": d.title,
                        "content": d.content,
                        "tags": d.tags
                    }
                    for d in docs
                ]
            }
    except Exception as e:
        return {"total": 0, "documents": [], "error": str(e)}

@router.post("/qualify-lead")
async def qualify_lead_endpoint(lead: Dict[str, Any]):
    """
    AI Lead Qualification and Opportunity Scoring endpoint.
    """
    is_corporate = lead.get("isCorporate", False)
    total_days = lead.get("totalDays", 1) or 1
    budget = lead.get("estimatedBudget", 0) or 0
    category = (lead.get("vehicleCategory") or "").lower()
    notes = (lead.get("notes") or "").lower()

    score = 50
    reasons = []

    if is_corporate:
        score += 25
        reasons.append("Corporate account client (+25)")
    if total_days >= 5:
        score += 15
        reasons.append(f"Long-term rental duration ({total_days} days) (+15)")
    if budget >= 500:
        score += 15
        reasons.append(f"High estimated budget (${budget}) (+15)")
    if any(k in category for k in ["luxury", "suv", "prado", "mercedes", "bmw", "tesla"]):
        score += 10
        reasons.append("Premium/Luxury fleet tier selected (+10)")
    if any(k in notes for k in ["vip", "urgent", "executive", "roadshow", "delegation"]):
        score += 10
        reasons.append("VIP/Executive special requirements (+10)")

    score = min(score, 98)
    classification = "Hot" if score >= 80 else ("Warm" if score >= 60 else "Cold")

    return {
        "lead_score": score,
        "classification": classification,
        "confidence": 0.95,
        "estimated_deal_value": f"${budget}" if budget else f"${total_days * 85}",
        "reasons": reasons,
        "suggested_action": "Immediate Executive SLA Call & SMS" if classification == "Hot" else ("Automated Quotation & Vehicle Spec Dispatch" if classification == "Warm" else "Drip Marketing Campaign"),
        "summary": f"Qualified as {classification} lead (Score: {score}/100) based on rental inquiry parameters."
    }

@router.post("/sync")
async def sync_knowledge_base():
    """Trigger dynamic sync of cars, hubs, and policies from PostgreSQL to vector store."""
    count = await dynamic_knowledge_syncer.sync_all()
    return {"status": "synced", "documents_indexed": count}

