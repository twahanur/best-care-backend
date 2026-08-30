from typing import Dict, Any, Optional
from app.query.language_detector import language_detector
from app.query.entity_extractor import entity_extractor
from app.query.intent_classifier import intent_classifier

class QueryPlan:
    def __init__(
        self,
        query: str,
        language: str,
        intent: str,
        query_type: str,
        entities: Dict[str, Any],
        requires_sql: bool = False,
        requires_vector: bool = False,
        requires_booking_action: bool = False,
        sql_template_name: Optional[str] = None
    ):
        self.query = query
        self.language = language
        self.intent = intent
        self.query_type = query_type
        self.entities = entities
        self.requires_sql = requires_sql
        self.requires_vector = requires_vector
        self.requires_booking_action = requires_booking_action
        self.sql_template_name = sql_template_name

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "language": self.language,
            "intent": self.intent,
            "query_type": self.query_type,
            "entities": self.entities,
            "requires_sql": self.requires_sql,
            "requires_vector": self.requires_vector,
            "requires_booking_action": self.requires_booking_action,
            "sql_template_name": self.sql_template_name
        }

class QueryPlanner:
    @staticmethod
    def plan(
        query: str,
        booking_state: Optional[Dict[str, Any]] = None,
        user_role: str = "CUSTOMER"
    ) -> QueryPlan:
        """
        Analyzes the query and generates an execution plan.
        """
        language = language_detector.detect(query)
        entities = entity_extractor.extract(query)
        intent = intent_classifier.classify(query, booking_state=booking_state, user_role=user_role)

        # 1. Booking Action Flow
        if intent in ["booking_create", "booking_confirm", "booking_cancel_request"]:
            return QueryPlan(
                query=query,
                language=language,
                intent=intent,
                query_type="booking_action",
                entities=entities,
                requires_sql=True,
                requires_vector=False,
                requires_booking_action=True,
                sql_template_name="car_availability"
            )

        # 2. Structured SQL Path (Dynamic Live Tables)
        structured_intents = {
            "car_availability": "car_availability",
            "car_search": "car_search",
            "price_inquiry": "price_inquiry",
            "booking_lookup": "user_bookings",
            "payment_status": "user_payments",
            "admin_revenue": "admin_revenue",
            "admin_most_rented": "admin_most_rented",
            "admin_maintenance": "admin_maintenance"
        }

        if intent in structured_intents:
            return QueryPlan(
                query=query,
                language=language,
                intent=intent,
                query_type="structured",
                entities=entities,
                requires_sql=True,
                requires_vector=False,
                sql_template_name=structured_intents[intent]
            )

        # 3. Hybrid Path (Structured SQL + Vector Descriptions)
        if intent in ["car_recommendation", "trip_recommendation"]:
            return QueryPlan(
                query=query,
                language=language,
                intent=intent,
                query_type="hybrid",
                entities=entities,
                requires_sql=True,
                requires_vector=True,
                sql_template_name="car_availability"
            )

        # 4. Pure Semantic Vector Path (Knowledge Documents, Policies, FAQ)
        if intent in ["policy_inquiry", "insurance_inquiry", "general_faq"]:
            return QueryPlan(
                query=query,
                language=language,
                intent=intent,
                query_type="semantic",
                entities=entities,
                requires_sql=False,
                requires_vector=True
            )

        # 5. Conversational Path (Greetings, Thanks)
        return QueryPlan(
            query=query,
            language=language,
            intent=intent,
            query_type="conversational",
            entities=entities,
            requires_sql=False,
            requires_vector=False
        )

query_planner = QueryPlanner()
