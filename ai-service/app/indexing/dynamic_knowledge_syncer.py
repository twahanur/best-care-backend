import hashlib
import uuid
from typing import List, Dict, Any
from sqlalchemy import select, text
from app.core.database import get_db_session
from app.core.models import KnowledgeDocument, KnowledgeChunk, KnowledgeEmbedding, get_utc_now
from app.indexing.embedding_service import get_embedding

# Standard baseline policy documents (dynamic guidelines)
CORE_POLICIES = [
    {
        "id": "policy_deposit_refund",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Security Deposit & Refund Timelines",
        "content": (
            "Security Deposit: A refundable pre-authorization deposit is required at vehicle pickup ($150-$200 for Standard/Sedan, $300-$350 for SUVs/Vans, $400-$600 for Luxury/Sports). "
            "Deposit Release: The pre-authorization hold is immediately released upon vehicle check-in following vehicle return inspection (typically reflects within 24 to 48 hours). "
            "Payment Methods: Visa, MasterCard, American Express, Digital Bank Transfer, and major mobile wallets. "
            "Cancellation & Refund Policy: Free cancellation with 100% full refund if cancelled up to 24 hours prior to the scheduled pickup time. "
            "Late cancellations (<24h) incur a single day rental charge."
        ),
        "tags": ["policy", "deposit", "refund", "cancellation", "payment", "security deposit", "money"]
    },
    {
        "id": "policy_insurance_protection",
        "entity_type": "policy",
        "category": "Insurance & Protection",
        "title": "Protection Packages & Coverage Tiers",
        "content": (
            "Protection Tiers: "
            "1. Basic CDW (Collision Damage Waiver): Included free in base rental price. Covers vehicle damage with a $1,000 deductible / excess. "
            "2. Comprehensive Protection Plus (+$18/day): Reduces excess deductible to $0 (Zero Excess). Includes glass/windshield protection, tire damage, and 24/7 roadside emergency breakdown assistance. "
            "3. VIP Full Shield (+$30/day): Zero excess, zero security deposit required, comprehensive theft protection, personal accident insurance ($100k coverage), plus free guaranteed replacement car dispatch within 2 hours if any mechanical breakdown occurs."
        ),
        "tags": ["insurance", "protection", "cdw", "zero excess", "coverage", "roadside assistance", "accident", "theft"]
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
            "Electric Vehicles: Delivered with 80%+ battery and can be returned at 20%+ battery without recharge penalty."
        ),
        "tags": ["policy", "mileage", "fuel", "unlimited mileage", "gas", "electric", "charging"]
    },
    {
        "id": "policy_age_license",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Driver Eligibility & License Requirements",
        "content": (
            "Driver Requirements: Primary driver must be at least 21 years old for standard vehicles. "
            "For Luxury and Sports categories, minimum age is 25 years old. "
            "Documentation: A valid domestic driver's license held for at least 1 year is required. "
            "International travelers must present an International Driving Permit (IDP) along with passport. "
            "Chauffeur Service: Available with professional English-speaking drivers for all vehicles (+$35/day)."
        ),
        "tags": ["policy", "age", "license", "driver", "international", "eligibility", "documents", "idp"]
    },
    {
        "id": "trip_mountain_offroad",
        "entity_type": "trip_guide",
        "category": "Trip Guide",
        "title": "Mountainous & Hilly Road Recommendations (Sylhet, Bandarban, Sajek)",
        "content": (
            "When traveling to hill tracts, tea gardens, or off-road scenic spots (e.g. Sajek Valley, Bandarban Hill Tracts, Jaflong, Sreemangal), "
            "we strictly recommend 4WD or AWD SUVs (like Toyota Land Cruiser Prado TX or Hyundai Tucson AWD). "
            "Standard sedans have low ground clearance and risk undercarriage damage on steep inclinations. "
            "4WD vehicles provide high ground clearance (220mm) and hill descent traction for maximum safety."
        ),
        "tags": ["trip", "mountain", "hills", "sajek", "bandarban", "sylhet", "off-road", "4wd", "suv"]
    }
]

