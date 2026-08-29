"""
Database Seed and Initial Ingestion Loader.
Seeds PostgreSQL with the enterprise knowledge base if tables are empty, and generates initial embeddings.
"""
from typing import List, Dict, Any
from sqlalchemy import select
from app.core.database import get_db_session
from app.core.models import KnowledgeDocument, get_utc_now
from app.indexing.canonical_builder import CanonicalBuilder
from app.indexing.change_detector import ChangeDetector
from app.indexing.chunker import chunker
from app.indexing.embedding_service import get_batch_embeddings
from app.indexing.index_updater import IndexUpdater

INITIAL_KNOWLEDGE_DOCS: List[Dict[str, Any]] = [
    # Vehicles
    {
        "id": "fleet_prado_suv",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Toyota Land Cruiser Prado TX (4x4 Luxury SUV)",
        "content": (
            "Model: Toyota Land Cruiser Prado TX (4x4 Luxury SUV). Daily Rate: $145/day. "
            "Capacity: 7 Passengers, 4 Large Suitcases. Transmission: 6-speed Automatic. "
            "Terrain Capability: Heavy Off-Road, Mountainous Terrain (Sylhet, Bandarban, Sajek, Hilly Roads), 4WD with Differential Lock. "
            "Engine & Fuel: 2.8L Turbo Diesel (12 km/L). "
            "Key Features: Dual AC, Ground Clearance 220mm, Rooftop Rack Ready, Child Seat ISOFIX, Hill Descent Control, GPS Navigation. "
            "Best For: Family mountain expeditions, off-road adventures, multi-day wilderness trips."
        ),
        "tags": ["suv", "4x4", "mountain", "off-road", "7-seater", "luxury", "prado", "diesel", "family", "large group"],
        "metadata": {
            "dailyRate": 145, "seats": 7, "category": "SUV", "transmission": "Automatic", "fuelType": "Diesel",
            "terrain": "Mountain / 4WD Off-Road"
        }
    },
    {
        "id": "fleet_tucson_suv",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Hyundai Tucson AWD (Compact Modern SUV)",
        "content": (
            "Model: Hyundai Tucson AWD (Compact SUV). Daily Rate: $85/day. "
            "Capacity: 5 Passengers, 3 Suitcases. Transmission: 8-speed Automatic. "
            "Terrain Capability: All-Wheel Drive (AWD), Highway, Light Gravel, Rainy/Wet Conditions. "
            "Engine & Fuel: 2.0L Smartstream Petrol/Hybrid (15 km/L). "
            "Key Features: Panoramic Sunroof, Apple CarPlay/Android Auto, Lane Keep Assist, Emergency Braking, Spacious Legroom. "
            "Best For: Medium family road trips, weekend getaways, comfortable highway cruising."
        ),
        "tags": ["suv", "awd", "family", "5-seater", "budget-suv", "tucson", "hybrid", "vacation"],
        "metadata": {
            "dailyRate": 85, "seats": 5, "category": "SUV", "transmission": "Automatic", "fuelType": "Hybrid",
            "terrain": "Highway / Light Gravel"
        }
    },
    {
        "id": "fleet_tesla_modely",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Tesla Model Y Long Range (Electric SUV)",
        "content": (
            "Model: Tesla Model Y Long Range (All-Electric SUV). Daily Rate: $110/day. "
            "Capacity: 5 Passengers, 3 Large Suitcases + Front Trunk (Frunk). Transmission: Single-Speed Direct Drive. "
            "Terrain Capability: City, Expressways, Paved Highways with Supercharger Support. Range: 510 km on full charge. "
            "Key Features: Autopilot, 15-inch Touchscreen, Premium Audio, Zero Emissions, Ultra-Quiet Ride, Supercharging Access. "
            "Best For: Eco-conscious travelers, tech enthusiasts, premium city commute, scenic highway tours."
        ),
        "tags": ["electric", "ev", "tesla", "eco", "modern", "luxury", "5-seater", "fast"],
        "metadata": {
            "dailyRate": 110, "seats": 5, "category": "Electric", "transmission": "Automatic", "fuelType": "Electric",
            "terrain": "Highway / City"
        }
    },
    {
        "id": "fleet_mercedes_eclass",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Mercedes-Benz E-Class AMG Line (Executive Luxury Sedan)",
        "content": (
            "Model: Mercedes-Benz E-Class AMG Line. Daily Rate: $160/day. "
            "Capacity: 5 Passengers, 2 Large Suitcases. Transmission: 9G-TRONIC Automatic. "
            "Terrain Capability: Paved City & Expressways. Luxury Smooth Suspension. "
            "Engine & Fuel: 2.0L Turbocharged Mild-Hybrid Petrol (14 km/L). "
            "Key Features: Nappa Leather Seats, Burmester 3D Surround Sound, Ambient Lighting 64 colors, Chauffeur Package, Executive Tint. "
            "Best For: Corporate VIP business meetings, weddings, airport VIP pickups, luxury executive travel."
        ),
        "tags": ["luxury", "sedan", "mercedes", "executive", "corporate", "vip", "wedding", "business"],
        "metadata": {
            "dailyRate": 160, "seats": 5, "category": "Luxury", "transmission": "Automatic", "fuelType": "Hybrid",
            "terrain": "City / Expressways"
        }
    },
    {
        "id": "fleet_camry_hybrid",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Toyota Camry Premium Hybrid (Full-Size Sedan)",
        "content": (
            "Model: Toyota Camry Premium Hybrid. Daily Rate: $70/day. "
            "Capacity: 5 Passengers, 3 Suitcases. Transmission: e-CVT Automatic. "
            "Terrain Capability: City Streets, Highways, Inter-District Roads. "
            "Engine & Fuel: 2.5L Dynamic Force Hybrid (22 km/L Exceptional Fuel Economy). "
            "Key Features: Whisper Quiet Cabin, Wireless Phone Charging, Blind Spot Monitor, Rear Sunshade, Ventilated Seats. "
            "Best For: Long-distance budget-conscious comfort, business trips, couple or family city road trips."
        ),
        "tags": ["sedan", "hybrid", "fuel-efficient", "camry", "toyota", "economy", "5-seater", "comfortable"],
        "metadata": {
            "dailyRate": 70, "seats": 5, "category": "Sedan", "transmission": "Automatic", "fuelType": "Hybrid",
            "terrain": "City / Highway"
        }
    },
    {
        "id": "fleet_hiace_luxury",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Toyota HiAce Grandia Luxury (Executive Passenger Van)",
        "content": (
            "Model: Toyota HiAce Grandia Luxury. Daily Rate: $130/day. "
            "Capacity: 11 Passengers, 8 Large Suitcases. Transmission: 6-speed Automatic. "
            "Terrain Capability: Highway, Interstate, Paved Rural & Tourist Spots. "
            "Engine & Fuel: 2.8L Turbo Diesel (11 km/L). "
            "Key Features: Reclining Captain Seats, High Roof Comfort, Dual Overhead AC Vents for all rows, Microphone PA system, USB chargers per seat. "
            "Best For: Large group corporate tours, family reunions, wedding guest transportation, tourist group excursions."
        ),
        "tags": ["van", "11-seater", "large group", "family", "hiace", "corporate", "luggage", "tour"],
        "metadata": {
            "dailyRate": 130, "seats": 11, "category": "Van", "transmission": "Automatic", "fuelType": "Diesel",
            "terrain": "Highway / Tour Routes"
        }
    },
    {
        "id": "fleet_civic_sport",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Honda Civic Sport (Compact Stylish Sedan)",
        "content": (
            "Model: Honda Civic Sport. Daily Rate: $55/day. "
            "Capacity: 5 Passengers, 2 Suitcases. Transmission: CVT with Paddle Shifters. "
            "Terrain Capability: City, Suburban, Highway. "
            "Engine & Fuel: 1.5L VTEC Turbo (16 km/L). "
            "Key Features: Sport Alloy Wheels, Digital Cockpit, Honda Sensing Safety Suite, Apple CarPlay, Compact Parking Ease. "
            "Best For: Solo travelers, young couples, agile city driving, affordable daily rental."
        ),
        "tags": ["budget", "compact", "sedan", "civic", "honda", "sport", "city", "affordable"],
        "metadata": {
            "dailyRate": 55, "seats": 5, "category": "Sedan", "transmission": "Automatic", "fuelType": "Petrol",
            "terrain": "City / Highway"
        }
    },
    {
        "id": "fleet_mustang_gt",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Ford Mustang GT V8 Convertible (Sports Car)",
        "content": (
            "Model: Ford Mustang GT Convertible. Daily Rate: $175/day. "
            "Capacity: 4 Passengers, 2 Small Bags. Transmission: 10-speed SelectShift Automatic. "
            "Terrain Capability: Coastal Roads, Highway Cruising, Scenic Drives. "
            "Engine: 5.0L Ti-VCT V8 (450 HP). "
            "Key Features: Power Soft-Top Convertible, Active Valve Performance Exhaust, Brembo Brakes, Track Apps, Heated & Cooled Leather Seats. "
            "Best For: Honeymoons, photo shoots, coastal scenic drives, sports car enthusiasts."
        ),
        "tags": ["sports", "convertible", "mustang", "luxury", "v8", "fast", "couple", "photoshoot"],
        "metadata": {
            "dailyRate": 175, "seats": 4, "category": "Sports", "transmission": "Automatic", "fuelType": "Petrol",
            "terrain": "Coastal / Highway"
        }
    },

    # Policies
    {
        "id": "policy_age_license",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Driver Eligibility & License Requirements",
        "content": (
            "Driver Requirements: Primary driver must be at least 21 years old for standard/economy vehicles (Sedans, Compact SUVs). "
            "For Luxury, Executive (Mercedes E-Class) and Sports categories (Mustang GT), minimum age is 25 years old. "
            "Documentation: A valid domestic driver's license held for at least 1 year is required. "
            "International travelers must present an International Driving Permit (IDP) along with their national passport. "
            "Additional Drivers: Up to 2 additional drivers can be added for a flat $10/day fee (free under VIP Full Shield package)."
        ),
        "tags": ["policy", "age", "license", "driver", "international", "eligibility", "documents", "idp"],
        "metadata": {"minAgeStandard": 21, "minAgeLuxury": 25, "idpRequired": True}
    },
    {
        "id": "policy_deposit_refund",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Security Deposit & Refund Timelines",
        "content": (
            "Security Deposit: A refundable pre-authorization deposit is required at vehicle pickup ($200 for Standard/Economy, $350 for SUVs/Vans, $500 for Luxury/Sports). "
            "Deposit Release: The pre-authorization hold is immediately released upon vehicle check-in following vehicle return inspection (typically reflects within 24 to 48 hours depending on the customer's bank). "
            "Accepted Payment Methods: Visa, MasterCard, American Express, Digital Bank Transfer, and major mobile wallets. "
            "Cancellation & Refund Policy: Free cancellation with 100% full refund if cancelled up to 24 hours prior to the scheduled pickup time. "
            "Late cancellations (<24h) incur a single day rental charge."
        ),
        "tags": ["policy", "deposit", "refund", "cancellation", "payment", "security deposit", "credit card", "money"],
        "metadata": {"depositStandard": 200, "depositSUV": 350, "depositLuxury": 500, "freeCancellationHours": 24}
    },
    {
        "id": "policy_mileage_fuel",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Mileage Allowance & Fuel Guidelines",
        "content": (
            "Mileage Allowance: All bookings of 3 days or longer include 100% Unlimited Mileage across the entire country. "
            "For short 1-day or 2-day rentals, an allowance of 250 km/day is included, with excess mileage billed at $0.25/km. "
            "Fuel Policy: Full-to-Full protocol. The vehicle is delivered with a 100% full tank and must be returned with a full tank. "
            "If returned less than full, refueling is charged at standard pump price plus a $10 refueling convenience service fee. "
            "Electric Vehicles (Tesla): Delivered with 80%+ battery and can be returned at 20%+ battery without recharge penalty if booked under Eco-Shield."
        ),
        "tags": ["policy", "mileage", "fuel", "unlimited mileage", "gas", "fuel tank", "electric", "charging"],
        "metadata": {"unlimitedMinDays": 3, "dailyAllowanceKm": 250, "fuelPolicy": "Full-to-Full"}
    },
    {
        "id": "policy_insurance_protection",
        "entity_type": "insurance",
        "category": "Insurance & Protection",
        "title": "Protection Packages & Coverage Tiers",
        "content": (
            "Protection Tiers: "
            "1. Basic CDW (Collision Damage Waiver): Included free in base rental price. Covers vehicle damage with a $1,000 deductible / excess. "
            "2. Comprehensive Protection Plus (+$18/day): Reduces excess deductible to $0 (Zero Excess). Includes glass/windshield protection, tire damage, and 24/7 roadside emergency breakdown assistance. "
            "3. VIP Full Shield (+$30/day): Zero excess, zero security deposit required, comprehensive theft protection, personal accident insurance ($100k coverage), plus free guaranteed replacement car dispatch within 2 hours if any mechanical breakdown occurs."
        ),
        "tags": ["insurance", "protection", "cdw", "zero excess", "coverage", "roadside assistance", "accident", "theft"],
        "metadata": {"basicExcess": 1000, "comprehensivePlusDaily": 18, "vipFullShieldDaily": 30}
    },

    # Trip Guides
    {
        "id": "trip_mountain_offroad",
        "entity_type": "trip_guide",
        "category": "Trip Guide",
        "title": "Mountainous & Hilly Road Recommendations (Sylhet, Bandarban, Sajek)",
        "content": (
            "Recommended Vehicles for Hilly & Rough Terrain: "
            "When traveling to hill tracts, tea gardens, or off-road scenic spots (e.g. Sajek Valley, Bandarban Hill Tracts, Jaflong, Sreemangal), "
            "we strictly recommend the Toyota Land Cruiser Prado TX (4WD) or Hyundai Tucson (AWD). "
            "Standard sedans have low ground clearance and risk undercarriage damage on steep inclinations and rocky trails. "
            "The Prado TX provides 220mm ground clearance, low-range 4WD traction, and Hill Descent Control for maximum safety."
        ),
        "tags": ["trip", "mountain", "hills", "sajek", "bandarban", "sylhet", "off-road", "prado", "4wd", "tucson"],
        "metadata": {"destinations": ["Sajek", "Bandarban", "Sylhet"], "recommendedVehicles": ["fleet_prado_suv", "fleet_tucson_suv"]}
    },
    {
        "id": "trip_corporate_executive",
        "entity_type": "trip_guide",
        "category": "Trip Guide",
        "title": "Corporate Executive & VIP Travel Guidance",
        "content": (
            "Recommendations for Business Delegates & VIP Events: "
            "For executive travel, diplomatic visits, high-profile corporate roadshows, and airport transfers, "
            "the Mercedes-Benz E-Class AMG Line or Toyota Camry Hybrid are top choices. "
            "Chauffeur Service: Available upon request with professional English-speaking drivers trained in VIP protocol (+$35/day)."
        ),
        "tags": ["trip", "corporate", "executive", "business", "vip", "chauffeur", "mercedes", "camry"],
        "metadata": {"recommendedVehicles": ["fleet_mercedes_eclass", "fleet_camry_hybrid"]}
    },
    {
        "id": "trip_family_large_group",
        "entity_type": "trip_guide",
        "category": "Trip Guide",
        "title": "Large Family & Group Excursion Guidance",
        "content": (
            "Recommendations for 6 to 11 Travelers: "
            "For large families or tour groups exceeding 5 passengers with multiple large suitcases, "
            "the Toyota HiAce Grandia Luxury (11-seater) or Toyota Prado TX (7-seater) are ideal. "
            "The HiAce Grandia features individual captain seats, overhead AC blowers, and high ceiling clearance for effortless long-distance travel."
        ),
        "tags": ["trip", "family", "group", "hiace", "prado", "large family", "7-seater", "11-seater", "luggage"],
        "metadata": {"minPassengers": 6, "recommendedVehicles": ["fleet_hiace_luxury", "fleet_prado_suv"]}
    }
]

