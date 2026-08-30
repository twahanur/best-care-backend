import re
from typing import Dict, Any, Optional

class IntentClassifier:
    @staticmethod
    def classify(query: str, booking_state: Optional[Dict[str, Any]] = None, user_role: str = "CUSTOMER") -> str:
        """
        Classifies user intent from natural language inquiry.
        """
        q = query.lower().strip()
        state_status = (booking_state or {}).get("status", "idle")

        # 1. Active Booking State Flow Overrides
        if state_status in ["collecting", "confirming"]:
            if re.search(r"\b(cancel|no|na|bad dao|dorkar nai|stop)\b", q):
                return "booking_cancel_request"
            if state_status == "confirming" and re.search(r"\b(haan|yes|confirm|thik ache|proceed|sure|koro|korbo|book it)\b", q):
                return "booking_confirm"
            return "booking_create"

        # 2. Direct Booking Request Trigger
        if re.search(r"\b(book\s*koro|book\s*korbo|booking\s*koro|reserve\s*koro|rent\s*koro|book\s*it|rent\s*this|car\s*book|gari\s*book|book\s*a\s*car|reserve\s*this)\b", q) or \
           re.search(r"\b(suv\s*book|sedan\s*book|prado\s*book|tucson\s*book|hiace\s*book|camry\s*book|tesla\s*book)\b", q):
            return "booking_create"

        # 3. Admin Analytics Queries (Role-Gated or Explicit Analytics)
        if user_role == "ADMIN" or "admin" in q:
            if re.search(r"\b(revenue|income|earning|taka|mot\s*taka|total\s*revenue|sales)\b", q):
                return "admin_revenue"
            if re.search(r"\b(most\s*rented|popular|bestselling|top\s*car|beshi\s*rent)\b", q):
                return "admin_most_rented"
            if re.search(r"\b(maintenance|servicing|reparation|repair|problem)\b", q):
                return "admin_maintenance"

        # 4. User Personal Data Lookups
        if re.search(r"\b(amar\s*booking|my\s*booking|my\s*rentals|booking\s*status|amar\s*reservation|upcoming\s*trip)\b", q):
            return "booking_lookup"
        if re.search(r"\b(amar\s*payment|my\s*payment|invoice|payment\s*status|paid\s*amount)\b", q):
            return "payment_status"

        # 5. Policies & Insurance (High priority before generic pricing)
        if re.search(r"\b(deposit|security\s*deposit|refund|cancellation\s*policy|cancel\s*policy|ferot|return)\b", q):
            return "policy_inquiry"
        if re.search(r"\b(insurance|cdw|protection|bima|coverage|shield|excess|deductible)\b", q):
            return "insurance_inquiry"
        if re.search(r"\b(mileage|fuel|gas|petrol|license|age|document|driver\s*age|unlimited)\b", q):
            return "policy_inquiry"

        # 6. Availability & Live Inventory Queries
        if re.search(r"\b(available|availability|ache|pawa\s*jabe|khali|free|dekhao|list)\b", q) and \
           re.search(r"\b(car|gari|vehicle|suv|sedan|khulna|dhaka|chittagong|sylhet|banani|gulshan)\b", q):
            return "car_availability"

        # 7. Pricing & Rate Inquiries
        if re.search(r"\b(price|rate|cost|bhara|khoroch|koto|discount|coupon|offer|daily\s*rate|cheapest|shosta)\b", q):
            return "price_inquiry"

        # 8. Recommendations (Trip & Fleet)
        if re.search(r"\b(sajek|bandarban|sylhet|jaflong|pahar|pahari|mountain|offroad|4wd|hill|rough)\b", q):
            return "trip_recommendation"
        if re.search(r"\b(recommend|suggest|bhalo\s*hobe|family|tour|group|wedding|corporate|vip)\b", q):
            return "car_recommendation"

        # 9. Structured Car Search (Specific specs/seats)
        if re.search(r"\b(seat|seater|jon|capacity|automatic|manual|diesel|hybrid|electric)\b", q):
            return "car_search"

        # 10. Greetings & Courtesy
        if re.search(r"^(hi|hello|hey|assalamualaikum|kemon\s*achen|greetings)$", q):
            return "greeting"
        if re.search(r"\b(thanks|thank\s*you|dhonnobad|welcome)\b", q):
            return "thanks"

        return "general_faq"

intent_classifier = IntentClassifier()
