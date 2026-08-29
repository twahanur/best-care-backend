"""
AI Lead Qualification & Scoring Engine.
Analyzes incoming customer rental inquiries, trip requirements, duration, and budget to prioritize high-value leads.
"""
from typing import Dict, Any, Optional

class LeadScorer:
    @staticmethod
    def score_lead(
        customer_name: str,
        customer_email: str,
        vehicle_category: str,
        duration_days: int,
        estimated_budget: Optional[float] = None,
        trip_purpose: Optional[str] = None,
        notes: Optional[str] = None,
        is_corporate: bool = False
    ) -> Dict[str, Any]:
        """
        Calculates an intelligent lead quality score (0 to 100) and assigns classification:
        - Hot (80-100): High conversion probability, high ticket value, corporate/long-term
        - Warm (50-79): Moderate ticket, standard rental
        - Cold (0-49): Low budget, ambiguous timeframe, short duration
        """
        score = 50.0  # Base starting score
        reasons = []

        # 1. Rental Duration Multiplier
        if duration_days >= 7:
            score += 25.0
            reasons.append(f"Long-term rental duration ({duration_days} days) represents high total contract value.")
        elif duration_days >= 3:
            score += 15.0
            reasons.append(f"Multi-day rental ({duration_days} days) qualifies for unlimited mileage tier.")
        elif duration_days == 1:
            score -= 10.0
            reasons.append("Single day rental with lower lifetime value.")

        # 2. Vehicle Category & Luxury Potential
        cat_lower = vehicle_category.lower()
        if "luxury" in cat_lower or "executive" in cat_lower or "mercedes" in cat_lower or "mustang" in cat_lower:
            score += 20.0
            reasons.append("High-tier premium vehicle requested with elevated profit margins.")
        elif "suv" in cat_lower or "van" in cat_lower:
            score += 10.0
            reasons.append("Family/Group transport vehicle category.")
        elif "budget" in cat_lower or "economy" in cat_lower:
            score += 0.0

        # 3. Corporate / Business Status
        if is_corporate or (trip_purpose and "business" in trip_purpose.lower()):
            score += 15.0
            reasons.append("Corporate client profile with recurring rental contract potential.")

        # 4. Budget Adequacy
        if estimated_budget and estimated_budget > (duration_days * 120):
            score += 10.0
            reasons.append("Generous budget headroom indicated.")
        elif estimated_budget and estimated_budget < (duration_days * 45):
            score -= 15.0
            reasons.append("Tight budget constraint relative to fleet average.")

        # 5. Notes & Special Requests Analysis
        if notes and any(k in notes.lower() for k in ["urgent", "airport pickup", "chauffeur", "vip", "today", "tomorrow"]):
            score += 10.0
            reasons.append("High intent and urgent execution timeline specified in booking remarks.")

        # Clamp score between 10 and 99
        final_score = int(max(10, min(99, score)))

        # Categorize
        if final_score >= 80:
            classification = "Hot"
            priority = "High (Immediate 15-min SLA)"
            suggested_action = "Assign dedicated account manager, send priority quote with VIP Full Shield upgrade."
        elif final_score >= 55:
            classification = "Warm"
            priority = "Medium (Within 2 hours)"
            suggested_action = "Send automated booking confirmation email with vehicle spec sheet."
        else:
            classification = "Cold"
            priority = "Low (Standard Queue)"
            suggested_action = "Send standard automated quotation with economy discount code."

        # Estimated contract revenue
        base_rate = 130 if "luxury" in cat_lower else (95 if "suv" in cat_lower else 65)
        estimated_contract_value = duration_days * base_rate

        return {
            "customer_name": customer_name,
            "customer_email": customer_email,
            "lead_score": final_score,
            "classification": classification,
            "priority": priority,
            "estimated_value_usd": estimated_contract_value,
            "conversion_probability_pct": min(95, int(final_score * 0.95)),
            "scoring_rationale": reasons,
            "suggested_sales_action": suggested_action
        }
