"""Utility helper functions for NRE app."""

from datetime import datetime, date


def format_price(price: int) -> str:
    """Format price in Indian number system with ₹ symbol."""
    if price >= 10_000_000:  # 1 Crore
        crores = price / 10_000_000
        if crores == int(crores):
            return f"₹{int(crores)} Cr"
        return f"₹{crores:.2f} Cr"
    elif price >= 100_000:  # 1 Lakh
        lakhs = price / 100_000
        if lakhs == int(lakhs):
            return f"₹{int(lakhs)} L"
        return f"₹{lakhs:.2f} L"
    else:
        return f"₹{price:,}"


def format_area(sqft: int) -> str:
    """Format area in sqft."""
    return f"{sqft:,} sq.ft"


def whatsapp_link(phone: str, property_title: str) -> str:
    """Generate a WhatsApp click-to-chat link."""
    # Remove spaces and non-numeric chars, add India country code
    clean = "".join(c for c in phone if c.isdigit())
    if len(clean) == 10:
        clean = "91" + clean
    msg = f"Hi, I am interested in your property: {property_title}. Please share more details."
    import urllib.parse
    encoded = urllib.parse.quote(msg)
    return f"https://wa.me/{clean}?text={encoded}"


def days_ago(posted_date) -> str:
    """Return human-readable 'X days ago' from a date string or date object."""
    if isinstance(posted_date, str):
        try:
            d = datetime.strptime(posted_date, "%Y-%m-%d").date()
        except Exception:
            return posted_date
    elif isinstance(posted_date, date):
        d = posted_date
    else:
        return str(posted_date)
    delta = (date.today() - d).days
    if delta == 0:
        return "Today"
    elif delta == 1:
        return "Yesterday"
    elif delta < 30:
        return f"{delta} days ago"
    elif delta < 365:
        months = delta // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    else:
        years = delta // 365
        return f"{years} year{'s' if years > 1 else ''} ago"


def bhk_label(bedrooms) -> str:
    """Return BHK label string."""
    if bedrooms is None or bedrooms == 0:
        return "N/A"
    return f"{bedrooms} BHK"


PROPERTY_TYPE_ICONS = {
    "Apartment": "🏢",
    "House": "🏠",
    "Villa": "🏡",
    "Plot": "🗺️",
    "Commercial": "🏪",
    "Farm House": "🌾",
    "Office Space": "💼",
    "Shop": "🛒",
}


def property_icon(ptype: str) -> str:
    return PROPERTY_TYPE_ICONS.get(ptype, "🏠")


FACING_LABELS = ["East", "West", "North", "South", "North-East", "North-West", "South-East", "South-West"]
PROPERTY_TYPES = list(PROPERTY_TYPE_ICONS.keys())

# Property types that have bedrooms / bathrooms
RESIDENTIAL_TYPES = {"Apartment", "House", "Villa", "Farm House"}

# Nellore default map centre
NELLORE_LAT = 14.4426
NELLORE_LON = 79.9865

