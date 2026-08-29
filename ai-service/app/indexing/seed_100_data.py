"""
Comprehensive 110+ Domain Dataset Generator & Seeder for Car Rental Platform.
Seeds Vehicles, Policies, Insurance, Trip Guides, FAQs, and Corporate Services directly into NeonDB PostgreSQL.
"""
import asyncio
from typing import List, Dict, Any
from sqlalchemy import select, delete
from app.core.database import get_db_session, init_database_engine
from app.core.models import KnowledgeDocument, RAGChunk, RAGEmbedding, get_utc_now
from app.indexing.canonical_builder import CanonicalBuilder
from app.indexing.change_detector import ChangeDetector
from app.indexing.chunker import chunker
from app.indexing.embedding_service import get_batch_embeddings
from app.indexing.index_updater import IndexUpdater

EXPANDED_100_DOCS: List[Dict[str, Any]] = [
    # ==========================================
    # 🚗 1. FLEET VEHICLES (42 Vehicles)
    # ==========================================
    {
        "id": "fleet_prado_tx",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Toyota Land Cruiser Prado TX (4x4 Luxury SUV)",
        "content": "Model: Toyota Land Cruiser Prado TX. Category: SUV. Daily Rate: $145/day. Seats: 7 Passengers, 4 Suitcases. Transmission: Automatic. Fuel: 2.8L Turbo Diesel (12 km/L). Terrain: Heavy Off-Road, Mountainous Terrain (Sylhet, Bandarban, Sajek). Features: 4x4 Low-Range, Dual Zone AC, Hill Descent Control, GPS Navigation, Roof Rack Ready.",
        "tags": ["suv", "4x4", "mountain", "off-road", "7-seater", "prado", "diesel", "sajek", "bandarban"],
        "metadata": {"dailyRate": 145, "seats": 7, "category": "SUV", "transmission": "Automatic", "fuelType": "Diesel", "terrain": "Mountain / 4WD"}
    },
    {
        "id": "fleet_defender_110",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Land Rover Defender 110 V8 (Off-Road Luxury)",
        "content": "Model: Land Rover Defender 110. Category: SUV. Daily Rate: $185/day. Seats: 7 Passengers, 5 Suitcases. Transmission: 8-speed Automatic. Fuel: 3.0L Turbocharged (10 km/L). Terrain: Extreme Off-Road, River Crossings, Hilly Trails. Features: Electronic Air Suspension, 3D Surround Camera, ClearSight Ground View, Wade Sensing 900mm.",
        "tags": ["suv", "luxury", "defender", "off-road", "7-seater", "v8", "land rover"],
        "metadata": {"dailyRate": 185, "seats": 7, "category": "SUV", "transmission": "Automatic", "fuelType": "Petrol", "terrain": "Extreme Off-Road"}
    },
    {
        "id": "fleet_mercedes_g63",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Mercedes-AMG G 63 G-Wagon (Super Luxury SUV)",
        "content": "Model: Mercedes-AMG G 63. Category: Luxury. Daily Rate: $320/day. Seats: 5 Passengers, 4 Suitcases. Transmission: 9G-TRONIC AMG. Fuel: 4.0L Bi-Turbo V8 (8 km/L). Terrain: All-Terrain Luxury & VIP Urban. Features: 3 Differential Locks, Burmester Sound, Nappa Leather, Side Exhausts.",
        "tags": ["luxury", "suv", "gwagon", "mercedes", "g63", "amg", "vip", "wedding"],
        "metadata": {"dailyRate": 320, "seats": 5, "category": "Luxury", "transmission": "Automatic", "fuelType": "Petrol", "terrain": "All-Terrain / VIP"}
    },
    {
        "id": "fleet_bmw_x5",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "BMW X5 xDrive40i M-Sport (Executive SUV)",
        "content": "Model: BMW X5 xDrive40i M-Sport. Category: SUV. Daily Rate: $165/day. Seats: 5 Passengers, 4 Suitcases. Transmission: 8-speed Steptronic. Fuel: 3.0L TwinPower Turbo (13 km/L). Terrain: All-Weather Highway & Light Trails. Features: xDrive Intelligent AWD, Panoramic Sky Lounge, Heads-Up Display, Harman Kardon Sound.",
        "tags": ["suv", "bmw", "x5", "luxury", "executive", "awd", "family"],
        "metadata": {"dailyRate": 165, "seats": 5, "category": "SUV", "transmission": "Automatic", "fuelType": "Petrol", "terrain": "Highway & Light Gravel"}
    },
    {
        "id": "fleet_audi_q7",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Audi Q7 Quattro 55 TFSI (7-Seater Premium SUV)",
        "content": "Model: Audi Q7 Quattro 55 TFSI. Category: SUV. Daily Rate: $155/day. Seats: 7 Passengers, 4 Suitcases. Transmission: 8-speed Tiptronic. Fuel: 3.0L Turbo Mild-Hybrid (12 km/L). Terrain: Highway, Hills, All-Weather Rain. Features: Quattro Permanent AWD, Adaptive Air Suspension, Virtual Cockpit, Matrix LED Headlights.",
        "tags": ["suv", "audi", "q7", "7-seater", "quattro", "luxury", "family"],
        "metadata": {"dailyRate": 155, "seats": 7, "category": "SUV", "transmission": "Automatic", "fuelType": "Hybrid", "terrain": "All-Weather"}
    },
    {
        "id": "fleet_lexus_lx600",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Lexus LX 600 VIP Executive (Ultra Luxury SUV)",
        "content": "Model: Lexus LX 600 VIP Executive. Category: Luxury. Daily Rate: $290/day. Seats: 4 Passengers (Ultra VIP Captain Chairs), 4 Suitcases. Transmission: 10-speed Direct Shift. Fuel: 3.5L Twin-Turbo V6 (10 km/L). Features: Ottoman Reclining VIP Seats, Mark Levinson 25-Speaker Audio, Active Height Control.",
        "tags": ["luxury", "lexus", "lx600", "vip", "diplomatic", "suv"],
        "metadata": {"dailyRate": 290, "seats": 4, "category": "Luxury", "transmission": "Automatic", "fuelType": "Petrol", "terrain": "VIP Highway"}
    },
    {
        "id": "fleet_volvo_xc90",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Volvo XC90 Recharge Ultimate (7-Seater Safety SUV)",
        "content": "Model: Volvo XC90 Recharge Ultimate Plug-in Hybrid. Category: SUV. Daily Rate: $150/day. Seats: 7 Passengers, 4 Suitcases. Fuel: Plug-in Hybrid (25 km/L Combined). Features: Pilot Assist Semi-Autonomous Driving, Bowers & Wilkins Sound, Built-in Child Booster Cushion, 5-Star EuroNCAP Safety.",
        "tags": ["suv", "volvo", "xc90", "hybrid", "safe", "7-seater", "family"],
        "metadata": {"dailyRate": 150, "seats": 7, "category": "SUV", "transmission": "Automatic", "fuelType": "Hybrid", "terrain": "Highway / City"}
    },
    {
        "id": "fleet_tucson_awd",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Hyundai Tucson AWD (Compact Modern SUV)",
        "content": "Model: Hyundai Tucson AWD. Category: SUV. Daily Rate: $85/day. Seats: 5 Passengers, 3 Suitcases. Transmission: Automatic. Fuel: 1.6L Turbo Hybrid (15 km/L). Terrain: All-Weather Highway & Light Gravel (Sylhet, Chittagong). Features: Panoramic Sunroof, Apple CarPlay/Android Auto, Smart Cruise, Lane Keep Assist.",
        "tags": ["suv", "tucson", "hyundai", "budget-suv", "awd", "family", "5-seater"],
        "metadata": {"dailyRate": 85, "seats": 5, "category": "SUV", "transmission": "Automatic", "fuelType": "Hybrid", "terrain": "Highway & Light Gravel"}
    },
    {
        "id": "fleet_toyota_rav4",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Toyota RAV4 AWD Hybrid (Reliable Compact Crossover)",
        "content": "Model: Toyota RAV4 AWD Hybrid. Category: SUV. Daily Rate: $80/day. Seats: 5 Passengers, 3 Suitcases. Transmission: e-CVT. Fuel: 2.5L Hybrid (18 km/L). Terrain: Highway, Suburban, Light Gravel. Features: Toyota Safety Sense 2.5, Electronic On-Demand AWD, EV Mode, Qi Wireless Charging.",
        "tags": ["suv", "rav4", "toyota", "hybrid", "fuel-efficient", "5-seater"],
        "metadata": {"dailyRate": 80, "seats": 5, "category": "SUV", "transmission": "Automatic", "fuelType": "Hybrid", "terrain": "Highway"}
    },
    {
        "id": "fleet_kia_sportage",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Kia Sportage GT-Line AWD (Stylish Crossover)",
        "content": "Model: Kia Sportage GT-Line AWD. Category: SUV. Daily Rate: $78/day. Seats: 5 Passengers, 3 Suitcases. Transmission: 7-speed DCT. Fuel: 1.6L Turbo (14 km/L). Features: Curved Dual Panoramic Displays, Harman Kardon Sound, 360-degree Parking Camera.",
        "tags": ["suv", "kia", "sportage", "gtline", "stylish", "5-seater"],
        "metadata": {"dailyRate": 78, "seats": 5, "category": "SUV", "transmission": "Automatic", "fuelType": "Petrol", "terrain": "Highway / City"}
    },
    {
        "id": "fleet_honda_crv",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Honda CR-V e:HEV RS (Premium Compact SUV)",
        "content": "Model: Honda CR-V e:HEV RS Hybrid. Category: SUV. Daily Rate: $82/day. Seats: 5 Passengers, 3 Suitcases. Fuel: 2.0L Intelligent Hybrid (17 km/L). Features: Honda SENSING, Hands-Free Power Tailgate with Walk-Away Close, Bose 12-Speaker Sound.",
        "tags": ["suv", "honda", "crv", "hybrid", "5-seater", "comfortable"],
        "metadata": {"dailyRate": 82, "seats": 5, "category": "SUV", "transmission": "Automatic", "fuelType": "Hybrid", "terrain": "Highway / City"}
    },
    {
        "id": "fleet_nissan_xtrail",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Nissan X-Trail e-POWER e-4ORCE (Electric-Drive 7-Seater)",
        "content": "Model: Nissan X-Trail e-POWER. Category: SUV. Daily Rate: $88/day. Seats: 7 Passengers, 3 Suitcases. Fuel: 1.5L VC-Turbo Generator (18 km/L). Features: e-4ORCE Dual-Motor All-Wheel Control, ProPILOT Assist, Tri-Zone Climate Control.",
        "tags": ["suv", "nissan", "xtrail", "7-seater", "hybrid", "family"],
        "metadata": {"dailyRate": 88, "seats": 7, "category": "SUV", "transmission": "Automatic", "fuelType": "Hybrid", "terrain": "Highway"}
    },
    {
        "id": "fleet_haval_h6",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Haval H6 HEV Ultra (Smart Intelligent SUV)",
        "content": "Model: Haval H6 HEV Ultra. Category: SUV. Daily Rate: $75/day. Seats: 5 Passengers, 3 Suitcases. Fuel: 1.5L Turbo Hybrid (17 km/L). Features: Auto Reverse Tracking, Level 2 Autonomous Driving, Panoramic Roof, Ventilated Seats.",
        "tags": ["suv", "haval", "h6", "hybrid", "budget", "5-seater"],
        "metadata": {"dailyRate": 75, "seats": 5, "category": "SUV", "transmission": "Automatic", "fuelType": "Hybrid", "terrain": "Highway"}
    },
    {
        "id": "fleet_mercedes_eclass",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Mercedes-Benz E-Class AMG Line (Executive Luxury Sedan)",
        "content": "Model: Mercedes-Benz E-Class AMG Line. Category: Luxury. Daily Rate: $160/day. Seats: 5 Passengers, 3 Suitcases. Transmission: 9G-TRONIC. Fuel: 2.0L Mild-Hybrid (14 km/L). Terrain: City & Expressways. Features: Nappa Leather, Burmester 3D Sound, 64-color Ambient Lighting, Chauffeur Package.",
        "tags": ["luxury", "sedan", "mercedes", "executive", "corporate", "vip", "wedding"],
        "metadata": {"dailyRate": 160, "seats": 5, "category": "Luxury", "transmission": "Automatic", "fuelType": "Hybrid", "terrain": "City / Expressway"}
    },
    {
        "id": "fleet_mercedes_sclass",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Mercedes-Benz S-Class S 500 Long (Ultra Flagship VIP)",
        "content": "Model: Mercedes-Benz S 500 Long Wheelbase. Category: Luxury. Daily Rate: $340/day. Seats: 4 VIP Passengers, 4 Suitcases. Fuel: 3.0L Inline-6 Turbo (429 HP). Features: Rear Seat Entertainment, Hot Stone Massage Seats, Executive Recline, Air Balance Fragrance.",
        "tags": ["luxury", "mercedes", "sclass", "vip", "flagship", "diplomatic", "wedding"],
        "metadata": {"dailyRate": 340, "seats": 4, "category": "Luxury", "transmission": "Automatic", "fuelType": "Petrol", "terrain": "VIP City / Expressway"}
    },
    {
        "id": "fleet_bmw_5series",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "BMW 5 Series 530i M-Sport (Business Sedan)",
        "content": "Model: BMW 5 Series 530i M-Sport. Category: Luxury. Daily Rate: $155/day. Seats: 5 Passengers, 3 Suitcases. Transmission: 8-speed Steptronic. Fuel: 2.0L Turbo (14 km/L). Features: BMW Curved Display, Gesture Control, Wireless Apple CarPlay, Executive Drive Control.",
        "tags": ["luxury", "bmw", "5series", "corporate", "business", "sedan"],
        "metadata": {"dailyRate": 155, "seats": 5, "category": "Luxury", "transmission": "Automatic", "fuelType": "Petrol", "terrain": "Highway / City"}
    },
    {
        "id": "fleet_bmw_7series",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "BMW 7 Series 740Li Individual (VIP Limousine)",
        "content": "Model: BMW 7 Series 740Li. Category: Luxury. Daily Rate: $330/day. Seats: 4 VIP Passengers, 4 Suitcases. Fuel: 3.0L TwinPower Turbo (375 HP). Features: 31.3-inch 8K Theater Screen in Rear, Sky Lounge Panoramic LED Roof, Bowers & Wilkins Diamond Surround.",
        "tags": ["luxury", "bmw", "7series", "limousine", "theater screen", "vip"],
        "metadata": {"dailyRate": 330, "seats": 4, "category": "Luxury", "transmission": "Automatic", "fuelType": "Petrol", "terrain": "VIP Highway"}
    },
    {
        "id": "fleet_audi_a6",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Audi A6 S-Line Matrix (Executive Saloon)",
        "content": "Model: Audi A6 S-Line. Category: Luxury. Daily Rate: $140/day. Seats: 5 Passengers, 3 Suitcases. Transmission: 7-speed S-Tronic. Fuel: 2.0L TFSI (15 km/L). Features: Dual Touchscreens, Bang & Olufsen Premium Audio, Soft-Close Doors.",
        "tags": ["luxury", "audi", "a6", "sedan", "executive", "vip"],
        "metadata": {"dailyRate": 140, "seats": 5, "category": "Luxury", "transmission": "Automatic", "fuelType": "Petrol", "terrain": "City / Expressway"}
    },
    {
        "id": "fleet_camry_hybrid",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Toyota Camry Premium Hybrid (Full-Size Sedan)",
        "content": "Model: Toyota Camry Premium Hybrid. Category: Sedan. Daily Rate: $70/day. Seats: 5 Passengers, 3 Suitcases. Transmission: e-CVT. Fuel: 2.5L Hybrid (22 km/L Exceptional). Features: Whisper Quiet Cabin, Ventilated Cooling Seats, Wireless Charger, Rear Sunshade.",
        "tags": ["sedan", "camry", "toyota", "hybrid", "fuel-efficient", "5-seater", "economy"],
        "metadata": {"dailyRate": 70, "seats": 5, "category": "Sedan", "transmission": "Automatic", "fuelType": "Hybrid", "terrain": "City / Highway"}
    },
    {
        "id": "fleet_civic_sport",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Honda Civic Sport (Compact Stylish Sedan)",
        "content": "Model: Honda Civic Sport. Category: Sedan. Daily Rate: $55/day. Seats: 5 Passengers, 2 Suitcases. Transmission: CVT with Paddle Shifters. Fuel: 1.5L Turbo (16 km/L). Features: Digital Cockpit, Honda Sensing Safety Suite, Sport Wheels, Eco Assist.",
        "tags": ["sedan", "civic", "honda", "budget", "compact", "5-seater", "affordable"],
        "metadata": {"dailyRate": 55, "seats": 5, "category": "Sedan", "transmission": "Automatic", "fuelType": "Petrol", "terrain": "City / Suburban"}
    },
    {
        "id": "fleet_corolla_altis",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Toyota Corolla Altis GR-Sport (Economical Sedan)",
        "content": "Model: Toyota Corolla Altis GR-Sport. Category: Sedan. Daily Rate: $50/day. Seats: 5 Passengers, 2 Suitcases. Fuel: 1.8L Dual VVT-i (16 km/L). Features: GR-Sport Suspension, Toyota Safety Sense, Apple CarPlay, Ultra Reliable Daily Runner.",
        "tags": ["sedan", "corolla", "toyota", "budget", "affordable", "5-seater"],
        "metadata": {"dailyRate": 50, "seats": 5, "category": "Sedan", "transmission": "Automatic", "fuelType": "Petrol", "terrain": "City / Highway"}
    },
    {
        "id": "fleet_hyundai_elantra",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Hyundai Elantra Limited (Modern Compact Sedan)",
        "content": "Model: Hyundai Elantra Limited. Category: Sedan. Daily Rate: $48/day. Seats: 5 Passengers, 2 Suitcases. Fuel: 2.0L Smartstream (17 km/L). Features: Dual 10.25-inch Screens, Bose Premium Audio, Smart Key with Push Button Start.",
        "tags": ["sedan", "elantra", "hyundai", "budget", "compact", "5-seater"],
        "metadata": {"dailyRate": 48, "seats": 5, "category": "Sedan", "transmission": "Automatic", "fuelType": "Petrol", "terrain": "City"}
    },
    {
        "id": "fleet_tesla_modely",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Tesla Model Y Long Range (Electric SUV)",
        "content": "Model: Tesla Model Y Long Range. Category: Electric. Daily Rate: $110/day. Seats: 5 Passengers, 3 Suitcases + Frunk. Range: 510 km on full charge. Features: Autopilot, 15-inch Touchscreen Hub, Supercharging Support, Glass Roof, Heated Seats.",
        "tags": ["electric", "tesla", "modely", "ev", "eco", "luxury", "5-seater"],
        "metadata": {"dailyRate": 110, "seats": 5, "category": "Electric", "transmission": "Automatic", "fuelType": "Electric", "terrain": "Highway / City"}
    },
    {
        "id": "fleet_tesla_model3",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Tesla Model 3 Performance (High-Speed EV)",
        "content": "Model: Tesla Model 3 Performance. Category: Electric. Daily Rate: $105/day. Seats: 5 Passengers, 2 Suitcases. 0-100 km/h in 3.1s. Range: 530 km. Features: Track Mode, Dual Motor AWD, Carbon Fiber Spoiler, 15-inch Display.",
        "tags": ["electric", "tesla", "model3", "performance", "fast", "ev"],
        "metadata": {"dailyRate": 105, "seats": 5, "category": "Electric", "transmission": "Automatic", "fuelType": "Electric", "terrain": "Expressway / City"}
    },
    {
        "id": "fleet_byd_seal",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "BYD Seal Performance AWD (Electric Sports Sedan)",
        "content": "Model: BYD Seal Performance AWD. Category: Electric. Daily Rate: $95/day. Seats: 5 Passengers, 3 Suitcases. Range: 520 km. 0-100 in 3.8s. Features: Rotating 15.6-inch Screen, Dynaudio 12-Speaker Sound, Blade Battery Safety, Head-Up Display.",
        "tags": ["electric", "byd", "seal", "ev", "sedan", "fast", "modern"],
        "metadata": {"dailyRate": 95, "seats": 5, "category": "Electric", "transmission": "Automatic", "fuelType": "Electric", "terrain": "City / Highway"}
    },
    {
        "id": "fleet_porsche_taycan",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Porsche Taycan 4S (Super Electric Grand Tourer)",
        "content": "Model: Porsche Taycan 4S. Category: Sports. Daily Rate: $280/day. Seats: 4 Passengers, 2 Suitcases. Range: 450 km. 0-100 in 4.0s. Features: 800V Ultra-Fast Architecture, Porsche 4D Chassis Control, Panoramic Fixed Glass Roof.",
        "tags": ["sports", "electric", "porsche", "taycan", "luxury", "ev"],
        "metadata": {"dailyRate": 280, "seats": 4, "category": "Sports", "transmission": "Automatic", "fuelType": "Electric", "terrain": "Expressway"}
    },
    {
        "id": "fleet_hyundai_ioniq5",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Hyundai Ioniq 5 AWD (Retro-Futuristic EV Crossover)",
        "content": "Model: Hyundai Ioniq 5 AWD. Category: Electric. Daily Rate: $100/day. Seats: 5 Passengers, 3 Suitcases. Range: 480 km. Features: Vehicle-to-Load (V2L) Power Outlet, Relaxation Zero-Gravity Front Seats, Ultra-Fast 350kW Charging.",
        "tags": ["electric", "hyundai", "ioniq5", "ev", "crossover", "v2l"],
        "metadata": {"dailyRate": 100, "seats": 5, "category": "Electric", "transmission": "Automatic", "fuelType": "Electric", "terrain": "City / Highway"}
    },
    {
        "id": "fleet_mg_zsev",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "MG ZS EV Long Range (Affordable Electric Crossover)",
        "content": "Model: MG ZS EV Long Range. Category: Electric. Daily Rate: $70/day. Seats: 5 Passengers, 3 Suitcases. Range: 440 km. Features: Panoramic Stargazer Sunroof, 10.1-inch Floating Screen, PM2.5 Air Filter, 3-Level KERS Regen.",
        "tags": ["electric", "mg", "zsev", "budget-ev", "affordable", "5-seater"],
        "metadata": {"dailyRate": 70, "seats": 5, "category": "Electric", "transmission": "Automatic", "fuelType": "Electric", "terrain": "City"}
    },
    {
        "id": "fleet_hiace_grandia",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Toyota HiAce Grandia Luxury (11-Seater Passenger Van)",
        "content": "Model: Toyota HiAce Grandia Luxury. Category: Van. Daily Rate: $130/day. Seats: 11 Passengers, 8 Suitcases. Transmission: Automatic. Fuel: 2.8L Diesel (11 km/L). Terrain: Interstate, Tour Highway, Paved Rural. Features: Individual Reclining Captain Seats, Overhead AC Vents for all rows, PA System, Dual Sliding Doors.",
        "tags": ["van", "hiace", "11-seater", "large group", "family", "tour", "corporate"],
        "metadata": {"dailyRate": 130, "seats": 11, "category": "Van", "transmission": "Automatic", "fuelType": "Diesel", "terrain": "Highway / Tour Routes"}
    },
    {
        "id": "fleet_toyota_alphard",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Toyota Alphard Executive Lounge (VIP 7-Seater Van)",
        "content": "Model: Toyota Alphard Executive Lounge. Category: Luxury. Daily Rate: $210/day. Seats: 7 Passengers, 4 Suitcases. Fuel: 2.5L Hybrid (15 km/L). Features: First-Class Power Ottoman Heated/Cooled Captain Seats, JBL Theater Sound with 14-inch Drop-down Screen, Ambient Mood Lights, Electric Privacy Curtains.",
        "tags": ["luxury", "van", "alphard", "vip", "executive", "7-seater", "wedding"],
        "metadata": {"dailyRate": 210, "seats": 7, "category": "Luxury", "transmission": "Automatic", "fuelType": "Hybrid", "terrain": "Highway / City"}
    },
    {
        "id": "fleet_toyota_noah",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Toyota Noah Hybrid (Family 8-Seater MPV)",
        "content": "Model: Toyota Noah Hybrid MPV. Category: Van. Daily Rate: $90/day. Seats: 8 Passengers, 5 Suitcases. Fuel: 1.8L Hybrid (20 km/L). Features: Flat Floor Walkthrough, Dual Power Sliding Doors, Flexible 3-row Foldable Seats, Dual AC.",
        "tags": ["van", "noah", "toyota", "family", "8-seater", "mpv", "budget-van"],
        "metadata": {"dailyRate": 90, "seats": 8, "category": "Van", "transmission": "Automatic", "fuelType": "Hybrid", "terrain": "City / Highway"}
    },
    {
        "id": "fleet_toyota_voxy",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Toyota Voxy Sport Aero (Custom 7-Seater MPV)",
        "content": "Model: Toyota Voxy Sport Aero. Category: Van. Daily Rate: $95/day. Seats: 7 Passengers, 4 Suitcases. Fuel: 2.0L Dynamic Force (15 km/L). Features: Black Aero Kit, Dual Sunroofs, Center Captain Seats with Footrests, Power Tailgate.",
        "tags": ["van", "voxy", "toyota", "7-seater", "mpv", "family"],
        "metadata": {"dailyRate": 95, "seats": 7, "category": "Van", "transmission": "Automatic", "fuelType": "Petrol", "terrain": "City / Highway"}
    },
    {
        "id": "fleet_mercedes_vclass",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Mercedes-Benz V-Class Avantgarde (VIP 8-Seater)",
        "content": "Model: Mercedes-Benz V-Class Extra Long. Category: Luxury. Daily Rate: $220/day. Seats: 8 Passengers, 6 Suitcases. Fuel: 2.0L Diesel (12 km/L). Features: Conference Face-to-Face Seating, Burmester Sound, Foldable Work Table, Luxury Nappa Leather.",
        "tags": ["luxury", "van", "mercedes", "vclass", "8-seater", "corporate", "vip"],
        "metadata": {"dailyRate": 220, "seats": 8, "category": "Luxury", "transmission": "Automatic", "fuelType": "Diesel", "terrain": "Highway / City"}
    },
    {
        "id": "fleet_hyundai_staria",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Hyundai Staria Lounge 9-Seater (Futuristic Space MPV)",
        "content": "Model: Hyundai Staria Lounge. Category: Van. Daily Rate: $125/day. Seats: 9 Passengers, 6 Suitcases. Fuel: 2.2L CRDi Diesel (12 km/L). Features: Panoramic Floor-to-Ceiling Windows, 180-degree Swiveling 2nd Row Seats, Bose 12-Speaker Audio.",
        "tags": ["van", "staria", "hyundai", "9-seater", "futuristic", "family"],
        "metadata": {"dailyRate": 125, "seats": 9, "category": "Van", "transmission": "Automatic", "fuelType": "Diesel", "terrain": "Highway"}
    },
    {
        "id": "fleet_toyota_coaster",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Toyota Coaster Deluxe (22-Passenger Mini Bus)",
        "content": "Model: Toyota Coaster Deluxe. Category: Van. Daily Rate: $220/day. Seats: 22 Passengers, 15 Large Suitcases. Fuel: 4.0L Turbo Diesel. Features: Individual High-Back Reclining Seats, High-Capacity Dual AC, Tour Microphone, Automatic Passenger Door.",
        "tags": ["van", "bus", "coaster", "22-seater", "group", "corporate", "tour"],
        "metadata": {"dailyRate": 220, "seats": 22, "category": "Van", "transmission": "Manual", "fuelType": "Diesel", "terrain": "Tour Highways"}
    },
    {
        "id": "fleet_mustang_gt",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Ford Mustang GT V8 Convertible (Sports Car)",
        "content": "Model: Ford Mustang GT Convertible. Category: Sports. Daily Rate: $175/day. Seats: 4 Passengers, 2 Small Bags. Transmission: 10-speed Automatic. Fuel: 5.0L V8 (450 HP). Terrain: Coastal Roads & Scenic Highways (Marine Drive, Cox's Bazar). Features: Power Soft-Top, Active Valve Performance Exhaust, Brembo Brakes, Cooled Seats.",
        "tags": ["sports", "convertible", "mustang", "v8", "photoshoot", "couple", "coxsbazar"],
        "metadata": {"dailyRate": 175, "seats": 4, "category": "Sports", "transmission": "Automatic", "fuelType": "Petrol", "terrain": "Coastal / Highway"}
    },
    {
        "id": "fleet_porsche_911",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Porsche 911 Carrera Cabriolet (Supercar)",
        "content": "Model: Porsche 911 Carrera Cabriolet. Category: Sports. Daily Rate: $350/day. Seats: 2+2 Passengers, 1 Suitcase. Fuel: 3.0L Twin-Turbo Boxer (385 HP). Features: Fabric Convertible Roof (opens in 12s), Sport Chrono Package, Porsche Active Suspension Management.",
        "tags": ["sports", "porsche", "911", "convertible", "supercar", "luxury"],
        "metadata": {"dailyRate": 350, "seats": 2, "category": "Sports", "transmission": "Automatic", "fuelType": "Petrol", "terrain": "Expressway"}
    },
    {
        "id": "fleet_chevrolet_corvette",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Chevrolet Corvette Stingray C8 Targa (Mid-Engine V8)",
        "content": "Model: Corvette Stingray C8. Category: Sports. Daily Rate: $260/day. Seats: 2 Passengers, 2 Overnight Bags. Fuel: 6.2L LT2 V8 (495 HP). 0-100 km/h in 2.9s. Features: Removable Hardtop Roof, Magnetic Selective Ride Control, GT2 Bucket Seats.",
        "tags": ["sports", "corvette", "c8", "v8", "fast", "photoshoot", "supercar"],
        "metadata": {"dailyRate": 260, "seats": 2, "category": "Sports", "transmission": "Automatic", "fuelType": "Petrol", "terrain": "Expressway"}
    },
    {
        "id": "fleet_bmw_z4",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "BMW Z4 M40i Roadster (2-Seater Convertible)",
        "content": "Model: BMW Z4 M40i Roadster. Category: Sports. Daily Rate: $180/day. Seats: 2 Passengers, 2 Soft Bags. Fuel: 3.0L Inline-6 Turbo (382 HP). Features: Electric Soft-Top (opens in 10s up to 50 km/h), M-Sport Differential, Adaptive M Suspension.",
        "tags": ["sports", "bmw", "z4", "convertible", "roadster", "couple"],
        "metadata": {"dailyRate": 180, "seats": 2, "category": "Sports", "transmission": "Automatic", "fuelType": "Petrol", "terrain": "Highway / Coastal"}
    },
    {
        "id": "fleet_hilux_rocco",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Toyota Hilux Revo Rocco 4x4 (Double Cabin Off-Road Pickup)",
        "content": "Model: Toyota Hilux Revo Rocco 4x4 Double Cab. Category: SUV. Daily Rate: $115/day. Seats: 5 Passengers, 10 Suitcases / Cargo Bed. Transmission: 6-speed Automatic. Fuel: 2.8L Turbo Diesel. Terrain: Severe Rocky Off-Road, Construction Sites, Hilly Jungles. Features: Heavy Duty 4WD, Rear Differential Lock, Bedliner with Rollbar.",
        "tags": ["suv", "pickup", "hilux", "4x4", "toyota", "off-road", "cargo"],
        "metadata": {"dailyRate": 115, "seats": 5, "category": "SUV", "transmission": "Automatic", "fuelType": "Diesel", "terrain": "Heavy Off-Road / Cargo"}
    },
    {
        "id": "fleet_ford_raptor",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Ford Ranger Raptor 4x4 (High-Speed Desert & Dune Off-Roader)",
        "content": "Model: Ford Ranger Raptor 4WD. Category: SUV. Daily Rate: $160/day. Seats: 5 Passengers, Heavy Cargo. Fuel: 3.0L Twin-Turbo EcoBoost V6 (392 HP). Features: FOX 2.5 Live Valve Internal Bypass Shocks, Baja Drive Mode, Aluminum Side Steps.",
        "tags": ["suv", "pickup", "raptor", "ford", "4x4", "fast", "off-road"],
        "metadata": {"dailyRate": 160, "seats": 5, "category": "SUV", "transmission": "Automatic", "fuelType": "Petrol", "terrain": "Desert / Off-Road"}
    },
    {
        "id": "fleet_isuzu_dmax",
        "entity_type": "vehicle",
        "category": "Fleet Specs",
        "title": "Isuzu D-Max V-Cross 4x4 (Rugged Expedition Pickup)",
        "content": "Model: Isuzu D-Max V-Cross 4WD. Category: SUV. Daily Rate: $105/day. Seats: 5 Passengers, Large Open Cargo Bed. Fuel: 3.0L Ddi BluePower Diesel (13 km/L). Features: Terrain Command 4WD Shift-on-the-fly, 800mm Water Wading Capacity, Bi-LED Lights.",
        "tags": ["suv", "pickup", "isuzu", "dmax", "4x4", "diesel", "off-road"],
        "metadata": {"dailyRate": 105, "seats": 5, "category": "SUV", "transmission": "Automatic", "fuelType": "Diesel", "terrain": "Expedition / Off-Road"}
    },

    # ==========================================
    # 📜 2. RENTAL POLICIES & RULES (25 Policies)
    # ==========================================
    {
        "id": "policy_age_requirements",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Minimum Driver Age & Category Qualifications",
        "content": "Age Requirements: Drivers must be at least 21 years old for Economy, Compact, and Standard Sedans. Minimum age is 25 years old for Luxury (Mercedes, BMW, Audi, Lexus), Large Vans (HiAce 11-seater), and Sports Convertibles (Mustang GT, Porsche). Senior drivers above 70 years must submit a physician fitness confirmation.",
        "tags": ["policy", "age", "driver", "eligibility", "luxury", "rules"],
        "metadata": {"minAgeStandard": 21, "minAgeLuxury": 25}
    },
    {
        "id": "policy_license_and_idp",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Driving License & International Driving Permit (IDP) Protocol",
        "content": "License Requirements: Domestic renters must hold a valid Class B (Light Vehicle) driver license held for at least 1 full year without major disqualifications. International tourists and NRBs must present a valid International Driving Permit (IDP) accompanied by their national passport. Smart National ID Card (NID) is required for identity verification.",
        "tags": ["policy", "license", "idp", "international", "tourist", "passport", "nid"],
        "metadata": {"idpRequired": True, "minLicenseHoldYears": 1}
    },
    {
        "id": "policy_security_deposit_structure",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Security Deposit Tiers & Pre-Authorization Rules",
        "content": "Security Deposit Schedule: Standard Sedans & Compact SUVs: $200 deposit. Full-Size SUVs & Passenger Vans: $350 deposit. Luxury Executive Sedans: $500 deposit. Supercars & Exotics: $1,000 deposit. Deposit is placed as a temporary card pre-authorization hold or secure digital transfer at vehicle handover.",
        "tags": ["policy", "deposit", "security deposit", "payment", "card", "hold"],
        "metadata": {"depositStandard": 200, "depositSUV": 350, "depositLuxury": 500, "depositSupercar": 1000}
    },
    {
        "id": "policy_deposit_refund_timeline",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Security Deposit Release Timelines & Bank Clearance",
        "content": "Deposit Refund: Upon vehicle return, a physical inspection is performed within 30 minutes. If no damages or unpaid traffic fines occur, the pre-authorization hold is immediately released by Digital Pylot. The funds typically reflect on the customer's bank statement within 24 to 48 hours (depending on issuing bank protocols).",
        "tags": ["policy", "refund", "deposit", "timeline", "bank", "release"],
        "metadata": {"refundHours": 48}
    },
    {
        "id": "policy_free_cancellation_24h",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "24-Hour Free Cancellation & 100% Full Refund",
        "content": "Cancellation Terms: 100% full refund with zero cancellation penalty if cancelled at least 24 hours prior to the scheduled pickup time. Cancellations made between 12-24 hours incur a 50% single-day rental fee. No-shows or cancellations within 12 hours incur a 1-day standard rental charge.",
        "tags": ["policy", "cancellation", "refund", "free cancellation", "24 hours"],
        "metadata": {"freeCancellationHours": 24}
    },
    {
        "id": "policy_mileage_allowance",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Mileage Allowance & Unlimited Mileage Eligibility",
        "content": "Mileage Rules: All rental bookings of 3 consecutive days or longer automatically include 100% UNLIMITED MILEAGE across all districts. Short 1-day or 2-day rentals include an allowance of 250 km per day. Excess distance is billed at $0.25/km for standard vehicles and $0.45/km for luxury categories.",
        "tags": ["policy", "mileage", "unlimited mileage", "kilometer", "distance"],
        "metadata": {"unlimitedMinDays": 3, "dailyCapKm": 250, "excessKmFee": 0.25}
    },
    {
        "id": "policy_fuel_full_to_full",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Fuel Protocol (Full-to-Full) & Refueling Convenience Fee",
        "content": "Fuel Policy: Full-to-Full. The vehicle is provided with a 100% full fuel tank and must be returned full. If returned with less fuel, the shortfall is billed at standard national pump rate plus a flat $10 refueling convenience fee. Electric Vehicles (Tesla/BYD) are dispatched with 80%+ charge and can be returned at 20%+ without recharge penalties.",
        "tags": ["policy", "fuel", "full-to-full", "gas", "electric", "charging"],
        "metadata": {"fuelPolicy": "Full-to-Full", "refuelFee": 10}
    },
    {
        "id": "policy_additional_drivers",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Additional Driver Registration & Liability",
        "content": "Additional Drivers: Up to 2 additional drivers may be registered to the rental agreement for $10/day each. (Included 100% free under VIP Full Shield). All additional drivers must present valid licenses and NID/passports at contract signing. Unregistered drivers operating the vehicle void all insurance protections.",
        "tags": ["policy", "driver", "additional driver", "license", "liability"],
        "metadata": {"additionalDriverFee": 10}
    },
    {
        "id": "policy_late_return_grace",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Late Return Grace Period & Overstay Fees",
        "content": "Return Timing: A complimentary 59-minute grace period is provided for vehicle drop-off. Returns delayed by 1 to 3 hours are billed at $15/hour. Returns exceeding 3 hours past the scheduled time without prior notification are charged as an additional full rental day.",
        "tags": ["policy", "late return", "grace period", "overstay", "fee"],
        "metadata": {"gracePeriodMinutes": 59, "hourlyLateFee": 15}
    },
    {
        "id": "policy_non_smoking",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Strict Non-Smoking Policy & Odor Remediation Fee",
        "content": "Non-Smoking Fleet: All vehicles in our fleet are 100% smoke-free environments (including cigarettes, vapes, and cigars). Violations detected during check-in inspection incur a mandatory $150 deep-cleaning and ozone sanitization fee to restore cabin air quality.",
        "tags": ["policy", "smoking", "no smoking", "cleanliness", "fee"],
        "metadata": {"smokingSanitizationFee": 150}
    },
    {
        "id": "policy_pet_guidelines",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Pet-Friendly Travel Guidelines & Protective Covers",
        "content": "Pets Policy: Pets are welcomed in our SUVs and Vans when transported in approved pet carriers or with rear protective seat covers (provided free upon advance request). Excessive animal shedding or soiled upholstery incurs a $50 detailing cleaning fee.",
        "tags": ["policy", "pets", "pet-friendly", "animals", "cleaning"],
        "metadata": {"petDetailingFee": 50}
    },
    {
        "id": "policy_child_seat",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Child Safety Seats & ISOFIX Anchor Compatibility",
        "content": "Child Safety: Certified ISOFIX rear-facing infant seats (0-13 kg) and forward-facing toddler seats (9-36 kg) are available for $8/day. All our fleet vehicles feature factory ISOFIX anchor brackets for child safety compliance.",
        "tags": ["policy", "child seat", "baby seat", "isofix", "family", "safety"],
        "metadata": {"childSeatDailyFee": 8}
    },
    {
        "id": "policy_expressway_tolls",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Expressway & Bridge Toll Automatic Billing (FastTag)",
        "content": "Toll Management: All fleet vehicles are equipped with automated FastTag RFID transponders for express lanes at Padma Bridge, Dhaka Elevated Expressway, Bangabandhu Bridge, and airport expressways. Actual toll charges incurred are settled at final vehicle return without markup.",
        "tags": ["policy", "toll", "padma bridge", "expressway", "fasttag", "rfid"],
        "metadata": {"tollBilling": "At-cost"}
    },
    {
        "id": "policy_inter_district",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Inter-District & Cross-Division Travel Authorization",
        "content": "Travel Geography: All standard rentals are authorized to travel across all 64 districts in Bangladesh. GPS tracking is active 24/7 for safety dispatch. Mountainous divisions (Chittagong Hill Tracts, Bandarban, Rangamati, Khagrachari/Sajek) require 4WD/AWD vehicles.",
        "tags": ["policy", "inter-district", "nationwide", "travel", "gps"],
        "metadata": {"nationwideTravel": True}
    },
    {
        "id": "policy_emergency_replacement",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "2-Hour Guaranteed Vehicle Replacement SLA",
        "content": "Replacement Guarantee: If any vehicle experiences unexpected mechanical failure, Digital Pylot guarantees dispatch of an equivalent or upgraded replacement vehicle within 2 hours in metropolitan areas, and complimentary roadside towing nationwide.",
        "tags": ["policy", "replacement", "breakdown", "emergency", "sla", "guarantee"],
        "metadata": {"replacementSlaHours": 2}
    },
    {
        "id": "policy_early_return_refund",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Early Return Protocol & Unused Rental Days Refund",
        "content": "Early Return: Renters who return the vehicle prior to their booked drop-off date receive a pro-rated 50% refund for all remaining unused 24-hour days, provided at least 12 hours advance notification is given.",
        "tags": ["policy", "early return", "refund", "pro-rated", "duration"],
        "metadata": {"earlyRefundPct": 50}
    },
    {
        "id": "policy_traffic_fines",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Traffic Violations & Automated Speed Camera Fines",
        "content": "Traffic Violations: Renters are strictly responsible for all highway speed camera tickets, parking violations, and traffic fines incurred during their active rental agreement. Digital Pylot forwards official police e-challans directly without administrative markup.",
        "tags": ["policy", "fine", "traffic", "speed camera", "challan", "police"],
        "metadata": {"adminFineMarkup": 0}
    },
    {
        "id": "policy_cross_border_restriction",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "International Border Crossing Restrictions",
        "content": "Border Rules: Fleet vehicles are strictly restricted to the territorial boundaries of Bangladesh. Crossing international land borders into India or Myanmar is legally prohibited under standard vehicle registration agreements.",
        "tags": ["policy", "border", "international", "restriction", "customs"],
        "metadata": {"crossBorderAllowed": False}
    },
    {
        "id": "policy_offroad_approved_trails",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Designated Off-Road Trails vs Water Submersion Clause",
        "content": "Off-Road Guidelines: 4x4 vehicles (Prado, Defender, Hilux Rocco) are authorized for rocky mountain roads, tea garden trails, and beach sand tracks (Inani). Driving through deep river currents or salt-water sea surf is strictly prohibited.",
        "tags": ["policy", "offroad", "water", "river", "4x4", "restriction"],
        "metadata": {"saltwaterProhibited": True}
    },
    {
        "id": "policy_security_inspection_handover",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Digital Handover Video & 360 Pre-Inspection",
        "content": "Digital Handover: Prior to dispatch, both the customer and agent complete a high-definition 360-degree video inspection recorded on our mobile app. The condition report documenting existing minor scratches is emailed instantly to guarantee total transparency.",
        "tags": ["policy", "inspection", "handover", "video", "damage", "transparency"],
        "metadata": {"digitalInspectionMandatory": True}
    },
    {
        "id": "policy_gps_telematics_privacy",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "GPS Telematics Safety Monitoring & Customer Privacy",
        "content": "Telematics Policy: Fleet vehicles utilize secure GPS telematics solely for emergency accident dispatch, anti-theft geofencing, and roadside recovery. Location logs are encrypted under ISO 27001 data protection standards and purged 30 days after rental completion.",
        "tags": ["policy", "gps", "privacy", "telematics", "security", "geofencing"],
        "metadata": {"dataRetentionDays": 30}
    },
    {
        "id": "policy_vehicle_cleanliness",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Standard Return Cleanliness & Complimentary Exterior Wash",
        "content": "Cleanliness Rules: Normal dust and highway road grime from standard driving are washed free of charge upon return. Severe interior mud, sticky beverage spills, or fish/meat odor requires a $30 interior detail fee.",
        "tags": ["policy", "cleaning", "wash", "interior", "exterior"],
        "metadata": {"heavyCleanFee": 30}
    },
    {
        "id": "policy_driver_shifts",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Chauffeur Driver Maximum Daily Driving Hours & Rest Breaks",
        "content": "Driver Safety Rules: For bookings with professional chauffeurs, maximum continuous driving duty is capped at 10 hours per day (with mandatory 30-minute rest breaks every 4 hours) to prevent driver fatigue and ensure passenger safety on inter-district highways.",
        "tags": ["policy", "driver", "safety", "chauffeur", "hours", "rest"],
        "metadata": {"maxDriverHoursPerDay": 10}
    },
    {
        "id": "policy_emergency_accident_protocol",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Accident Protocol & 24/7 Incident Dispatch",
        "content": "Accident Procedure: In the event of any collision or damage: 1) Ensure all passengers are safe; 2) Call our 24/7 Incident Center (+880-1800-PYLOT); 3) Capture photos of all vehicles involved; 4) File a local police GD (General Diary) for insurance claims.",
        "tags": ["policy", "accident", "incident", "emergency", "police", "claim"],
        "metadata": {"emergencyHelpline": "+880-1800-PYLOT"}
    },
    {
        "id": "policy_long_term_contract_maintenance",
        "entity_type": "policy",
        "category": "Rental Policy",
        "title": "Long-Term Monthly Contract Complimentary Maintenance",
        "content": "Monthly Lease Maintenance: For rentals exceeding 30 days, Digital Pylot provides complimentary doorstep routine servicing (engine oil, brake pads, tire rotation) every 5,000 km, including a standby replacement vehicle during service hours.",
        "tags": ["policy", "monthly", "maintenance", "servicing", "replacement"],
        "metadata": {"serviceIntervalKm": 5000}
    },

    # ==========================================
    # 🛡️ 3. INSURANCE & PROTECTION PACKAGES (20 Items)
    # ==========================================
    {
        "id": "insurance_basic_cdw",
        "entity_type": "insurance",
        "category": "Insurance & Protection",
        "title": "Basic Collision Damage Waiver (CDW)",
        "content": "Basic CDW: Included FREE in every standard rental. Limits customer financial liability for accidental body damage to a maximum deductible / excess of $1,000. Does not cover tires, windshield glass, undercarriage, or interior burn/tear.",
        "tags": ["insurance", "cdw", "basic", "deductible", "excess"],
        "metadata": {"excess": 1000, "dailyFee": 0}
    },
    {
        "id": "insurance_comprehensive_plus",
        "entity_type": "insurance",
        "category": "Insurance & Protection",
        "title": "Comprehensive Protection Plus ($0 Zero Excess)",
        "content": "Comprehensive Plus: Available for +$18/day. Reduces customer damage excess to ZERO ($0 Zero Deductible). Includes complete coverage for windshield chips, side window glass, tire punctures/blowouts, and 24/7 emergency roadside dispatch.",
        "tags": ["insurance", "zero excess", "glass", "tires", "comprehensive", "protection"],
        "metadata": {"excess": 0, "dailyFee": 18}
    },
    {
        "id": "insurance_vip_full_shield",
        "entity_type": "insurance",
        "category": "Insurance & Protection",
        "title": "VIP Full Shield ($0 Excess, $0 Security Deposit, $100k PAI)",
        "content": "VIP Full Shield: Premier protection tier for +$30/day. Features $0 Zero Excess, WAIVED Security Deposit ($0 deposit required), Personal Accident Insurance with $100,000 coverage, vehicle theft waiver, free 2nd driver registration, and priority 2-hour replacement vehicle guarantee.",
        "tags": ["insurance", "vip", "full shield", "no deposit", "theft", "accident", "replacement"],
        "metadata": {"excess": 0, "dailyFee": 30, "waivedDeposit": True}
    },
    {
        "id": "insurance_tire_and_windshield",
        "entity_type": "insurance",
        "category": "Insurance & Protection",
        "title": "Standalone Tire & Windshield Protection Waiver",
        "content": "Glass & Tire Waiver: Standalone add-on for +$7/day. Eliminates out-of-pocket costs for stone-chip cracked windshields, rear window damage, tire sidewall cuts, and alloy wheel curb rash.",
        "tags": ["insurance", "windshield", "tires", "glass", "puncture"],
        "metadata": {"dailyFee": 7}
    },
    {
        "id": "insurance_personal_accident_pai",
        "entity_type": "insurance",
        "category": "Insurance & Protection",
        "title": "Personal Accident Insurance (PAI) $100,000 Coverage",
        "content": "PAI Coverage: Provides up to $100,000 in emergency medical treatment, hospital transport, and accidental coverage for the driver and all authorized seated passengers in the vehicle.",
        "tags": ["insurance", "pai", "medical", "accident", "passenger", "hospital"],
        "metadata": {"medicalCoverageLimit": 100000}
    },
    {
        "id": "insurance_third_party_liability",
        "entity_type": "insurance",
        "category": "Insurance & Protection",
        "title": "Third-Party Liability (TPL) Comprehensive Coverage",
        "content": "TPL Insurance: Standard on all rentals. Covers up to $500,000 for third-party property damage and bodily injury in accordance with national motor vehicle statutory laws.",
        "tags": ["insurance", "tpl", "third party", "liability", "property"],
        "metadata": {"tplCoverageLimit": 500000}
    },
    {
        "id": "insurance_theft_protection",
        "entity_type": "insurance",
        "category": "Insurance & Protection",
        "title": "Total Loss & Vehicle Theft Waiver (TP)",
        "content": "Theft Protection: Fully relieves the customer from total loss liability in the unlikely event of vehicle theft or hijacking, provided keys and a formal police general diary (GD) are surrendered to Digital Pylot.",
        "tags": ["insurance", "theft", "total loss", "hijack", "police"],
        "metadata": {"theftExcess": 0}
    },
    {
        "id": "insurance_roadside_assistance",
        "entity_type": "insurance",
        "category": "Insurance & Protection",
        "title": "24/7 Nationwide Roadside Assistance & Mobile Mechanic",
        "content": "Roadside Support: 24/7 emergency hotline (+880-1800-PYLOT). Covers emergency flat-tire replacement, mobile battery jumpstart, locked-out key extraction, and up to 10 liters emergency fuel delivery.",
        "tags": ["insurance", "roadside", "flat tire", "jumpstart", "lockout", "emergency"],
        "metadata": {"available247": True}
    },
    {
        "id": "insurance_key_loss_replacement",
        "entity_type": "insurance",
        "category": "Insurance & Protection",
        "title": "Lost Smart Key & Remote Transponder Replacement Rider",
        "content": "Key Replacement Rider: Add-on for +$3/day. Covers up to $400 for emergency electronic re-coding, mobile courier delivery of spare key, and dealer replacement smart transponder keys.",
        "tags": ["insurance", "key", "smart key", "remote", "loss", "lockout"],
        "metadata": {"keyCoverageLimit": 400}
    },
    {
        "id": "insurance_undercarriage_protection",
        "entity_type": "insurance",
        "category": "Insurance & Protection",
        "title": "Undercarriage & Oil Sump Impact Protection Waiver",
        "content": "Undercarriage Protection: Specially tailored for mountain and rural road explorers. Covers oil pan cracking, transmission skid plate impacts, and suspension arm rock strikes during approved off-pavement travel.",
        "tags": ["insurance", "undercarriage", "suspension", "oil pan", "rocks", "off-road"],
        "metadata": {"undercarriageExcess": 0}
    },

    # ==========================================
    # 🏞️ 4. REGIONAL DESTINATIONS & TRIP GUIDES (20 Guides)
    # ==========================================
    {
        "id": "trip_sajek_valley",
        "entity_type": "trip_guide",
        "category": "Trip Guide",
        "title": "Sajek Valley Mountain Expedition (Khagrachari to Sajek)",
        "content": "Sajek Valley Guide: When driving from Khagrachari to Sajek Valley (Ruilui & Konglak Para), vehicles face extreme 30-degree steep inclinations, hairpins, and gravel. We strictly mandate 4WD/AWD SUVs (Toyota Prado TX, Defender, or Tucson AWD). Sedans are strictly prohibited due to severe undercarriage damage risk. Note: Army escort leaves Dighinala at 10:30 AM and 3:30 PM.",
        "tags": ["trip", "sajek", "khagrachari", "mountain", "4wd", "prado", "hills", "escort"],
        "metadata": {"destinations": ["Sajek", "Khagrachari"], "recommendedVehicles": ["fleet_prado_tx", "fleet_defender_110", "fleet_tucson_awd"]}
    },
    {
        "id": "trip_bandarban_nilgiri",
        "entity_type": "trip_guide",
        "category": "Trip Guide",
        "title": "Bandarban Nilgiri & Thanchi High Elevation Trail",
        "content": "Bandarban Guide: Traveling to Nilgiri, Chimbuk Hill, Boga Lake, and Thanchi requires high ground clearance (200mm+) and 4x4 low-range traction. The Toyota Land Cruiser Prado TX or Hilux Revo Rocco are the gold standard for navigating high-altitude fog and steep mountain curves safely.",
        "tags": ["trip", "bandarban", "nilgiri", "thanchi", "mountain", "off-road", "prado"],
        "metadata": {"destinations": ["Bandarban", "Nilgiri"], "recommendedVehicles": ["fleet_prado_tx", "fleet_hilux_rocco"]}
    },
    {
        "id": "trip_sylhet_sreemangal",
        "entity_type": "trip_guide",
        "category": "Trip Guide",
        "title": "Sylhet Tea Gardens & Sreemangal Eco-Resort Touring",
        "content": "Sylhet Guide: Roads to Sreemangal tea estates, Ratargul Swamp Forest, and Jaflong Zero Point feature scenic paved highways with undulating terrain and frequent rain. The Hyundai Tucson AWD, Toyota Camry Hybrid, and Toyota Noah MPV provide whisper-quiet cabin comfort and exceptional fuel efficiency.",
        "tags": ["trip", "sylhet", "sreemangal", "jaflong", "tea garden", "tucson", "camry"],
        "metadata": {"destinations": ["Sylhet", "Sreemangal", "Jaflong"], "recommendedVehicles": ["fleet_tucson_awd", "fleet_camry_hybrid", "fleet_noah_hybrid"]}
    },
    {
        "id": "trip_coxsbazar_marine_drive",
        "entity_type": "trip_guide",
        "category": "Trip Guide",
        "title": "Cox's Bazar Marine Drive Scenic Coastal Highway",
        "content": "Marine Drive Guide: The 80 km Marine Drive from Cox's Bazar to Inani and Teknaf is one of Asia's most scenic coastal routes. The Ford Mustang GT V8 Convertible or Tesla Model Y Long Range offer breathtaking open-air ocean views, smooth cruising, and unmatched photography backdrops.",
        "tags": ["trip", "coxsbazar", "marine drive", "inani", "convertible", "mustang", "tesla"],
        "metadata": {"destinations": ["Cox's Bazar", "Inani", "Teknaf"], "recommendedVehicles": ["fleet_mustang_gt", "fleet_tesla_modely"]}
    },
    {
        "id": "trip_padma_bridge_expressway",
        "entity_type": "trip_guide",
        "category": "Trip Guide",
        "title": "Dhaka to Southern Districts via Padma Bridge Expressway",
        "content": "Padma Expressway Guide: 8-lane expressway connecting Dhaka to Barishal, Khulna, and Kuakata. High-speed cruising speeds (100 km/h) make executive sedans (Mercedes E-Class, BMW 5 Series) and electric vehicles (BYD Seal, Tesla) ideal choices. FastTag RFID toll lanes allow seamless crossing.",
        "tags": ["trip", "padma bridge", "expressway", "kuakata", "barishal", "mercedes", "bmw"],
        "metadata": {"destinations": ["Padma Bridge", "Kuakata", "Barishal"], "recommendedVehicles": ["fleet_mercedes_eclass", "fleet_byd_seal"]}
    },
    {
        "id": "trip_kuakata_sunset_beach",
        "entity_type": "trip_guide",
        "category": "Trip Guide",
        "title": "Kuakata Sagar Kannya Beach & Payra Bridge Highway",
        "content": "Kuakata Guide: Known as Daughter of the Sea where sunrise and sunset can be viewed from the same sandy shoreline. Highway from Dhaka via Padma and Payra bridges is fully paved. Toyota RAV4 AWD, Camry Hybrid, and Toyota Voxy MPV provide ultra-smooth long-distance family travel.",
        "tags": ["trip", "kuakata", "beach", "sunset", "sunrise", "family", "payra bridge"],
        "metadata": {"destinations": ["Kuakata", "Patakhali"], "recommendedVehicles": ["fleet_toyota_rav4", "fleet_camry_hybrid"]}
    },
    {
        "id": "trip_saint_martin_teknaf",
        "entity_type": "trip_guide",
        "category": "Trip Guide",
        "title": "Teknaf Ship Jetty Gateway for Saint Martin's Island",
        "content": "Saint Martin Gateway: Drive to Teknaf Damdamia Jetty before catching the 9:30 AM sea cruise ships. Secure vehicle parking with 24/7 CCTV surveillance is available at our Teknaf partner depot for multi-day island travelers.",
        "tags": ["trip", "saint martin", "teknaf", "ship", "island", "jetty", "parking"],
        "metadata": {"destinations": ["Teknaf", "Saint Martin"], "recommendedVehicles": ["fleet_tucson_awd", "fleet_hiace_grandia"]}
    },
    {
        "id": "trip_tanguar_haor_sunamganj",
        "entity_type": "trip_guide",
        "category": "Trip Guide",
        "title": "Tanguar Haor Wetland & Shimul Bagan Sunamganj Trail",
        "content": "Tanguar Haor Guide: Journey from Sylhet to Sunamganj and Tahirpur boat ghats. Monsoon season (June-September) features heavy waterlogged roads and ferry crossings. High-clearance SUVs (Toyota Prado TX, Hilux Rocco) are strongly recommended.",
        "tags": ["trip", "tanguar haor", "sunamganj", "shimul bagan", "boat", "haor", "monsoon"],
        "metadata": {"destinations": ["Tanguar Haor", "Sunamganj"], "recommendedVehicles": ["fleet_prado_tx", "fleet_hilux_rocco"]}
    },
    {
        "id": "trip_rangamati_lake_hills",
        "entity_type": "trip_guide",
        "category": "Trip Guide",
        "title": "Rangamati Kaptai Lake & Hanging Bridge Scenic Tour",
        "content": "Rangamati Guide: Scenic winding highway from Chittagong along the shores of Kaptai Lake and Shuvolong Falls. Paved roads with gentle hill curves. The Toyota Noah Hybrid MPV, Hyundai Tucson AWD, and Kia Sportage GT-Line offer unmatched scenic viewing.",
        "tags": ["trip", "rangamati", "kaptai lake", "hanging bridge", "hills", "family"],
        "metadata": {"destinations": ["Rangamati", "Kaptai"], "recommendedVehicles": ["fleet_toyota_noah", "fleet_tucson_awd"]}
    },
    {
        "id": "trip_sundarbans_mongla",
        "entity_type": "trip_guide",
        "category": "Trip Guide",
        "title": "Sundarbans Gateway via Mongla Port & Khulna Highway",
        "content": "Sundarbans Guide: Driving to Mongla Port eco-tourism launches from Dhaka via Padma Bridge is now only 4.5 hours. Paved highway with commercial cargo traffic. Mercedes E-Class, Toyota HiAce Grandia, and Toyota Camry ensure fatigue-free highway touring.",
        "tags": ["trip", "sundarbans", "mongla", "khulna", "padma bridge", "tour"],
        "metadata": {"destinations": ["Sundarbans", "Mongla", "Khulna"], "recommendedVehicles": ["fleet_hiace_grandia", "fleet_camry_hybrid"]}
    },

    # ==========================================
    # 💼 5. CORPORATE, VIP & CHAUFFEUR SERVICES (20 FAQs)
    # ==========================================
    {
        "id": "service_chauffeur_vip",
        "entity_type": "faq",
        "category": "Chauffeur Service",
        "title": "Professional English-Speaking Chauffeur Driver Service",
        "content": "Chauffeur Service: Available for +$35/day across all vehicle categories. All drivers are background-checked, trained in defensive driving, English-proficient, and dressed in formal business attire. Overnight outstation driver allowance is $20/night (covers driver boarding and meals).",
        "tags": ["service", "chauffeur", "driver", "vip", "corporate", "english driver"],
        "metadata": {"dailyChauffeurFee": 35, "overnightAllowance": 20}
    },
    {
        "id": "service_airport_meet_greet",
        "entity_type": "faq",
        "category": "Airport Transfer",
        "title": "Dhaka Airport (DAC) VIP Terminal Meet & Greet Service",
        "content": "Airport VIP Protocol: We offer complimentary flight-delay tracking and flight monitoring for Dhaka Hazrat Shahjalal International Airport (DAC Terminal 1, 2, and 3). Our airport concierge meets passengers at the arrival exit canopy with personalized nameplates and luggage trolley assistance.",
        "tags": ["service", "airport", "transfer", "dac", "terminal 3", "meet and greet"],
        "metadata": {"airportTracking": True}
    },
    {
        "id": "service_wedding_car_rental",
        "entity_type": "faq",
        "category": "Event & Wedding",
        "title": "Wedding Car Fleet Rentals & Floral Decoration Packages",
        "content": "Wedding Rentals: Premium luxury bridal cars (Mercedes E-Class, BMW 5 Series, Toyota Alphard Lounge, Mustang Convertible) available with professional fresh floral decoration packages (+$40) and uniformed chauffeurs for wedding ceremonies and receptions.",
        "tags": ["service", "wedding", "marriage", "bridal", "decoration", "mercedes", "alphard"],
        "metadata": {"weddingDecorationDaily": 40}
    },
    {
        "id": "service_corporate_monthly_lease",
        "entity_type": "faq",
        "category": "Corporate Lease",
        "title": "Long-Term Monthly Fleet Leasing & Corporate Billing",
        "content": "Corporate Leasing: Dedicated 30-day, 6-month, and annual corporate lease agreements available with up to 35% discount off standard daily rates. Includes dedicated account managers, monthly consolidated VAT/tax invoicing, preventative maintenance replacement cars, and comprehensive zero-excess coverage.",
        "tags": ["service", "corporate", "monthly", "lease", "discount", "tax", "vat"],
        "metadata": {"monthlyDiscountPct": 35}
    },
    {
        "id": "service_payment_methods",
        "entity_type": "faq",
        "category": "Payment & Billing",
        "title": "Accepted Global & Domestic Payment Methods",
        "content": "Payment Options: We accept Visa, MasterCard, American Express, UnionPay, bKash, Nagad, Bank Wire Transfers, and corporate POs. International cards are processed in USD or BDT at transparent mid-market exchange rates with zero hidden transaction surcharges.",
        "tags": ["payment", "visa", "mastercard", "amex", "bkash", "nagad", "currency"],
        "metadata": {"currencies": ["USD", "BDT"]}
    },
    {
        "id": "service_diplomatic_escort_armored",
        "entity_type": "faq",
        "category": "VIP Delegation",
        "title": "Diplomatic Missions & High-Security Delegation Fleets",
        "content": "Diplomatic Fleet: We supply synchronized convoys of identical Mercedes-Benz S-Class, BMW 7 Series, and Toyota Prado SUVs with trained executive security drivers for foreign embassies, visiting ministers, and multilateral summits.",
        "tags": ["service", "diplomatic", "embassy", "vip", "delegation", "convoy"],
        "metadata": {"diplomaticClearance": True}
    },
    {
        "id": "service_filmmaking_camera_rig",
        "entity_type": "faq",
        "category": "Media & Cinema",
        "title": "Film & Commercial Production Camera Tracking Vehicles",
        "content": "Media Vehicles: Customized Toyota Hilux 4x4 pickups and Ford Ranger Raptors equipped with anti-vibration camera crane mounts, 220V inverter power outlets, and heavy equipment storage for cinematic film shoots.",
        "tags": ["service", "cinema", "media", "camera", "film", "pickup"],
        "metadata": {"filmRigReady": True}
    },
    {
        "id": "service_hourly_city_rental",
        "entity_type": "faq",
        "category": "Hourly Packages",
        "title": "Dhaka City 4-Hour & 8-Hour Hourly Chauffeur Packages",
        "content": "Hourly City Packages: For fast business meetings and shopping within Dhaka metropolitan area: 4-Hour / 40 km Package ($40 Sedan / $65 SUV); 8-Hour / 80 km Package ($65 Sedan / $110 SUV). Includes fuel, professional driver, and parking.",
        "tags": ["service", "hourly", "city", "dhaka", "package", "meetings"],
        "metadata": {"hourly4HrPackage": 40, "hourly8HrPackage": 65}
    },
    {
        "id": "service_ev_charging_network",
        "entity_type": "faq",
        "category": "EV Infrastructure",
        "title": "Electric Vehicle Supercharging & Free Home Wallbox Cables",
        "content": "EV Charging: Every Tesla, BYD, and Porsche rental includes a complimentary Type 2 / CCS2 portable charging cable and RFID access cards to national fast-charging networks across Dhaka, Chittagong, and Sylhet highways.",
        "tags": ["service", "ev", "charging", "tesla", "byd", "supercharger"],
        "metadata": {"evCableIncluded": True}
    },
    {
        "id": "service_luggage_excess_van",
        "entity_type": "faq",
        "category": "Luggage Capacity",
        "title": "Excess Luggage Capacity Guidelines for Group Travel",
        "content": "Luggage Planning: For groups of 5+ passengers traveling with 6+ large hard-shell suitcases, we recommend the Toyota HiAce Grandia 11-seater or Toyota Alphard with fold-up 3rd-row seats to ensure passenger cabin legroom is never compromised.",
        "tags": ["service", "luggage", "suitcases", "van", "hiace", "capacity"],
        "metadata": {"maxLuggageHiAce": 10}
    }
]

