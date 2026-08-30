import asyncio
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.generation.prompt_templates import SYSTEM_RAG_AGENT_PROMPT

genai_client = None
if settings.GEMINI_API_KEY:
    try:
        from google import genai
        genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
    except Exception as e:
        print(f"[LLMGenerator] Gemini client notice: {e}. Using resilient grounded synthesizer.")

class LLMGenerator:
    @classmethod
    async def generate_response(
        cls,
        query: str,
        language: str,
        intent: str,
        context_str: str,
        sql_data: Optional[List[Dict[str, Any]]] = None,
        vector_docs: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Generates a grounded response using Gemini Flash or deterministic fallback.
        """
        prompt = SYSTEM_RAG_AGENT_PROMPT.format(
            context_str=context_str,
            user_query=query,
            detected_language=language,
            intent=intent
        )

        # 1. Try Gemini Models with Multi-Model Fallback Cascade
        if genai_client and settings.GEMINI_API_KEY:
            model_candidates = [settings.GEMINI_MODEL] + settings.fallback_model_list
            for model_name in model_candidates:
                try:
                    response = await asyncio.wait_for(
                        asyncio.to_thread(
                            genai_client.models.generate_content,
                            model=model_name,
                            contents=prompt
                        ),
                        timeout=5.0
                    )
                    if response and response.text:
                        return response.text.strip()
                except Exception:
                    continue

        # 2. Resilient Deterministic Grounded Synthesis Fallback
        return cls._synthesize_grounded_fallback(query, language, intent, sql_data, vector_docs)

    @classmethod
    def _synthesize_grounded_fallback(
        cls,
        query: str,
        language: str,
        intent: str,
        sql_data: Optional[List[Dict[str, Any]]] = None,
        vector_docs: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Deterministic multilingual template synthesis directly from database truth."""
        # 1. Availability / Search / Price
        if intent in ["car_availability", "car_search", "price_inquiry"]:
            if not sql_data:
                if language == "banglish":
                    return "Bortomane ei category ba location e kono car available pawa jayni. Onno kono car ba location dekhte chan?"
                elif language == "bangla":
                    return "বর্তমানে এই ক্যাটাগরি বা লোকেশনে কোনো গাড়ি অ্যাভেইলেবল পাওয়া যায়নি।"
                else:
                    return "No available vehicles found matching your criteria at this moment."

            lines = []
            if language == "banglish":
                lines.append(f"Amader database e {len(sql_data)} ta car available ache:")
                for i, c in enumerate(sql_data[:5], 1):
                    lines.append(f"{i}. **{c.get('name')}** — ${c.get('dailyRate')}/day ({c.get('seats', 5)} seats, {c.get('category', 'Standard')})")
                lines.append("\nKono car ti apnar pochondo hoyeche? Book korte chaile bolun!")
            elif language == "bangla":
                lines.append(f"আমাদের ডেটাবেসে {len(sql_data)} টি গাড়ি অ্যাভেইলেবল রয়েছে:")
                for i, c in enumerate(sql_data[:5], 1):
                    lines.append(f"{i}. **{c.get('name')}** — ${c.get('dailyRate')}/দিন ({c.get('seats', 5)} আসন, {c.get('category', 'Standard')})")
                lines.append("\nকোন গাড়িটি বুক করতে চান জানাবেন।")
            else:
                lines.append(f"We have {len(sql_data)} vehicles currently available:")
                for i, c in enumerate(sql_data[:5], 1):
                    lines.append(f"{i}. **{c.get('name')}** — ${c.get('dailyRate')}/day ({c.get('seats', 5)} seats, {c.get('category', 'Standard')})")
                lines.append("\nWould you like to reserve any of these vehicles?")

            return "\n".join(lines)

        # 2. User Bookings Lookup
        if intent == "booking_lookup":
            if not sql_data:
                return "Apnar kono active booking record pawa jayni." if language == "banglish" else "No active bookings found for your account."

            lines = ["Apnar booking records:" if language == "banglish" else "Your booking records:"]
            for b in sql_data:
                lines.append(f"- **{b.get('bookingCode')}**: {b.get('car_name')} | Status: {b.get('status')} | Total: ${b.get('totalAmount')}")
            return "\n".join(lines)

        # 3. User Payment Status
        if intent == "payment_status":
            if not sql_data:
                return "Kono payment record pawa jayni." if language == "banglish" else "No payment records found."
            lines = ["Apnar payment details:" if language == "banglish" else "Your payment records:"]
            for p in sql_data:
                lines.append(f"- Booking #{p.get('bookingId')}: ${p.get('amount')} ({p.get('paymentStatus')}) via {p.get('paymentMethod')}")
            return "\n".join(lines)

        # 4. Admin Revenue / Most Rented / Maintenance
        if intent == "admin_revenue" and sql_data:
            d = sql_data[0]
            return f"📊 **Revenue Analytics**:\n- Total Bookings: {d.get('total_bookings')}\n- Total Revenue: ${d.get('total_revenue')}\n- Average Booking Value: ${d.get('avg_booking_value')}"

        if intent == "admin_most_rented" and sql_data:
            lines = ["🏆 **Most Rented Fleet Vehicles**:"]
            for i, c in enumerate(sql_data, 1):
                lines.append(f"{i}. {c.get('name')} — {c.get('rental_count')} completed rentals")
            return "\n".join(lines)

        if intent == "admin_maintenance" and sql_data:
            lines = ["🔧 **Vehicles Requiring Maintenance**:"]
            for m in sql_data:
                lines.append(f"- {m.get('car_name')}: {m.get('title')} (Est: ${m.get('estimatedCost')})")
            return "\n".join(lines)

        # 5. Policies & FAQ
        if vector_docs:
            d = vector_docs[0]
            if language == "banglish":
                return f"Amader official policy ({d.get('title')}):\n\n{d.get('content')}"
            elif language == "bangla":
                return f"আমাদের অফিসিয়াল নিয়মাবলী ({d.get('title')}):\n\n{d.get('content')}"
            else:
                return f"According to our official guidelines ({d.get('title')}):\n\n{d.get('content')}"

        # 6. Greetings
        if intent == "greeting":
            if language == "banglish":
                return "Hello! Best Care Car Rental এ আপনাকে স্বাগতম। গাড়ি খোঁজা, ভাড়া জানা বা বুকিং করতে আমি কিভাবে সাহায্য করতে পারি?"
            elif language == "bangla":
                return "আসসালামু আলাইকুম! বেস্ট কেয়ার কার রেন্টালে স্বাগতম। আপনি কি কোনো নির্দিষ্ট গাড়ি বা ভ্রমণের জন্য গাড়ি খুঁজছেন?"
            else:
                return "Welcome to Best Care Car Rental! How may I assist you with vehicle availability, rental policies, or reservations today?"

        return "How may I help you with your car rental today?"

llm_generator = LLMGenerator()