async def seed_knowledge_base_if_empty():
    """
    Seeds database with initial canonical documents and pre-computes their embeddings.
    """
    async with get_db_session() as session:
        result = await session.execute(select(KnowledgeDocument))
        existing_docs = result.scalars().all()
        
        if existing_docs:
            print(f"[Seed] PostgreSQL knowledge base already contains {len(existing_docs)} documents.")
            return

        print(f"[Seed] Initializing PostgreSQL knowledge base with {len(INITIAL_KNOWLEDGE_DOCS)} canonical documents...")
        
        for doc_data in INITIAL_KNOWLEDGE_DOCS:
            canonical = CanonicalBuilder.build(doc_data["entity_type"], doc_data)
            content_hash = ChangeDetector.compute_hash(canonical)
            
            doc = KnowledgeDocument(
                id=doc_data["id"],
                entity_type=doc_data.get("entity_type", "general"),
                entity_id=doc_data.get("id"),
                category=doc_data.get("category", "General"),
                title=doc_data.get("title", ""),
                content=doc_data.get("content", ""),
                canonical_text=canonical,
                tags=doc_data.get("tags", []),
                metadata_json=doc_data.get("metadata", {}),
                content_hash=content_hash,
                is_active=True,
                created_at=get_utc_now()
            )
            session.add(doc)
            await session.commit()

            # Pre-compute initial embeddings
            chunks = chunker.chunk_text(canonical)
            chunk_texts = [c["chunk_text"] for c in chunks]
            embeddings = await get_batch_embeddings(chunk_texts)
            
            await IndexUpdater.index_document_chunks(
                session=session,
                document_id=doc.id,
                chunks_data=chunks,
                embeddings=embeddings
            )

        print("[Seed] Successfully seeded and pre-computed embeddings in PostgreSQL.")
