from typing import Dict, Any, Optional, List
from app.booking.booking_state import BookingState
from app.booking.booking_client import booking_client
from app.query.entity_extractor import VEHICLE_PATTERNS

class BookingHandler:
    @classmethod
    async def process_turn(
        cls,
        query: str,
        entities: Dict[str, Any],
        language: str,
        current_state_dict: Optional[Dict[str, Any]] = None,
        recent_messages: Optional[List[Dict[str, Any]]] = None,
        user_info: Optional[Dict[str, Any]] = None,
        auth_header: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Orchestrates multi-turn conversational booking slot-filling and confirmation.
        """
        state = BookingState(**(current_state_dict or {}))

        # 1. Check for Cancellation
        if entities.get("is_cancellation"):
            state.status = "cancelled"
            if language == "bangla":
                msg = "আপনার বুকিং প্রসেস বাতিল করা হয়েছে। আর কোনো প্রশ্ন বা সাহায্য লাগলে জানাবেন।"
            elif language == "banglish":
                msg = "Apnar booking process cancel kora hoyeche. Aro kono proshno thakle bolte paren."
            else:
                msg = "Your booking process has been cancelled. Let me know if you need anything else."
            return {
                "message": msg,
                "booking_state": state.model_dump(),
                "booking_action": {"status": "cancelled"}
            }

        # 2. Check for Confirmation when in 'confirming' state
        if state.status == "confirming" and entities.get("is_confirmation"):
            res = await booking_client.create_booking(state.model_dump(), user_info=user_info, auth_header=auth_header)
            state.status = "booked"
            state.booking_code = res.get("bookingCode")

            if language == "bangla":
                msg = (
                    f"✅ **বুকিং নিশ্চিত হয়েছে!**\n\n"
                    f"📋 **বুকিং কোড:** `{state.booking_code}`\n"
                    f"🚗 **গাড়ি:** {state.car_name}\n"
                    f"📅 **তারিখ ও সময়:** {state.pickup_date}, {state.pickup_time}\n"
                    f"📍 **পিকআপ:** {state.pickup_location}\n"
                    f"📍 **ড্রপঅফ:** {state.dropoff_location or state.pickup_location}\n"
                    f"💰 **মোট ভাড়া:** ${state.total_amount}\n\n"
                    f"আমাদের ড্রাইভার ও সাপোর্ট টিম সময়মতো আপনার সাথে যোগাযোগ করবে।"
                )
            elif language == "banglish":
                msg = (
                    f"✅ **Booking Confirm Hoyeche!**\n\n"
                    f"📋 **Booking Code:** `{state.booking_code}`\n"
                    f"🚗 **Car:** {state.car_name}\n"
                    f"📅 **Date & Time:** {state.pickup_date}, {state.pickup_time}\n"
                    f"📍 **Pickup:** {state.pickup_location}\n"
                    f"📍 **Dropoff:** {state.dropoff_location or state.pickup_location}\n"
                    f"💰 **Total:** ${state.total_amount}\n\n"
                    f"Amader driver & support team timely apnar sathe jogajog korbe."
                )
            else:
                msg = (
                    f"✅ **Reservation Confirmed!**\n\n"
                    f"📋 **Booking Code:** `{state.booking_code}`\n"
                    f"🚗 **Vehicle:** {state.car_name}\n"
                    f"📅 **Pickup:** {state.pickup_date} at {state.pickup_time}\n"
                    f"📍 **From:** {state.pickup_location}\n"
                    f"📍 **To:** {state.dropoff_location or state.pickup_location}\n"
                    f"💰 **Total:** ${state.total_amount}\n\n"
                    f"Our chauffeur and dispatch team will arrive promptly at your scheduled time."
                )

            return {
                "message": msg,
                "booking_state": state.model_dump(),
                "booking_action": {
                    "status": "booked",
                    "booking_code": state.booking_code,
                    "booking_id": res.get("bookingId")
                }
            }

        # 3. If starting a new booking, move to 'collecting'
        if state.status in ["idle", "cancelled", "booked"]:
            state = BookingState(status="collecting")

        # 4. Fill Slots from Current Query Entities
        if entities.get("vehicle_name"):
            state.car_name = entities["vehicle_name"]
            state.car_id = entities.get("vehicle_id")
            state.car_category = entities.get("category")
        elif entities.get("category") and not state.car_category:
            state.car_category = entities["category"]
            # Auto-assign standard flagship for category if not specified
            if state.car_category == "SUV":
                state.car_name = "Toyota Land Cruiser Prado TX"
                state.car_id = "car_prado_suv"
                state.daily_rate = 145.0
            elif state.car_category == "Sedan":
                state.car_name = "Toyota Camry Premium Hybrid"
                state.car_id = "car_camry_hybrid"
                state.daily_rate = 70.0

        if entities.get("pickup_date"):
            state.pickup_date = entities["pickup_date"]
        if entities.get("dropoff_date"):
            state.dropoff_date = entities["dropoff_date"]
        if entities.get("pickup_time"):
            state.pickup_time = entities["pickup_time"]
        if entities.get("pickup_location"):
            state.pickup_location = entities["pickup_location"]
        if entities.get("dropoff_location"):
            state.dropoff_location = entities["dropoff_location"]
        if entities.get("duration_days"):
            state.total_days = entities["duration_days"]

        # 5. Resolve Car from Previous History if still missing
        if not state.car_name and recent_messages:
            for m in reversed(recent_messages):
                text_content = m.get("content", "").lower()
                for v_key, v_info in VEHICLE_PATTERNS.items():
                    if v_key in text_content:
                        state.car_name = v_info["name"]
                        state.car_id = v_info["id"]
                        state.car_category = v_info["category"]
                        state.daily_rate = v_info["dailyRate"]
                        break
                if state.car_name:
                    break

        # Set default daily rate if car identified
        if state.car_name and not state.daily_rate:
            for v_info in VEHICLE_PATTERNS.values():
                if v_info["name"].lower() in state.car_name.lower():
                    state.daily_rate = float(v_info["dailyRate"])
                    state.car_id = v_info["id"]
                    break

        # 6. Check Completeness
        if state.is_complete():
            state.status = "confirming"
            state.calculate_total()

            if language == "bangla":
                preview = (
                    f"📋 **বুকিং বিবরণী (Summary):**\n"
                    f"🚗 **গাড়ি:** {state.car_name} (${state.daily_rate}/দিন)\n"
                    f"📅 **তারিখ ও সময়:** {state.pickup_date}, {state.pickup_time}\n"
                    f"📍 **পিকআপ:** {state.pickup_location}\n"
                    f"📍 **ড্রপঅফ:** {state.dropoff_location or state.pickup_location}\n"
                    f"💰 **মোট ভাড়া:** ${state.total_amount} ({state.total_days} দিন)\n\n"
                    f"**আপনি কি এটি নিশ্চিত (Confirm) করতে চান? (হ্যাঁ / না)**"
                )
            elif language == "banglish":
                preview = (
                    f"📋 **Booking Summary:**\n"
                    f"🚗 **Car:** {state.car_name} (${state.daily_rate}/day)\n"
                    f"📅 **Date & Time:** {state.pickup_date}, {state.pickup_time}\n"
                    f"📍 **Pickup:** {state.pickup_location}\n"
                    f"📍 **Dropoff:** {state.dropoff_location or state.pickup_location}\n"
                    f"💰 **Total:** ${state.total_amount} ({state.total_days} day)\n\n"
                    f"**Apni ki confirm korte chan? (Haan / Na)**"
                )
            else:
                preview = (
                    f"📋 **Reservation Summary:**\n"
                    f"🚗 **Vehicle:** {state.car_name} (${state.daily_rate}/day)\n"
                    f"📅 **Schedule:** {state.pickup_date} at {state.pickup_time}\n"
                    f"📍 **Pickup:** {state.pickup_location}\n"
                    f"📍 **Dropoff:** {state.dropoff_location or state.pickup_location}\n"
                    f"💰 **Estimated Total:** ${state.total_amount} ({state.total_days} day)\n\n"
                    f"**Would you like to confirm this reservation? (Yes / No)**"
                )

            return {
                "message": preview,
                "booking_state": state.model_dump(),
                "booking_action": {
                    "status": "confirming",
                    "collected": state.model_dump(),
                    "missing": []
                }
            }

        # 7. Still Missing Slots -> Ask Next Question
        next_q = state.next_question_prompt(language=language)
        state.last_question = next_q

        # Add brief positive feedback about what was just captured
        prefix = ""
        if state.car_name and not current_state_dict.get("car_name"):
            prefix = f"{state.car_name} select korechi ✓\n" if language == "banglish" else f"{state.car_name} নির্বাচন করা হয়েছে।\n"

        return {
            "message": f"{prefix}{next_q}".strip(),
            "booking_state": state.model_dump(),
            "booking_action": {
                "status": "collecting",
                "collected": state.model_dump(),
                "missing": state.missing_fields()
            }
        }

booking_handler = BookingHandler()
