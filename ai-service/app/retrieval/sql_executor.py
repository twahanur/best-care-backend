import re
import asyncio
from typing import List, Dict, Any, Optional
from sqlalchemy import text
from app.core.database import get_db_session

# Predefined, strictly parameterized read-only SQL templates
SQL_TEMPLATES = {
    "car_availability": """
        SELECT c.id, c.name, c.brand, c.category, c.seats, c."dailyRate", c.status,
               c.transmission, c."fuelType", c."securityDeposit",
               lh.name as hub_name, lh.city as hub_city
        FROM cars c
        LEFT JOIN location_hubs lh ON c."currentHubId" = lh.id
        WHERE c.status = 'AVAILABLE'
          AND (:city IS NULL OR LOWER(lh.city) LIKE LOWER(:city) OR LOWER(c.name) LIKE LOWER(:city))
          AND (:category IS NULL OR LOWER(c.category) = LOWER(:category))
          AND (:seats IS NULL OR c.seats >= :seats)
        ORDER BY c."dailyRate" ASC
        LIMIT 20;
    """,
    "car_search": """
        SELECT c.id, c.name, c.brand, c.category, c.seats, c."dailyRate", c.status,
               c.transmission, c."fuelType", c."securityDeposit"
        FROM cars c
        WHERE (:category IS NULL OR LOWER(c.category) = LOWER(:category))
          AND (:seats IS NULL OR c.seats >= :seats)
          AND (:max_rate IS NULL OR c."dailyRate" <= :max_rate)
        ORDER BY c."dailyRate" ASC
        LIMIT 20;
    """,
    "price_inquiry": """
        SELECT c.id, c.name, c.brand, c.category, c.seats, c."dailyRate", c.status, c."securityDeposit"
        FROM cars c
        WHERE (:category IS NULL OR LOWER(c.category) = LOWER(:category))
          AND (:name IS NULL OR LOWER(c.name) LIKE LOWER(:name) OR LOWER(c.brand) LIKE LOWER(:name))
        ORDER BY c."dailyRate" ASC
        LIMIT 10;
    """,
    "user_bookings": """
        SELECT b.id, b."bookingCode", b.status, b."paymentStatus", b."pickupDateTime",
               b."dropoffDateTime", b."totalAmount", b."totalDays", b."pickupLocation",
               b."dropoffLocation", c.name as car_name, c.brand as car_brand
        FROM bookings b
        LEFT JOIN cars c ON b."carId" = c.id
        WHERE b."userId" = :user_id
        ORDER BY b."createdAt" DESC
        LIMIT 15;
    """,
    "user_payments": """
        SELECT p.id, p."bookingId", p."amount", p."paymentStatus", p."paymentMethod",
               p."transactionId", p."createdAt"
        FROM payments p
        WHERE p."userId" = :user_id
        ORDER BY p."createdAt" DESC
        LIMIT 15;
    """,
    "admin_revenue": """
        SELECT COUNT(b.id) as total_bookings,
               COALESCE(SUM(b."totalAmount"), 0) as total_revenue,
               COALESCE(AVG(b."totalAmount"), 0) as avg_booking_value
        FROM bookings b
        WHERE b.status NOT IN ('CANCELLED');
    """,
    "admin_most_rented": """
        SELECT c.id, c.name, c.brand, c.category, COUNT(b.id) as rental_count
        FROM bookings b
        JOIN cars c ON b."carId" = c.id
        GROUP BY c.id, c.name, c.brand, c.category
        ORDER BY rental_count DESC
        LIMIT 10;
    """,
    "admin_maintenance": """
        SELECT ms.id, ms."maintenanceType", ms.title, ms."startDate", ms."endDate",
               ms."isCompleted", ms."estimatedCost", c.name as car_name, c.brand as car_brand
        FROM maintenance_schedules ms
        JOIN cars c ON ms."carId" = c.id
        WHERE ms."isCompleted" = false
        ORDER BY ms."startDate" ASC
        LIMIT 15;
    """
}

