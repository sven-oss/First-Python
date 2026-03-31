import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "crm.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS companies (
                id          TEXT PRIMARY KEY,
                name        TEXT NOT NULL,
                industry    TEXT,
                website     TEXT,
                email       TEXT,
                phone       TEXT,
                street      TEXT,
                city        TEXT,
                state       TEXT,
                zip_code    TEXT,
                country     TEXT,
                notes       TEXT,
                created_at  TEXT NOT NULL,
                updated_at  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS contacts (
                id          TEXT PRIMARY KEY,
                first_name  TEXT NOT NULL,
                last_name   TEXT NOT NULL,
                email       TEXT,
                phone       TEXT,
                mobile      TEXT,
                job_title   TEXT,
                department  TEXT,
                company_id  TEXT REFERENCES companies(id) ON DELETE SET NULL,
                street      TEXT,
                city        TEXT,
                state       TEXT,
                zip_code    TEXT,
                country     TEXT,
                notes       TEXT,
                created_at  TEXT NOT NULL,
                updated_at  TEXT NOT NULL
            );
        """)