# Approximate lat/lon for major Nellore localities
AREA_COORDS: dict[str, tuple[float, float]] = {
    "Trunk Road":            (14.4426, 79.9865),
    "Santhapet":             (14.4385, 79.9808),
    "R.C. Road":             (14.4430, 79.9855),
    "Grand Trunk Road":      (14.4410, 79.9880),
    "Pogathota":             (14.4398, 79.9950),
    "Dargamitta":            (14.4360, 79.9830),
    "Nellore Bus Stand Area":(14.4445, 79.9870),
    "Gandhi Nagar":          (14.4500, 79.9900),
    "Bhavani Nagar":         (14.4480, 79.9820),
    "Ashok Nagar":           (14.4460, 79.9882),
    "Kothapet":              (14.4420, 79.9840),
    "Krishnapet":            (14.4435, 79.9810),
    "Ramnagar":              (14.4455, 79.9845),
    "Nehru Nagar":           (14.4415, 79.9910),
    "Ambedkar Nagar":        (14.4402, 79.9795),
    "Ramalingapuram":        (14.4370, 79.9760),
    "Brodipet":              (14.4390, 79.9875),
    "Shankar Nagar":         (14.4472, 79.9835),
    "Subhash Nagar":         (14.4445, 79.9855),
    "LIC Colony":            (14.4462, 79.9865),
    "Judges Colony":         (14.4488, 79.9850),
    "S.R. Nagar":            (14.4440, 79.9895),
    "Vasantha Nagar":        (14.4425, 79.9835),
    "Sarada Nagar":          (14.4510, 79.9840),
    "Dhanalakshmi Nagar":    (14.4418, 79.9920),
    "Vedayapalem":           (14.4450, 79.9752),
    "Magunta Layout":        (14.4605, 79.9872),
    "Balaji Nagar":          (14.4555, 79.9950),
    "Indira Nagar":          (14.4503, 79.9803),
    "Pinakini Nagar":        (14.4352, 79.9702),
    "Auto Nagar":            (14.4570, 79.9820),
    "Allipuram":             (14.4530, 79.9758),
    "Raghavaiah Nagar":      (14.4618, 79.9900),
    "NTR Nagar":             (14.4590, 79.9860),
    "Bhagyanagar":           (14.4640, 79.9930),
    "Harinathapuram":        (14.4522, 79.9780),
    "Padmavathi Nagar":      (14.4545, 79.9910),
    "Vijayalakshmi Nagar":   (14.4580, 79.9835),
    "Saipuram Colony":       (14.4560, 79.9760),
    "Teachers Colony":       (14.4535, 79.9800),
    "Engineers Colony":      (14.4515, 79.9825),
    "Akkayyapalem":          (14.4492, 79.9775),
    "P.S.R. Nagar":          (14.4568, 79.9870),
    "Pedaganjam":            (14.4250, 79.9900),
    "Kappatralla":           (14.4210, 79.9850),
    "Sydapuram":             (14.4180, 79.9780),
    "Pottur":                (14.4160, 79.9840),
    "Ramji Nagar":           (14.4280, 79.9810),
    "Old Town":              (14.4300, 79.9870),
    "Pattabhiram Nagar":     (14.4320, 79.9920),
    "Muthukuru Road":        (14.4200, 79.9760),
    "Mandalam":              (14.4120, 79.9800),
    "Kaluvoya":              (14.4050, 79.9770),
    "Krishnapatnam":         (14.2550, 80.1280),
    "Muthukur":              (14.3920, 80.0450),
    "Kavali Road":           (14.3800, 80.0100),
    "Chinthareddypalem":     (14.4350, 80.0050),
    "Nawabpet":              (14.4310, 79.9940),
    "Allur Road":            (14.3600, 79.9650),
    "Naidupeta Road":        (14.5800, 80.0500),
    "Rapur Road":            (14.5200, 79.9700),
    "Kakutur":               (14.5050, 79.9600),
    "Podalakur Road":        (14.4800, 79.9550),
    "Bogole":                (14.5500, 79.9500),
    "Kovur Road":            (14.4700, 79.9500),
    "Pellakur":              (14.5350, 79.9600),
    "Duttalur":              (14.5600, 79.9650),
    "Mypadu Road":           (14.4200, 79.9450),
    "Atmakur Road":          (14.4650, 79.9480),
    "Vinjamur Road":         (14.5100, 79.9420),
    "Kalukonda":             (14.4900, 79.9380),
}