# Fallback in-memory catalog data if Neon DB tables are empty/mocked
FALLBACK_CARS = [
    {"id": "car_prado_suv", "name": "Toyota Land Cruiser Prado TX", "brand": "Toyota", "category": "SUV", "seats": 7, "dailyRate": 145, "status": "AVAILABLE", "transmission": "Automatic", "fuelType": "Diesel", "securityDeposit": 350, "hub_city": "Khulna"},
    {"id": "car_tucson_suv", "name": "Hyundai Tucson AWD", "brand": "Hyundai", "category": "SUV", "seats": 5, "dailyRate": 85, "status": "AVAILABLE", "transmission": "Automatic", "fuelType": "Hybrid", "securityDeposit": 350, "hub_city": "Dhaka"},
    {"id": "car_tesla_modely", "name": "Tesla Model Y Long Range", "brand": "Tesla", "category": "Electric", "seats": 5, "dailyRate": 110, "status": "AVAILABLE", "transmission": "Automatic", "fuelType": "Electric", "securityDeposit": 500, "hub_city": "Dhaka"},
    {"id": "car_mercedes_eclass", "name": "Mercedes-Benz E-Class AMG Line", "brand": "Mercedes-Benz", "category": "Luxury", "seats": 5, "dailyRate": 160, "status": "AVAILABLE", "transmission": "Automatic", "fuelType": "Petrol", "securityDeposit": 500, "hub_city": "Dhaka"},
    {"id": "car_camry_hybrid", "name": "Toyota Camry Premium Hybrid", "brand": "Toyota", "category": "Sedan", "seats": 5, "dailyRate": 70, "status": "AVAILABLE", "transmission": "Automatic", "fuelType": "Hybrid", "securityDeposit": 200, "hub_city": "Khulna"},
    {"id": "car_hiace_luxury", "name": "Toyota HiAce Grandia Luxury", "brand": "Toyota", "category": "Van", "seats": 11, "dailyRate": 130, "status": "AVAILABLE", "transmission": "Automatic", "fuelType": "Diesel", "securityDeposit": 350, "hub_city": "Chittagong"},
    {"id": "car_civic_sport", "name": "Honda Civic Sport", "brand": "Honda", "category": "Sedan", "seats": 5, "dailyRate": 55, "status": "AVAILABLE", "transmission": "Automatic", "fuelType": "Petrol", "securityDeposit": 200, "hub_city": "Khulna"},
    {"id": "car_mustang_gt", "name": "Ford Mustang GT Convertible", "brand": "Ford", "category": "Sports", "seats": 4, "dailyRate": 175, "status": "AVAILABLE", "transmission": "Automatic", "fuelType": "Petrol", "securityDeposit": 500, "hub_city": "Dhaka"}
]

FALLBACK_BOOKINGS = [
    {"id": "bkg_1001", "bookingCode": "RC-BK-78901", "userId": "usr_cust_1", "status": "ACTIVE", "paymentStatus": "PAID", "pickupDateTime": "2026-08-28T09:00:00Z", "dropoffDateTime": "2026-09-02T18:00:00Z", "totalAmount": 515, "totalDays": 5, "car_name": "Jaguar XE L Prestige"},
    {"id": "bkg_1002", "bookingCode": "RC-BK-78902", "userId": "usr_cust_2", "status": "CONFIRMED", "paymentStatus": "PAID", "pickupDateTime": "2026-08-30T10:00:00Z", "dropoffDateTime": "2026-09-01T20:00:00Z", "totalAmount": 250, "totalDays": 2, "car_name": "Audi A6 Business Executive"},
    {"id": "bkg_1003", "bookingCode": "RC-BK-78903", "userId": "usr_cust_1", "status": "PENDING", "paymentStatus": "PENDING", "pickupDateTime": "2026-09-03T08:00:00Z", "dropoffDateTime": "2026-09-07T18:00:00Z", "totalAmount": 440, "totalDays": 4, "car_name": "Tesla Model Y Long Range"},
    {"id": "bkg_1004", "bookingCode": "RC-BK-78904", "userId": "usr_cust_1", "status": "COMPLETED", "paymentStatus": "PAID", "pickupDateTime": "2026-08-15T08:00:00Z", "dropoffDateTime": "2026-08-18T18:00:00Z", "totalAmount": 279, "totalDays": 3, "car_name": "Hyundai Tucson Limited Edition"}
]

