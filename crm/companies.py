from datetime import datetime, timezone
from typing import Optional
from .database import get_connection
from .models import Company


def _row_to_company(row) -> Company:
    return Company(**dict(row))


def create(company: Company) -> Company:
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO companies
                (id, name, industry, website, email, phone,
                 street, city, state, zip_code, country, notes, created_at, updated_at)
            VALUES
                (:id, :name, :industry, :website, :email, :phone,
                 :street, :city, :state, :zip_code, :country, :notes, :created_at, :updated_at)
        """, company.__dict__)
    return company


def get(company_id: str) -> Optional[Company]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM companies WHERE id = ?", (company_id,)
        ).fetchone()
    return _row_to_company(row) if row else None


def list_all(search: Optional[str] = None) -> list[Company]:
    with get_connection() as conn:
        if search:
            pattern = f"%{search}%"
            rows = conn.execute(
                "SELECT * FROM companies WHERE name LIKE ? OR industry LIKE ? OR city LIKE ? ORDER BY name",
                (pattern, pattern, pattern)
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM companies ORDER BY name").fetchall()
    return [_row_to_company(r) for r in rows]


def update(company_id: str, **fields) -> Optional[Company]:
    if not fields:
        return get(company_id)
    fields["updated_at"] = datetime.now(timezone.utc).isoformat()
    set_clause = ", ".join(f"{k} = :{k}" for k in fields)
    fields["id"] = company_id
    with get_connection() as conn:
        conn.execute(f"UPDATE companies SET {set_clause} WHERE id = :id", fields)
    return get(company_id)


def delete(company_id: str) -> bool:
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM companies WHERE id = ?", (company_id,))
    return cursor.rowcount > 0


def get_contacts(company_id: str) -> list:
    from .contacts import list_all as list_contacts
    return [c for c in list_contacts() if c.company_id == company_id]
