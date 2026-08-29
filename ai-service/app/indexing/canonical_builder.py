"""
Canonical Document Representation Builder.
Transforms raw database entities (Vehicles, Policies, FAQs, Locations) into standardized,
high-density semantic text representations for chunking and embedding.
"""
from typing import Dict, Any, List

class CanonicalBuilder:
    @staticmethod
    def build_vehicle_canonical(v: Dict[str, Any]) -> str:
        features_str = ", ".join(v.get("features", [])) if isinstance(v.get("features"), list) else str(v.get("features", ""))
        specs = v.get("specs", {})
        engine = specs.get("engine", "") if isinstance(specs, dict) else ""
        hp = specs.get("horsepower", "") if isinstance(specs, dict) else ""
        
        return (
            f"Vehicle: {v.get('brand', '')} {v.get('name', '')}\n"
            f"Category: {v.get('category', '')}\n"
            f"Daily Rental Rate: ${v.get('dailyRate', 0)}/day\n"
            f"Seating Capacity: {v.get('seats', 4)} passengers, {v.get('luggageCapacity', 2)} luggage capacity\n"
            f"Transmission: {v.get('transmission', 'Automatic')}\n"
            f"Fuel Type: {v.get('fuelType', 'Petrol')} ({v.get('fuelEfficiency', 'Standard')})\n"
            f"Terrain & Road Capability: {v.get('terrainCapability', 'Paved roads')}\n"
            f"Key Equipment & Features: {features_str}\n"
            f"Technical Specifications: Engine {engine}, {hp} HP\n"
            f"Current Availability: {'Available for immediate rental' if v.get('available', True) else 'Currently rented / unavailable'}"
        )

    @staticmethod
    def build_policy_canonical(p: Dict[str, Any]) -> str:
        return (
            f"Rental Policy: {p.get('title', '')}\n"
            f"Category: {p.get('category', 'Rental Policy')}\n"
            f"Policy Details & Rules:\n{p.get('content', '')}\n"
            f"Tags & Applicable Clauses: {', '.join(p.get('tags', []))}"
        )

    @staticmethod
    def build_trip_guide_canonical(t: Dict[str, Any]) -> str:
        return (
            f"Travel Destination Guide: {t.get('title', '')}\n"
            f"Category: {t.get('category', 'Trip Guide')}\n"
            f"Recommendations & Road Profile:\n{t.get('content', '')}\n"
            f"Key Search Tags: {', '.join(t.get('tags', []))}"
        )

    @classmethod
    def build(cls, entity_type: str, data: Dict[str, Any]) -> str:
        if entity_type == "vehicle":
            return cls.build_vehicle_canonical(data)
        elif entity_type == "policy" or entity_type == "insurance":
            return cls.build_policy_canonical(data)
        elif entity_type == "trip_guide":
            return cls.build_trip_guide_canonical(data)
        else:
            title = data.get("title", "")
            category = data.get("category", "General")
            content = data.get("content", "")
            tags = ", ".join(data.get("tags", [])) if isinstance(data.get("tags"), list) else ""
            return f"Title: {title}\nCategory: {category}\nContent: {content}\nTags: {tags}"
