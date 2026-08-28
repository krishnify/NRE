"""Seed script — populates Nellore areas and sample properties."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import init_db, insert_area, add_property, is_seeded

# ── Nellore City Areas / Localities ───────────────────────────────────────────
# Organised by zone for future filtering

AREAS = [
    # Central / Old City
    ("Santhapet", "Central"),
    ("Trunk Road", "Central"),
    ("R.C. Road", "Central"),
    ("Grand Trunk Road", "Central"),
    ("Pogathota", "Central"),
    ("Dargamitta", "Central"),
    ("Nellore Bus Stand Area", "Central"),
    ("Gandhi Nagar", "Central"),
    ("Bhavani Nagar", "Central"),
    ("Ashok Nagar", "Central"),
    ("Kothapet", "Central"),
    ("Krishnapet", "Central"),
    ("Ramnagar", "Central"),
    ("Nehru Nagar", "Central"),
    ("Ambedkar Nagar", "Central"),
    ("Ramalingapuram", "Central"),
    ("Brodipet", "Central"),
    ("Shankar Nagar", "Central"),
    ("Subhash Nagar", "Central"),
    ("LIC Colony", "Central"),
    ("Judges Colony", "Central"),
    ("S.R. Nagar", "Central"),
    ("Vasantha Nagar", "Central"),
    ("Sarada Nagar", "Central"),
    ("Dhanalakshmi Nagar", "Central"),

    # North Nellore
    ("Vedayapalem", "North"),
    ("Magunta Layout", "North"),
    ("Balaji Nagar", "North"),
    ("Indira Nagar", "North"),
    ("Pinakini Nagar", "North"),
    ("Auto Nagar", "North"),
    ("Allipuram", "North"),
    ("Raghavaiah Nagar", "North"),
    ("NTR Nagar", "North"),
    ("Bhagyanagar", "North"),
    ("Harinathapuram", "North"),
    ("Padmavathi Nagar", "North"),
    ("Vijayalakshmi Nagar", "North"),
    ("Saipuram Colony", "North"),
    ("Teachers Colony", "North"),
    ("Engineers Colony", "North"),
    ("Akkayyapalem", "North"),
    ("P.S.R. Nagar", "North"),

    # South Nellore
    ("Pedaganjam", "South"),
    ("Kappatralla", "South"),
    ("Sydapuram", "South"),
    ("Pottur", "South"),
    ("Ramji Nagar", "South"),
    ("Old Town", "South"),
    ("Pattabhiram Nagar", "South"),
    ("Muthukuru Road", "South"),
    ("Mandalam", "South"),
    ("Kaluvoya", "South"),

    # East / Port Area
    ("Krishnapatnam", "East"),
    ("Muthukur", "East"),
    ("Kavali Road", "East"),
    ("Chinthareddypalem", "East"),
    ("Nawabpet", "East"),
    ("Allur Road", "East"),
    ("Naidupeta Road", "East"),

    # West / Suburban
    ("Rapur Road", "West"),
    ("Kakutur", "West"),
    ("Podalakur Road", "West"),
    ("Bogole", "West"),
    ("Kovur Road", "West"),
    ("Pellakur", "West"),
    ("Duttalur", "West"),
    ("Mypadu Road", "West"),
    ("Atmakur Road", "West"),
    ("Vinjamur Road", "West"),
    ("Kalukonda", "West"),
]

# ── Sample Properties ─────────────────────────────────────────────────────────

SAMPLE_PROPERTIES = [
    # ── Trunk Road ──
    {
        "title": "3 BHK Premium Apartment — Trunk Road",
        "property_type": "Apartment",
        "locality": "Trunk Road",
        "price": 7500000,  # 75 Lakhs
        "bedrooms": 3,
        "bathrooms": 2,
        "size_sqft": 1450,
        "description": (
            "Spacious 3 BHK apartment on 4th floor with excellent ventilation. "
            "Located right on Trunk Road with easy access to schools, hospitals, "
            "and shopping. Modular kitchen, 24/7 water supply, covered car parking, "
            "power backup, and security. Semi-furnished."
        ),
        "seller_name": "Ravi Kumar",
        "seller_phone": "9848012345",
        "seller_whatsapp": "9848012345",
        "facing": "East",
        "age_years": 3,
        "is_featured": 1,
        "status": "Active",
    },
    {
        "title": "2 BHK Flat — Trunk Road (Ready to Move)",
        "property_type": "Apartment",
        "locality": "Trunk Road",
        "price": 4500000,  # 45 Lakhs
        "bedrooms": 2,
        "bathrooms": 2,
        "size_sqft": 1050,
        "description": (
            "Well-maintained 2 BHK flat on 2nd floor. UDS 450 sqft. "
            "Close to Nellore Collectorate and city centre. "
            "Vitrified tiles, granite kitchen platform, compound wall, "
            "covered parking. Immediate registration possible."
        ),
        "seller_name": "Srinivas Reddy",
        "seller_phone": "9701234567",
        "seller_whatsapp": "9701234567",
        "facing": "North",
        "age_years": 5,
        "is_featured": 0,
        "status": "Active",
    },

    # ── Magunta Layout ──
    {
        "title": "Individual House — Magunta Layout",
        "property_type": "House",
        "locality": "Magunta Layout",
        "price": 9800000,  # 98 Lakhs
        "bedrooms": 4,
        "bathrooms": 3,
        "size_sqft": 2200,
        "description": (
            "G+1 individual house on 200 sq.yd plot. Ground floor: hall, 2 bedrooms, "
            "kitchen, bathroom. First floor: 2 bedrooms, hall, terrace. "
            "Bore water + municipal water. Car parking for 2 vehicles. "
            "Located in a peaceful residential colony."
        ),
        "seller_name": "Lakshmi Prasad",
        "seller_phone": "9866543210",
        "seller_whatsapp": "9866543210",
        "facing": "East",
        "age_years": 8,
        "is_featured": 1,
        "status": "Active",
    },
    {
        "title": "Residential Plot — 150 Sq.Yd — Magunta Layout",
        "property_type": "Plot",
        "locality": "Magunta Layout",
        "price": 3200000,  # 32 Lakhs
        "bedrooms": None,
        "bathrooms": None,
        "size_sqft": 1350,
        "description": (
            "DTCP approved residential plot in prime Magunta Layout location. "
            "150 sq.yd corner plot, 20ft road access, all clear title documents, "
            "ready for immediate registration. Surrounded by residential houses. "
            "Close to schools and markets."
        ),
        "seller_name": "Venkata Rao",
        "seller_phone": "9963001122",
        "seller_whatsapp": "9963001122",
        "facing": "North",
        "age_years": 0,
        "is_featured": 0,
        "status": "Active",
    },

    # ── Balaji Nagar ──
    {
        "title": "3 BHK Villa — Balaji Nagar",
        "property_type": "Villa",
        "locality": "Balaji Nagar",
        "price": 12500000,  # 1.25 Cr
        "bedrooms": 3,
        "bathrooms": 3,
        "size_sqft": 2800,
        "description": (
            "Luxurious independent villa with premium interiors. G+1 structure on "
            "240 sq.yd plot. Granite flooring, modular kitchen with chimney, "
            "2 car parking, landscaped garden, terrace with water tank. "
            "Gated community with 24/7 security. Fully furnished."
        ),
        "seller_name": "Suresh Naidu",
        "seller_phone": "9441223344",
        "seller_whatsapp": "9441223344",
        "facing": "East",
        "age_years": 2,
        "is_featured": 1,
        "status": "Active",
    },
    {
        "title": "2 BHK Apartment — Balaji Nagar",
        "property_type": "Apartment",
        "locality": "Balaji Nagar",
        "price": 3800000,  # 38 Lakhs
        "bedrooms": 2,
        "bathrooms": 1,
        "size_sqft": 980,
        "description": (
            "Brand new 2 BHK apartment in a 4-floor complex. Vastu compliant, "
            "east-facing, vitrified tiles, stainless steel main door. "
            "Lift, overhead tank, borewell, covered parking. "
            "Bank loan available. Price negotiable."
        ),
        "seller_name": "Anand Builders",
        "seller_phone": "9848099887",
        "seller_whatsapp": "9848099887",
        "facing": "East",
        "age_years": 0,
        "is_featured": 0,
        "status": "Active",
    },

    # ── Vedayapalem ──
    {
        "title": "1 BHK Flat — Vedayapalem (Budget Pick)",
        "property_type": "Apartment",
        "locality": "Vedayapalem",
        "price": 1800000,  # 18 Lakhs
        "bedrooms": 1,
        "bathrooms": 1,
        "size_sqft": 600,
        "description": (
            "Affordable 1 BHK flat ideal for working professionals or small families. "
            "Located near Nellore railway station. Close to markets and bus routes. "
            "Good rental potential. Owner direct — no brokerage."
        ),
        "seller_name": "Padmavathi",
        "seller_phone": "9515443322",
        "seller_whatsapp": "9515443322",
        "facing": "West",
        "age_years": 6,
        "is_featured": 0,
        "status": "Active",
    },
    {
        "title": "Commercial Shop — Vedayapalem Main Road",
        "property_type": "Shop",
        "locality": "Vedayapalem",
        "price": 5500000,  # 55 Lakhs
        "bedrooms": None,
        "bathrooms": 1,
        "size_sqft": 400,
        "description": (
            "Ground floor commercial shop on busy Vedayapalem main road. "
            "High footfall area, excellent visibility. Suitable for retail, "
            "pharmacy, mobile shop, or food outlet. "
            "20 ft frontage, direct road access. Currently rented for ₹18,000/month."
        ),
        "seller_name": "Krishna Murthy",
        "seller_phone": "9246554433",
        "seller_whatsapp": "9246554433",
        "facing": "East",
        "age_years": 12,
        "is_featured": 0,
        "status": "Active",
    },

    # ── Santhapet ──
    {
        "title": "4 BHK House — Santhapet (Old City Charm)",
        "property_type": "House",
        "locality": "Santhapet",
        "price": 8500000,  # 85 Lakhs
        "bedrooms": 4,
        "bathrooms": 3,
        "size_sqft": 2600,
        "description": (
            "Spacious 4 BHK house in the heart of old Nellore. "
            "Well-connected to all parts of the city. "
            "RCC construction, compound wall, bore + municipal water, "
            "two-wheeler shed. "
            "Ideal for large family or can be used as rental property."
        ),
        "seller_name": "Subramanyam",
        "seller_phone": "9848056789",
        "seller_whatsapp": "9848056789",
        "facing": "North",
        "age_years": 15,
        "is_featured": 0,
        "status": "Active",
    },

    # ── Indira Nagar ──
    {
        "title": "3 BHK Apartment — Indira Nagar",
        "property_type": "Apartment",
        "locality": "Indira Nagar",
        "price": 6200000,  # 62 Lakhs
        "bedrooms": 3,
        "bathrooms": 2,
        "size_sqft": 1380,
        "description": (
            "3 BHK flat in a well-maintained apartment complex. "
            "3rd floor, East facing. Modular kitchen, master bedroom with attached bath, "
            "common hall with balcony. "
            "Society maintenance only ₹1,200/month. "
            "Close to SVMC hospital, Sarada College, and Leela Mahal junction."
        ),
        "seller_name": "Narendra Kumar",
        "seller_phone": "9700112233",
        "seller_whatsapp": "9700112233",
        "facing": "East",
        "age_years": 4,
        "is_featured": 1,
        "status": "Active",
    },

    # ── Gandhi Nagar ──
    {
        "title": "Office Space — Gandhi Nagar",
        "property_type": "Office Space",
        "locality": "Gandhi Nagar",
        "price": 4200000,  # 42 Lakhs
        "bedrooms": None,
        "bathrooms": 2,
        "size_sqft": 900,
        "description": (
            "Ready-to-move office space on 1st floor. "
            "AC cabins, reception area, conference room, pantry. "
            "Ideal for IT company, consultancy, or financial services office. "
            "Dedicated parking for 4 cars in basement. "
            "UPS power backup, fiber internet connection available."
        ),
        "seller_name": "Surya Realtors",
        "seller_phone": "9989001234",
        "seller_whatsapp": "9989001234",
        "facing": "North",
        "age_years": 7,
        "is_featured": 0,
        "status": "Active",
    },

    # ── Krishnapatnam ──
    {
        "title": "Farm House — Krishnapatnam Road",
        "property_type": "Farm House",
        "locality": "Krishnapatnam",
        "price": 18000000,  # 1.8 Cr
        "bedrooms": 3,
        "bathrooms": 2,
        "size_sqft": 5400,
        "description": (
            "Beautiful farm house on 1.5 acres near Krishnapatnam port road. "
            "3 BHK bungalow with large hall, open terrace, mango orchard, "
            "borewell with pump set. "
            "Excellent investment near the growing industrial corridor. "
            "Clear patta title. Suitable for agri/hospitality/weekend retreat."
        ),
        "seller_name": "Anjaneyulu",
        "seller_phone": "9642778899",
        "seller_whatsapp": "9642778899",
        "facing": "East",
        "age_years": 5,
        "is_featured": 1,
        "status": "Active",
    },

    # ── Pogathota ──
    {
        "title": "200 Sq.Yd Plot — Pogathota",
        "property_type": "Plot",
        "locality": "Pogathota",
        "price": 5000000,  # 50 Lakhs
        "bedrooms": None,
        "bathrooms": None,
        "size_sqft": 1800,
        "description": (
            "DTCP approved 200 sq.yd residential-cum-commercial plot in Pogathota. "
            "40ft main road frontage. Suitable for apartments or commercial complex. "
            "All documents clear, EC from 1975. "
            "Close to Ojas Hospital and Jubilee bus stand."
        ),
        "seller_name": "Eswara Rao",
        "seller_phone": "9848067891",
        "seller_whatsapp": "9848067891",
        "facing": "South",
        "age_years": 0,
        "is_featured": 0,
        "status": "Active",
    },

    # ── Muthukur ──
    {
        "title": "Individual House — Muthukur Town",
        "property_type": "House",
        "locality": "Muthukur",
        "price": 3500000,  # 35 Lakhs
        "bedrooms": 3,
        "bathrooms": 2,
        "size_sqft": 1600,
        "description": (
            "3 BHK independent house in Muthukur town centre. "
            "G+1, 120 sq.yd site, compound wall. "
            "Close to Muthukur railway station and government hospital. "
            "Good locality, quiet residential area. "
            "Municipal water and drainage connections available."
        ),
        "seller_name": "Chandra Sekhar",
        "seller_phone": "9550998877",
        "seller_whatsapp": "9550998877",
        "facing": "West",
        "age_years": 10,
        "is_featured": 0,
        "status": "Active",
    },

    # ── Rapur Road ──
    {
        "title": "Commercial Showroom — Rapur Highway",
        "property_type": "Commercial",
        "locality": "Rapur Road",
        "price": 8000000,  # 80 Lakhs
        "bedrooms": None,
        "bathrooms": 2,
        "size_sqft": 2000,
        "description": (
            "Large showroom on NH-16 (Rapur Highway). "
            "2000 sqft ground floor with 30ft frontage, 3-phase power, "
            "ample parking space in front. "
            "Suitable for automobile dealership, furniture showroom, or supermarket. "
            "High traffic location between Nellore and Rapur. Excellent visibility."
        ),
        "seller_name": "Vikram Properties",
        "seller_phone": "9133445566",
        "seller_whatsapp": "9133445566",
        "facing": "East",
        "age_years": 4,
        "is_featured": 0,
        "status": "Active",
    },

    # ── Pedaganjam ──
    {
        "title": "2 BHK House — Pedaganjam",
        "property_type": "House",
        "locality": "Pedaganjam",
        "price": 2800000,  # 28 Lakhs
        "bedrooms": 2,
        "bathrooms": 1,
        "size_sqft": 900,
        "description": (
            "Compact 2 BHK house with small garden space. "
            "80 sq.yd site with well water and borewell backup. "
            "All documents clear, ready for registration. "
            "Suitable for budget buyers or as rental investment. "
            "30 mins from Nellore city centre."
        ),
        "seller_name": "Ramana Murthy",
        "seller_phone": "9494112233",
        "seller_whatsapp": "9494112233",
        "facing": "North",
        "age_years": 12,
        "is_featured": 0,
        "status": "Active",
    },

    # ── Bhavani Nagar ──
    {
        "title": "4 BHK Luxury Apartment — Bhavani Nagar",
        "property_type": "Apartment",
        "locality": "Bhavani Nagar",
        "price": 11000000,  # 1.1 Cr
        "bedrooms": 4,
        "bathrooms": 4,
        "size_sqft": 2400,
        "description": (
            "Ultra-premium 4 BHK apartment in Nellore's premium residential hub. "
            "Features include — Italian marble flooring, imported kitchen fittings, "
            "gymnasium, swimming pool, children's play area, conference hall. "
            "24/7 CCTV security, video door phone. Vaastu compliant, North-East corner flat."
        ),
        "seller_name": "Elixir Properties",
        "seller_phone": "9000112233",
        "seller_whatsapp": "9000112233",
        "facing": "North-East",
        "age_years": 1,
        "is_featured": 1,
        "status": "Active",
    },

    # ── Kakutur ──
    {
        "title": "Agricultural Land — Kakutur (5 Acres)",
        "property_type": "Plot",
        "locality": "Kakutur",
        "price": 7500000,  # 75 Lakhs
        "bedrooms": None,
        "bathrooms": None,
        "size_sqft": 217800,
        "description": (
            "5 acres fertile agricultural land near Kakutur. "
            "Canal water irrigation available, bore-well with pump. "
            "Currently growing paddy. Clear patta documents. "
            "Excellent land for farming or future township development. "
            "Directly accessible from tar road."
        ),
        "seller_name": "Yellaiah",
        "seller_phone": "9676334455",
        "seller_whatsapp": "9676334455",
        "facing": "East",
        "age_years": 0,
        "is_featured": 0,
        "status": "Active",
    },

    # ── Ashok Nagar ──
    {
        "title": "3 BHK Independent House — Ashok Nagar",
        "property_type": "House",
        "locality": "Ashok Nagar",
        "price": 7200000,  # 72 Lakhs
        "bedrooms": 3,
        "bathrooms": 2,
        "size_sqft": 1800,
        "description": (
            "Well-maintained 3 BHK house in the heart of Ashok Nagar. "
            "Spacious hall, separate dining, modular kitchen, car porch. "
            "160 sq.yd site, RCC construction, 10 year old. "
            "Close to Nellore Collectorate, SP office, and city bus stand. "
            "Walking distance from commercial hubs."
        ),
        "seller_name": "Prakash Reddy",
        "seller_phone": "9849111222",
        "seller_whatsapp": "9849111222",
        "facing": "East",
        "age_years": 10,
        "is_featured": 1,
        "status": "Active",
    },

    # ── Pinakini Nagar ──
    {
        "title": "2 BHK Apartment — Pinakini Nagar",
        "property_type": "Apartment",
        "locality": "Pinakini Nagar",
        "price": 4000000,  # 40 Lakhs
        "bedrooms": 2,
        "bathrooms": 2,
        "size_sqft": 1050,
        "description": (
            "Fresh 2 BHK flat, just completed construction. "
            "Overlooking Pinakini River from the balcony — scenic river view! "
            "High-quality finishes, teak wood main door, "
            "lift, backup generator, rooftop terrace for residents. "
            "Ready for immediate registration. RERA registered."
        ),
        "seller_name": "River View Constructions",
        "seller_phone": "9866990011",
        "seller_whatsapp": "9866990011",
        "facing": "East",
        "age_years": 0,
        "is_featured": 1,
        "status": "Active",
    },
    {
        "title": "100 Sq.Yd Plot — Pinakini Nagar",
        "property_type": "Plot",
        "locality": "Pinakini Nagar",
        "price": 2200000,  # 22 Lakhs
        "bedrooms": None,
        "bathrooms": None,
        "size_sqft": 900,
        "description": (
            "DTCP approved 100 sq.yd plot in a clean residential layout. "
            "Near Pinakini Nagar junction, 30ft road access. "
            "Suitable for G+2 construction. "
            "Close to schools and auto-stand. Clear title."
        ),
        "seller_name": "Satyanarayana",
        "seller_phone": "9492556677",
        "seller_whatsapp": "9492556677",
        "facing": "North",
        "age_years": 0,
        "is_featured": 0,
        "status": "Active",
    },
]


def seed():
    print("Initialising database …")
    init_db()

    if is_seeded():
        print("Database already seeded. Skipping.")
        return

    print(f"Seeding {len(AREAS)} areas …")
    for name, zone in AREAS:
        insert_area(name, zone)

    print(f"Seeding {len(SAMPLE_PROPERTIES)} sample properties …")
    for prop in SAMPLE_PROPERTIES:
        pid = add_property(prop)
        print(f"  Added: [{pid}] {prop['title']}")

    print("✅ Seeding complete!")


if __name__ == "__main__":
    seed()
