"""
FastAPI Route Handlers for AI Lead Qualification & Workflow Automation.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from app.services.lead_scorer import LeadScorer

router = APIRouter(prefix="/lead", tags=["AI Lead Qualification"])

class LeadScoreRequest(BaseModel):
    customer_name: str = Field(..., examples=["Tanvir Ahmed"])
    customer_email: str = Field(..., examples=["tanvir@enterprise.com"])
    vehicle_category: str = Field(..., examples=["Luxury SUV"])
    duration_days: int = Field(..., ge=1, examples=[5])
    estimated_budget: Optional[float] = Field(None, examples=[750.0])
    trip_purpose: Optional[str] = Field(None, examples=["Corporate Client Visit"])
    notes: Optional[str] = Field(None, examples=["Urgent request, need airport VIP pickup with English-speaking chauffeur"])
    is_corporate: bool = Field(default=False, examples=[True])

class LeadScoreResponse(BaseModel):
    customer_name: str
    customer_email: str
    lead_score: int
    classification: str
    priority: str
    estimated_value_usd: float
    conversion_probability_pct: int
    scoring_rationale: List[str]
    suggested_sales_action: str

@router.post("/score-and-qualify", response_model=LeadScoreResponse)
async def score_and_qualify_lead(payload: LeadScoreRequest):
    """
    Evaluates incoming leads or bookings and assigns real-time AI Lead Score and automated sales action.
    """
    try:
        result = LeadScorer.score_lead(
            customer_name=payload.customer_name,
            customer_email=payload.customer_email,
            vehicle_category=payload.vehicle_category,
            duration_days=payload.duration_days,
            estimated_budget=payload.estimated_budget,
            trip_purpose=payload.trip_purpose,
            notes=payload.notes,
            is_corporate=payload.is_corporate
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lead qualification failed: {str(e)}")