# ── Famous Nellore Landmarks & Points of Interest ─────────────────────────────
NELLORE_LANDMARKS: list[dict] = [
    # Malls & Shopping
    {"name": "MGB Felicity Mall & PVR", "category": "🛍️ Mall & Entertainment", "area": "Dargamitta / GT Road", "lat": 14.4321, "lon": 79.9672},
    {"name": "CMR Shopping Mall", "category": "🛍️ Shopping", "area": "Trunk Road", "lat": 14.4418, "lon": 79.9858},
    {"name": "South India Shopping Mall", "category": "🛍️ Shopping", "area": "Trunk Road", "lat": 14.4422, "lon": 79.9862},
    {"name": "RS Brothers & Kalanikethan", "category": "🛍️ Shopping", "area": "Trunk Road", "lat": 14.4430, "lon": 79.9860},
    {"name": "Pogathota Gold Market", "category": "🛍️ Market", "area": "Pogathota", "lat": 14.4398, "lon": 79.9950},
    
    # Hospitals & Healthcare
    {"name": "Narayana Medical College & Hospital", "category": "🏥 Hospital", "area": "Chinthareddypalem", "lat": 14.4350, "lon": 80.0050},
    {"name": "ACSR Govt Medical College & Hospital (RIMS)", "category": "🏥 Hospital", "area": "Dargamitta", "lat": 14.4365, "lon": 79.9835},
    {"name": "Medicover Hospital", "category": "🏥 Hospital", "area": "Ramalingapuram", "lat": 14.4375, "lon": 79.9765},
    {"name": "KIMS Bollineni Hospital", "category": "🏥 Hospital", "area": "Brodipet / Trunk Road", "lat": 14.4392, "lon": 79.9878},
    {"name": "Vijaya Care Hospital", "category": "🏥 Hospital", "area": "Pogathota", "lat": 14.4405, "lon": 79.9940},
    {"name": "Lotus Hospital", "category": "🏥 Hospital", "area": "Trunk Road", "lat": 14.4440, "lon": 79.9875},
    {"name": "Simhapuri Hospital", "category": "🏥 Hospital", "area": "NH16 Mudivarthipalem", "lat": 14.4680, "lon": 79.9980},
    {"name": "Jayabharath Hospital", "category": "🏥 Hospital", "area": "Gandhi Nagar", "lat": 14.4505, "lon": 79.9895},
    
    # Transit & Railway / Bus
    {"name": "Nellore Main Railway Station", "category": "🚆 Railway Station", "area": "Railway Station Road", "lat": 14.4485, "lon": 79.9830},
    {"name": "Nellore South Railway Station", "category": "🚆 Railway Station", "area": "Vedayapalem", "lat": 14.4285, "lon": 79.9710},
    {"name": "RTC Jubilee Bus Stand (Main)", "category": "🚌 Bus Station", "area": "Pogathota / GT Road", "lat": 14.4445, "lon": 79.9870},
    {"name": "Atmakur Bus Stand", "category": "🚌 Bus Station", "area": "Trunk Road / Nawabpet", "lat": 14.4380, "lon": 79.9890},
    {"name": "Ramalingapuram Junction & Bus Stop", "category": "🚏 Junction", "area": "Ramalingapuram", "lat": 14.4370, "lon": 79.9760},
    
    # Educational Institutions
    {"name": "V.R. College & Grounds (VRC)", "category": "🎓 College", "area": "Trunk Road", "lat": 14.4435, "lon": 79.9850},
    {"name": "Vikrama Simhapuri University", "category": "🎓 University", "area": "Kakutur", "lat": 14.5050, "lon": 79.9600},
    {"name": "Narayana Engineering College", "category": "🎓 Engineering College", "area": "Dhurjati Nagar / Muthukur Rd", "lat": 14.4250, "lon": 79.9780},
    {"name": "Audisankara College", "category": "🎓 College", "area": "NH16 / Gudur Road", "lat": 14.3900, "lon": 79.9600},
    {"name": "Sarada Junior College", "category": "🎓 College", "area": "Gandhi Nagar", "lat": 14.4510, "lon": 79.9840},
    {"name": "St. Joseph's Girls High School", "category": "🏫 School", "area": "Santhapet", "lat": 14.4380, "lon": 79.9815},
    {"name": "Kendriya Vidyalaya", "category": "🏫 School", "area": "Ramnagar", "lat": 14.4455, "lon": 79.9845},
    
    # Famous Landmarks, Temples & Government
    {"name": "Collectorate Office & Zilla Parishad", "category": "🏛️ Govt Office", "area": "Dargamitta", "lat": 14.4360, "lon": 79.9830},
    {"name": "AC Subba Reddy Sports Stadium", "category": "🏟️ Stadium", "area": "Dargamitta", "lat": 14.4345, "lon": 79.9815},
    {"name": "Children's Park & Gandhi Statue", "category": "🌳 Park", "area": "Trunk Road", "lat": 14.4410, "lon": 79.9860},
    {"name": "Sri Talpagiri Ranganatha Swamy Temple", "category": "🛕 Temple", "area": "Ranganayakula Pet / Penna River", "lat": 14.4520, "lon": 79.9790},
    {"name": "Barah Shaheed Dargah & Dargah Tank", "category": "🕌 Religious Landmark", "area": "Dargamitta", "lat": 14.4330, "lon": 79.9795},
    {"name": "Jonnawada Sri Kamakshi Temple", "category": "🛕 Temple", "area": "Jonnawada (Penna River)", "lat": 14.4850, "lon": 79.8850},
    {"name": "Penna Barrage / Anicut", "category": "🌊 Landmark", "area": "Penna River Bridge", "lat": 14.4600, "lon": 79.9750},
    {"name": "VRC Centre (V.R. College Circle)", "category": "🚏 Landmark Junction", "area": "Central Trunk Road", "lat": 14.4435, "lon": 79.9855},
    {"name": "Leela Mahal Centre", "category": "🚏 Landmark Junction", "area": "Trunk Road", "lat": 14.4450, "lon": 79.9870},
    {"name": "District Court Complex", "category": "🏛️ Judiciary", "area": "Dargamitta", "lat": 14.4350, "lon": 79.9840},
    {"name": "Head Post Office", "category": "📮 Post Office", "area": "Trunk Road", "lat": 14.4420, "lon": 79.9860},
]