class DynamicKnowledgeSyncer:
    @classmethod
    async def sync_all(cls) -> int:
        """
        Dynamically extracts cars, hubs, and pricing rules from PostgreSQL,
        generates high-density canonical documents, and syncs vector embeddings.
        """
        docs_to_index: List[Dict[str, Any]] = []

        # 1. Dynamically Load Fleet Cars from PostgreSQL 'cars' table
        try:
            async with get_db_session() as session:
                sql_cars = """
                    SELECT c.id, c.name, c.brand, c.model, c.year, CAST(c.category AS text) as category,
                           CAST(c.transmission AS text) as transmission, CAST(c."fuelType" AS text) as "fuelType",
                           c.seats, c.doors, c."luggageCapacity", c."dailyRate", c."securityDeposit",
                           CAST(c.status AS text) as status, c."ratingAverage", c."isFeatured",
                           lh.name as hub_name, lh.city as hub_city
                    FROM cars c
                    LEFT JOIN location_hubs lh ON c."currentHubId" = lh.id
                    WHERE CAST(c.status AS text) != 'DECOMMISSIONED';
                """
                res = await session.execute(text(sql_cars))
                cars_rows = res.mappings().all()

                for row in cars_rows:
                    car_doc_id = f"doc_{row['id']}"
                    brand_name = f"{row.get('brand', '')} {row.get('name', '')}".strip()
                    cat = str(row.get('category', 'SEDAN')).upper()
                    rate = row.get('dailyRate', 0)
                    seats = row.get('seats', 5)
                    fuel = row.get('fuelType', 'PETROL')
                    trans = row.get('transmission', 'AUTOMATIC')
                    deposit = row.get('securityDeposit', 200)
                    hub_city = row.get('hub_city') or 'Dhaka'
                    status = row.get('status', 'AVAILABLE')

                    content = (
                        f"Model: {brand_name} ({row.get('year', 2024)}). Category: {cat}. "
                        f"Daily Rental Rate: ${rate}/day. Security Deposit: ${deposit}. "
                        f"Seating Capacity: {seats} Passengers, {row.get('luggageCapacity', 3)} Suitcases. "
                        f"Transmission: {trans}. Fuel Type: {fuel}. "
                        f"Current Hub Location: {hub_city} ({row.get('hub_name', 'Main Hub')}). "
                        f"Current Availability Status: {status}. Rating: {row.get('ratingAverage', 5.0)}/5.0."
                    )

                    tags = [
                        cat.lower(),
                        row.get('brand', '').lower(),
                        row.get('name', '').lower(),
                        hub_city.lower(),
                        fuel.lower(),
                        f"{seats}-seater",
                        "available" if status == "AVAILABLE" else "rented"
                    ]

                    docs_to_index.append({
                        "id": car_doc_id,
                        "entity_type": "vehicle",
                        "entity_id": row["id"],
                        "category": "Fleet Specs",
                        "title": f"{brand_name} ({cat})",
                        "content": content,
                        "tags": tags
                    })

        except Exception as e:
            print(f"[DynamicSyncer] Notice reading live cars table: {e}")

        # 2. Add baseline policy documents
        for p in CORE_POLICIES:
            docs_to_index.append(p)

        # 3. Store into knowledge_documents & knowledge_embeddings
        if not docs_to_index:
            return 0

        async with get_db_session() as session:
            for d in docs_to_index:
                canonical = f"{d['title']}\nCategory: {d['category']}\n{d['content']}\nTags: {', '.join(d.get('tags', []))}"
                content_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

                # Check if exists and up-to-date
                stmt = select(KnowledgeDocument).where(KnowledgeDocument.id == d["id"])
                existing = (await session.execute(stmt)).scalar_one_or_none()

                if existing and existing.content_hash == content_hash:
                    continue

                if existing:
                    existing.title = d["title"]
                    existing.category = d["category"]
                    existing.content = d["content"]
                    existing.canonical_text = canonical
                    existing.tags = d.get("tags", [])
                    existing.content_hash = content_hash
                    existing.updated_at = get_utc_now()
                else:
                    new_doc = KnowledgeDocument(
                        id=d["id"],
                        entity_type=d.get("entity_type", "general"),
                        entity_id=d.get("entity_id", d["id"]),
                        category=d["category"],
                        title=d["title"],
                        content=d["content"],
                        canonical_text=canonical,
                        tags=d.get("tags", []),
                        metadata_json={},
                        content_hash=content_hash,
                        is_active=True,
                        created_at=get_utc_now()
                    )
                    session.add(new_doc)

                # Chunk & Vectorize
                chunk_id = f"chk_{d['id']}_{uuid.uuid4().hex[:6]}"
                chunk = KnowledgeChunk(
                    id=chunk_id,
                    document_id=d["id"],
                    chunk_index=0,
                    chunk_text=canonical,
                    token_count=len(canonical.split()),
                    created_at=get_utc_now()
                )
                session.add(chunk)

                emb_vec = await get_embedding(canonical)
                embedding = KnowledgeEmbedding(
                    id=f"emb_{d['id']}_{uuid.uuid4().hex[:6]}",
                    document_id=d["id"],
                    chunk_id=chunk_id,
                    embedding_vector=emb_vec,
                    status="ACTIVE",
                    embedded_at=get_utc_now()
                )
                session.add(embedding)

            await session.commit()

        print(f"[DynamicSyncer] Successfully synced {len(docs_to_index)} dynamic knowledge documents to pgvector.")
        return len(docs_to_index)

dynamic_knowledge_syncer = DynamicKnowledgeSyncer()
