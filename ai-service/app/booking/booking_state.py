from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class BookingState(BaseModel):
    status: str = "idle"  # 'idle' | 'collecting' | 'confirming' | 'booked' | 'cancelled'
    car_id: Optional[str] = None
    car_name: Optional[str] = None
    car_category: Optional[str] = None
    daily_rate: Optional[float] = None
    pickup_date: Optional[str] = None
    dropoff_date: Optional[str] = None
    pickup_time: Optional[str] = None
    pickup_location: Optional[str] = None
    dropoff_location: Optional[str] = None
    total_days: int = 1
    total_amount: Optional[float] = None
    booking_code: Optional[str] = None
    last_question: Optional[str] = None

    def missing_fields(self) -> List[str]:
        """Identifies mandatory fields still needed to complete a car rental reservation."""
        missing = []
        if not self.car_name and not self.car_id and not self.car_category:
            missing.append("car")
        if not self.pickup_date:
            missing.append("pickup_date")
        if not self.pickup_location:
            missing.append("pickup_location")
        if not self.pickup_time:
            missing.append("pickup_time")
        return missing

    def is_complete(self) -> bool:
        return len(self.missing_fields()) == 0

    def calculate_total(self) -> float:
        rate = self.daily_rate or 85.0
        days = max(1, self.total_days)
        self.total_amount = round(rate * days, 2)
        return self.total_amount

    def next_question_prompt(self, language: str = "banglish") -> str:
        missing = self.missing_fields()
        if not missing:
            return ""

        next_f = missing[0]
        if next_f == "car":
            if language == "bangla":
                return "আপনি কোন গাড়িটি বুক করতে চান? (যেমন: SUV, Prado, Camry, Tucson, HiAce) অথবা আপনি কি আমাদের সেরা অপশন দেখতে চান?"
            elif language == "banglish":
                return "Apni kon car book korte chan? (Jemon: SUV, Prado, Camry, Tucson, HiAce) nicher theke bolte paren."
            else:
                return "Which vehicle would you like to book? (e.g., SUV, Prado, Camry, Tucson, HiAce)"

        elif next_f == "pickup_date":
            if language == "bangla":
                return f"{self.car_name or 'গাড়িটি'} কোন তারিখে বুক করতে চান? (যেমন: আগামীকাল বা ৪ তারিখ)"
            elif language == "banglish":
                return f"{self.car_name or 'Car ti'} kon date e book korte chan? (Jemon: agamikal ba 4 tarik)"
            else:
                return f"For which date would you like to book {self.car_name or 'the car'}?"

        elif next_f == "pickup_location":
            if language == "bangla":
                return "পিকআপ লোকেশন কোথায় হবে? (যেমন: সোনাডাঙ্গা, গুলশান, বা এয়ারপোর্ট)"
            elif language == "banglish":
                return "Pickup location kothay hobe? (Jemon: Sonadanga, Gulshan, ba Airport)"
            else:
                return "Where would you like the vehicle to be picked up from?"

        elif next_f == "pickup_time":
            if language == "bangla":
                return "কয়টার সময় পিকআপ করতে হবে? (যেমন: সকাল ১১টায় বা ৮টায়)"
            elif language == "banglish":
                return "Sokal ba dupur kottay pick korbo? (Jemon: sokal 11 tay ba 8 tay)"
            else:
                return "What time should the pickup be scheduled? (e.g., 11:00 AM or 8:00 AM)"

        return ""
