"""SQLite database layer for NRE — Nellore Real Estate."""

import sqlite3
import os
from pathlib import Path

DB_DIR = Path(__file__).parent
DB_PATH = DB_DIR / "nre.db"


def get_connection():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS areas (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            zone TEXT DEFAULT 'Central'
        );

        CREATE TABLE IF NOT EXISTS properties (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            title           TEXT NOT NULL,
            property_type   TEXT NOT NULL,
            locality        TEXT NOT NULL,
            price           INTEGER NOT NULL,
            bedrooms        INTEGER,
            bathrooms       INTEGER,
            size_sqft       INTEGER,
            description     TEXT,
            seller_name     TEXT NOT NULL,
            seller_phone    TEXT NOT NULL,
            seller_whatsapp TEXT,
            facing          TEXT,
            age_years       INTEGER DEFAULT 0,
            is_featured     INTEGER DEFAULT 0,
            status          TEXT DEFAULT 'Active',
            posted_date     TEXT DEFAULT (date('now')),
            images          TEXT,
            latitude        REAL,
            longitude       REAL
        );
    """)
    conn.commit()
    conn.close()
    migrate_db()


def migrate_db():
    """Safely add new columns to existing databases (idempotent)."""
    conn = get_connection()
    migrations = [
        "ALTER TABLE properties ADD COLUMN images TEXT",
        "ALTER TABLE properties ADD COLUMN latitude REAL",
        "ALTER TABLE properties ADD COLUMN longitude REAL",
    ]
    for sql in migrations:
        try:
            conn.execute(sql)
        except Exception:
            pass  # Column already exists
    conn.commit()
    conn.close()




def is_seeded() -> bool:
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM areas").fetchone()[0]
    conn.close()
    return count > 0


# ── Areas ─────────────────────────────────────────────────────────────────────

def get_all_areas() -> list[str]:
    conn = get_connection()
    rows = conn.execute("SELECT name FROM areas ORDER BY name").fetchall()
    conn.close()
    return [r["name"] for r in rows]


def get_areas_with_count() -> list[dict]:
    conn = get_connection()
    rows = conn.execute("""
        SELECT a.name, a.zone,
               COUNT(p.id) AS property_count
        FROM areas a
        LEFT JOIN properties p ON p.locality = a.name AND p.status = 'Active'
        GROUP BY a.name
        ORDER BY property_count DESC, a.name
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def insert_area(name: str, zone: str = "Central"):
    conn = get_connection()
    conn.execute(
        "INSERT OR IGNORE INTO areas (name, zone) VALUES (?, ?)", (name, zone)
    )
    conn.commit()
    conn.close()


# ── Properties ────────────────────────────────────────────────────────────────

def search_properties(
    locality: list[str] | None = None,
    property_type: list[str] | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    min_beds: int | None = None,
    status: str = "Active",
    featured_only: bool = False,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    conn = get_connection()
    clauses = ["status = ?"]
    params: list = [status]

    if locality:
        placeholders = ",".join("?" * len(locality))
        clauses.append(f"locality IN ({placeholders})")
        params.extend(locality)

    if property_type:
        placeholders = ",".join("?" * len(property_type))
        clauses.append(f"property_type IN ({placeholders})")
        params.extend(property_type)

    if min_price is not None:
        clauses.append("price >= ?")
        params.append(min_price)

    if max_price is not None:
        clauses.append("price <= ?")
        params.append(max_price)

    if min_beds is not None and min_beds > 0:
        clauses.append("bedrooms >= ?")
        params.append(min_beds)

    if featured_only:
        clauses.append("is_featured = 1")

    where = " AND ".join(clauses)
    query = f"""
        SELECT * FROM properties
        WHERE {where}
        ORDER BY is_featured DESC, posted_date DESC
        LIMIT ? OFFSET ?
    """
    params.extend([limit, offset])
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_property_by_id(prop_id: int) -> dict | None:
    conn = get_connection()
    row = conn.execute("SELECT * FROM properties WHERE id = ?", (prop_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def add_property(data: dict) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO properties
            (title, property_type, locality, price, bedrooms, bathrooms,
             size_sqft, description, seller_name, seller_phone, seller_whatsapp,
             facing, age_years, is_featured, status, posted_date,
             images, latitude, longitude)
        VALUES
            (:title, :property_type, :locality, :price, :bedrooms, :bathrooms,
             :size_sqft, :description, :seller_name, :seller_phone, :seller_whatsapp,
             :facing, :age_years, :is_featured, :status, date('now'),
             :images, :latitude, :longitude)
    """, data)
    prop_id = cur.lastrowid
    conn.commit()
    conn.close()
    return prop_id



def total_property_count(status: str = "Active") -> int:
    conn = get_connection()
    count = conn.execute(
        "SELECT COUNT(*) FROM properties WHERE status = ?", (status,)
    ).fetchone()[0]
    conn.close()
    return count


def total_area_count() -> int:
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM areas").fetchone()[0]
    conn.close()
    return count


def update_property_images(prop_id: int, images_csv: str):
    """Store comma-separated image filenames for a property."""
    conn = get_connection()
    conn.execute(
        "UPDATE properties SET images = ? WHERE id = ?", (images_csv, prop_id)
    )
    conn.commit()
    conn.close()