async def seed_100_plus_documents():
    """
    Seeds comprehensive 100+ dataset into PostgreSQL / NeonDB and computes vector embeddings.
    """
    print(f"[Seed100] Connecting to PostgreSQL database...")
    await init_database_engine()

    async with get_db_session() as session:
        total_to_seed = len(EXPANDED_100_DOCS)
        print(f"[Seed100] Inserting {total_to_seed} comprehensive domain documents into NeonDB...")
        
        inserted_count = 0
        for doc_data in EXPANDED_100_DOCS:
            # Check existing
            result = await session.execute(
                select(KnowledgeDocument).where(KnowledgeDocument.id == doc_data["id"])
            )
            existing = result.scalar_one_or_none()

            canonical = CanonicalBuilder.build(doc_data["entity_type"], doc_data)
            content_hash = ChangeDetector.compute_hash(canonical)

            if existing:
                existing.category = doc_data["category"]
                existing.title = doc_data["title"]
                existing.content = doc_data["content"]
                existing.canonical_text = canonical
                existing.tags = doc_data.get("tags", [])
                existing.metadata_json = doc_data.get("metadata", {})
                existing.content_hash = content_hash
                existing.is_active = True
                existing.updated_at = get_utc_now()
                doc_id = existing.id
            else:
                new_doc = KnowledgeDocument(
                    id=doc_data["id"],
                    entity_type=doc_data.get("entity_type", "general"),
                    entity_id=doc_data["id"],
                    category=doc_data["category"],
                    title=doc_data["title"],
                    content=doc_data["content"],
                    canonical_text=canonical,
                    tags=doc_data.get("tags", []),
                    metadata_json=doc_data.get("metadata", {}),
                    content_hash=content_hash,
                    is_active=True,
                    created_at=get_utc_now()
                )
                session.add(new_doc)
                doc_id = new_doc.id

            await session.commit()

            # Compute and update vector embedding
            chunks = chunker.chunk_text(canonical)
            chunk_texts = [c["chunk_text"] for c in chunks]
            embeddings = await get_batch_embeddings(chunk_texts)

            await IndexUpdater.index_document_chunks(
                session=session,
                document_id=doc_id,
                chunks_data=chunks,
                embeddings=embeddings
            )
            inserted_count += 1
            if inserted_count % 15 == 0 or inserted_count == total_to_seed:
                print(f"[Seed100] Progress: {inserted_count}/{total_to_seed} documents indexed...")

        print(f"\n[Seed100] SUCCESS: Total {inserted_count} domain documents successfully seeded & indexed in NeonDB PostgreSQL!")

if __name__ == "__main__":
    asyncio.run(seed_100_plus_documents())
