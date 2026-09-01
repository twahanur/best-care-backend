import re
from typing import Dict, Any, Optional

class IntentClassifier:
    @staticmethod
    def classify(query: str, booking_state: Optional[Dict[str, Any]] = None, user_role: str = "CUSTOMER") -> str:
        """
        Classifies user intent from rich natural language inquiry in English, Bangla, and Banglish.
        """
        q = query.lower().strip()
        state_status = (booking_state or {}).get("status", "idle")

        # 1. Active Booking State Flow Overrides
        if state_status in ["collecting", "confirming"]:
            if re.search(r"\b(cancel|no|na|nah|bad\s*dao|dorkar\s*nai|lagbe\s*na|stop|pore\s*korbo|nevermind|not\s*now)\b", q):
                return "booking_cancel_request"
            if state_status == "confirming" and re.search(r"\b(haan|ha|yes|confirm|thik\s*ache|shob\s*thik|proceed|sure|koro|korbo|book\s*it|done|cholo|ok|okay|agree)\b", q):
                return "booking_confirm"
            return "booking_create"

        # 2. Direct Booking Request Trigger (Natural variations)
        if re.search(r"\b(book\s*koro|book\s*korbo|booking\s*koro|booking\s*korbo|reserve\s*koro|rent\s*koro|book\s*it|rent\s*this|car\s*book|gari\s*book|book\s*a\s*car|reserve\s*this)\b", q) or \
           re.search(r"\b(book\s*korte\s*chai|booking\s*korte\s*chai|nite\s*chai|rent\s*nite\s*chai|gari\s*nite\s*chai|reserve\s*korte\s*chai|boking|booking\s*dorkar)\b", q) or \
           re.search(r"\b(i\s*want\s*to\s*book|can\s*i\s*book|please\s*book|i\s*need\s*to\s*rent|book\s*now|make\s*a\s*reservation)\b", q) or \
           re.search(r"\b(suv\s*book|sedan\s*book|prado\s*book|tucson\s*book|hiace\s*book|camry\s*book|tesla\s*book|audi\s*book|mercedes\s*book|jaguar\s*book|bmw\s*book)\b", q):
            return "booking_create"

        # 3. Analytics & Operational Metrics Queries (Bookings count, revenue, stats, reports, graphs, tables)
        if re.search(r"\b(koyta\s*booking|koyti\s*booking|how\s*many\s*bookings|total\s*booking|booking\s*count|number\s*of\s*bookings|booking\s*hoice|booking\s*hoyse|booking\s*shongkha)\b", q) or \
           re.search(r"\b(revenue|income|earning|taka|mot\s*taka|total\s*revenue|sales|mot\s*ay|ay\s*koto|koto\s*taka\s*income|day\s*wise|daily\s*report|chart|graph|table|report\s*generate)\b", q) or \
           (re.search(r"\b(last\s*30\s*din|last\s*month|gawto\s*mash|30\s*dine|7\s*dine|last\s*week)\b", q) and "booking" in q):
            return "admin_revenue"

        if re.search(r"\b(most\s*rented|popular|bestselling|top\s*car|beshi\s*rent|shobcheye\s*beshi|car\s*basis|car\s*wise|gari\s*basis)\b", q):
            return "admin_most_rented"

        if re.search(r"\b(maintenance|servicing|reparation|repair|problem|gari\s*kharap)\b", q):
            return "admin_maintenance"

        # 4. User Personal Data Lookups
        if re.search(r"\b(amar\s*booking|my\s*booking|my\s*rentals|booking\s*status|amar\s*reservation|upcoming\s*trip)\b", q):
            return "booking_lookup"
        if re.search(r"\b(amar\s*payment|my\s*payment|invoice|payment\s*status|paid\s*amount)\b", q):
            return "payment_status"

        # 5. Policies, Deposit, Refund, Driver, Mileage
        if re.search(r"\b(deposit|security\s*deposit|refund|cancellation\s*policy|cancel\s*policy|ferot|return|taka\s*kobe)\b", q):
            return "policy_inquiry"
        if re.search(r"\b(insurance|cdw|protection|bima|coverage|shield|excess|deductible)\b", q):
            return "insurance_inquiry"
        if re.search(r"\b(mileage|fuel|gas|petrol|license|age|document|driver|chauffeur|self\s*drive|unlimited)\b", q):
            return "policy_inquiry"

        # 6. Availability & Live Inventory Queries
        if re.search(r"\b(available|availability|ache|pawa\s*jabe|khali|free|dekhao|list|inventory)\b", q) and \
           re.search(r"\b(car|gari|vehicle|suv|sedan|khulna|dhaka|chittagong|sylhet|banani|gulshan|airport)\b", q):
            return "car_availability"

        # 7. Pricing & Rate Inquiries
        if re.search(r"\b(price|rate|cost|bhara|khoroch|koto|discount|coupon|offer|daily\s*rate|cheapest|shosta|package)\b", q):
            return "price_inquiry"

        # 8. Recommendations (Trip, Passenger capacity, Fleet selection)
        if re.search(r"\b(sajek|bandarban|sylhet|jaflong|pahar|pahari|mountain|offroad|4wd|hill|rough|cox|tour|trip)\b", q):
            return "trip_recommendation"
        if re.search(r"\b(recommend|suggest|bhalo\s*hobe|best\s*hobe|family|group|wedding|corporate|vip|konta\s*bhalo|konta\s*nebo)\b", q):
            return "car_recommendation"
        if re.search(r"\b(seat|seater|jon|joner|passenger|capacity|koyjon)\b", q):
            return "car_recommendation"

        # 9. Structured Car Search (Specific specs/fuel)
        if re.search(r"\b(automatic|manual|diesel|hybrid|electric|octane|petrol|sunroof|leather)\b", q):
            return "car_search"

        # 10. Greetings & Courtesy
        if re.search(r"^(hi|hello|hey|assalamualaikum|salam|kemon\s*achen|greetings|good\s*morning|good\s*evening)$", q):
            return "greeting"
        if re.search(r"\b(thanks|thank\s*you|dhonnobad|welcome|shukriya)\b", q):
            return "thanks"

        return "general_faq"

intent_classifier = IntentClassifier()