def search_nellore_locations(query: str, max_results: int = 8) -> list[dict]:
    """
    Search for landmarks, areas, streets, hospitals, colleges or buildings in Nellore.
    Uses local landmark database + 71 localities + OpenStreetMap Nominatim live search.
    """
    query = query.strip()
    if not query:
        return []

    q_lower = query.lower()
    results = []
    seen_names = set()

    # 1. Match famous landmarks
    for lm in NELLORE_LANDMARKS:
        if q_lower in lm["name"].lower() or q_lower in lm["area"].lower() or q_lower in lm["category"].lower():
            label = f"{lm['category']} {lm['name']} ({lm['area']})"
            results.append({
                "name": lm["name"],
                "category": lm["category"],
                "area": lm["area"],
                "lat": lm["lat"],
                "lon": lm["lon"],
                "display": label,
                "source": "landmark",
            })
            seen_names.add(lm["name"].lower())

    # 2. Match localities from AREA_COORDS
    for area_name, (alat, alon) in AREA_COORDS.items():
        if q_lower in area_name.lower() and area_name.lower() not in seen_names:
            results.append({
                "name": area_name,
                "category": "📍 Locality",
                "area": "Nellore",
                "lat": alat,
                "lon": alon,
                "display": f"📍 Locality: {area_name}",
                "source": "area",
            })
            seen_names.add(area_name.lower())

    # 3. If query is specific or few local results, query OpenStreetMap Nominatim
    if len(results) < 5 and len(query) >= 3:
        try:
            import urllib.request
            import urllib.parse
            import json
            import ssl

            ctx = ssl._create_unverified_context()
            encoded_q = urllib.parse.urlencode({
                "q": f"{query}, Nellore, Andhra Pradesh, India",
                "format": "json",
                "limit": 5,
                "addressdetails": 1,
            })
            url = f"https://nominatim.openstreetmap.org/search?{encoded_q}"
            req = urllib.request.Request(url, headers={"User-Agent": "NelloreRealEstateApp/2.0"})
            with urllib.request.urlopen(req, context=ctx, timeout=3.5) as resp:
                data = json.loads(resp.read().decode())
                for item in data:
                    item_name = item.get("display_name", "")
                    short_name = item_name.split(",")[0].strip()
                    if short_name.lower() not in seen_names:
                        lat_val = float(item["lat"])
                        lon_val = float(item["lon"])
                        # Verify coordinate is in Nellore region (roughly lat 14.1 to 14.8, lon 79.7 to 80.3)
                        if 14.0 <= lat_val <= 14.9 and 79.5 <= lon_val <= 80.4:
                            clean_display = ", ".join(item_name.split(",")[:3])
                            results.append({
                                "name": short_name,
                                "category": "🌐 Map Location",
                                "area": "Nellore",
                                "lat": lat_val,
                                "lon": lon_val,
                                "display": f"🔍 {clean_display}",
                                "source": "osm",
                            })
                            seen_names.add(short_name.lower())
        except Exception:
            pass  # Fallback to local results on network timeout

    return results[:max_results]

