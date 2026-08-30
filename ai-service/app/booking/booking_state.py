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
                return "আপনি কোন গাড়িটি বুক করতে আগ্রহী? (যেমন: SUV, Toyota Prado, Hyundai Tucson, বা Camry)"
            elif language == "banglish":
                return "Apni kon gari book korte chan? (Jemon: SUV, Toyota Prado, Hyundai Tucson, ba Camry)"
            else:
                return "Which vehicle would you prefer to reserve? (e.g., SUV, Toyota Prado, Hyundai Tucson, or Camry)"

        elif next_f == "pickup_date":
            if language == "bangla":
                return f"{self.car_name or 'গাড়িটি'} কোন তারিখে আপনার প্রয়োজন হবে? (যেমন: আগামীকাল বা ৪ সেপ্টেম্বর)"
            elif language == "banglish":
                return f"{self.car_name or 'Car-ti'} kon date e lagbe? (Jemon: agamikal ba 4 tarik)"
            else:
                return f"On which date would you like to schedule pickup for {self.car_name or 'the vehicle'}?"

        elif next_f == "pickup_location":
            if language == "bangla":
                return "আপনার সুবিধাজনক পিকআপ লোকেশন কোথায় হবে? (যেমন: সোনাডাঙ্গা, গুলশান, বা এয়ারপোর্ট)"
            elif language == "banglish":
                return "Apnar pickup location kothay hobe? (Jemon: Sonadanga, Gulshan, ba Dhaka Airport)"
            else:
                return "Where would you like our chauffeur to meet you for vehicle pickup?"

        elif next_f == "pickup_time":
            if language == "bangla":
                return "সকাল বা বিকালের কোন সময়ে গাড়িটি ডেলিভারি চান? (যেমন: সকাল ১১:০০ টায় বা ৮:০০ টায়)"
            elif language == "banglish":
                return "Gari ti kokhon deliver korbo? (Jemon: sokal 11:00 AM ba 8:00 AM)"
            else:
                return "What time would you prefer for vehicle pickup? (e.g., 11:00 AM or 8:00 AM)"

        return ""