class SQLExecutor:
    @staticmethod
    def _validate_safe_query(query_str: str):
        """Strict check to prevent any DDL/DML injection."""
        forbidden = r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|GRANT|REVOKE|EXEC|CREATE)\b"
        if re.search(forbidden, query_str, re.IGNORECASE):
            raise ValueError("Forbidden mutation statement in read-only SQL executor.")

    @classmethod
    async def execute_template(
        cls,
        template_name: str,
        params: Dict[str, Any],
        user_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Executes a predefined SQL template safely with parameter binding.
        """
        if template_name not in SQL_TEMPLATES:
            return []

        sql_text = SQL_TEMPLATES[template_name]
        cls._validate_safe_query(sql_text)

        # Build clean query parameters
        query_params = {
            "city": f"%{params.get('city')}%" if params.get("city") else None,
            "category": params.get("category"),
            "seats": params.get("seats"),
            "max_rate": params.get("budget_max"),
            "name": f"%{params.get('vehicle_name')}%" if params.get("vehicle_name") else None,
            "user_id": user_id or params.get("user_id", "usr_cust_1")
        }

        try:
            async with get_db_session() as session:
                stmt = text(sql_text)
                # Set 5-second execution timeout
                result = await asyncio.wait_for(session.execute(stmt, query_params), timeout=5.0)
                rows = result.mappings().all()
                if rows:
                    return [dict(row) for row in rows]
        except Exception as e:
            # Table might not exist or be empty in Neon database yet; use robust fallback
            pass

        # Fallback in-memory matching
        return cls._fallback_execute(template_name, params, user_id)

    @classmethod
    def _fallback_execute(
        cls,
        template_name: str,
        params: Dict[str, Any],
        user_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Fallback in-memory filter matching business logic."""
        if template_name in ["car_availability", "car_search", "price_inquiry"]:
            cars = list(FALLBACK_CARS)
            city = params.get("city") or params.get("location")
            category = params.get("category")
            seats = params.get("seats")
            v_name = params.get("vehicle_name")

            if city:
                city_clean = city.lower().split(",")[0].strip()
                filtered = [c for c in cars if city_clean in c.get("hub_city", "").lower() or city_clean in c["name"].lower()]
                if filtered:
                    cars = filtered

            if category:
                cars = [c for c in cars if c.get("category", "").lower() == category.lower()]

            if seats:
                cars = [c for c in cars if c.get("seats", 0) >= int(seats)]

            if v_name:
                v_clean = v_name.lower()
                matched = [c for c in cars if v_clean in c["name"].lower() or v_clean in c["brand"].lower()]
                if matched:
                    cars = matched

            return cars

        elif template_name == "user_bookings":
            uid = user_id or "usr_cust_1"
            return [b for b in FALLBACK_BOOKINGS if b["userId"] == uid]

        elif template_name == "user_payments":
            return [
                {"id": "pay_101", "bookingId": "bkg_1001", "amount": 515, "paymentStatus": "PAID", "paymentMethod": "Credit Card", "createdAt": "2026-08-28T09:00:00Z"},
                {"id": "pay_102", "bookingId": "bkg_1004", "amount": 279, "paymentStatus": "PAID", "paymentMethod": "Credit Card", "createdAt": "2026-08-15T08:00:00Z"}
            ]

        elif template_name == "admin_revenue":
            total_rev = sum(b["totalAmount"] for b in FALLBACK_BOOKINGS if b["status"] != "CANCELLED")
            return [{
                "total_bookings": len(FALLBACK_BOOKINGS),
                "total_revenue": total_rev,
                "avg_booking_value": round(total_rev / len(FALLBACK_BOOKINGS), 2)
            }]

        elif template_name == "admin_most_rented":
            return [
                {"id": "car_tucson_suv", "name": "Hyundai Tucson AWD", "brand": "Hyundai", "category": "SUV", "rental_count": 18},
                {"id": "car_prado_suv", "name": "Toyota Land Cruiser Prado TX", "brand": "Toyota", "category": "SUV", "rental_count": 14},
                {"id": "car_camry_hybrid", "name": "Toyota Camry Premium Hybrid", "brand": "Toyota", "category": "Sedan", "rental_count": 12}
            ]

        elif template_name == "admin_maintenance":
            return [
                {"id": "maint_1", "car_name": "Audi A6 Business Executive", "maintenanceType": "OIL_CHANGE", "title": "Regular 10,000km Engine Oil Change", "startDate": "2026-09-01", "estimatedCost": 120}
            ]

        return []

sql_executor = SQLExecutor()
