from datetime import datetime, timezone
from typing import Optional
from .database import get_connection
from .models import Contact


def _row_to_contact(row) -> Contact:
    return Contact(**dict(row))


def create(contact: Contact) -> Contact:
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO contacts
                (id, first_name, last_name, email, phone, mobile, job_title, department,
                 company_id, street, city, state, zip_code, country, notes, created_at, updated_at)
            VALUES
                (:id, :first_name, :last_name, :email, :phone, :mobile, :job_title, :department,
                 :company_id, :street, :city, :state, :zip_code, :country, :notes, :created_at, :updated_at)
        """, contact.__dict__)
    return contact


def get(contact_id: str) -> Optional[Contact]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM contacts WHERE id = ?", (contact_id,)
        ).fetchone()
    return _row_to_contact(row) if row else None


def list_all(search: Optional[str] = None) -> list[Contact]:
    with get_connection() as conn:
        if search:
            pattern = f"%{search}%"
            rows = conn.execute("""
                SELECT * FROM contacts
                WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ? OR job_title LIKE ?
                ORDER BY last_name, first_name
            """, (pattern, pattern, pattern, pattern)).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM contacts ORDER BY last_name, first_name"
            ).fetchall()
    return [_row_to_contact(r) for r in rows]


def update(contact_id: str, **fields) -> Optional[Contact]:
    if not fields:
        return get(contact_id)
    fields["updated_at"] = datetime.now(timezone.utc).isoformat()
    set_clause = ", ".join(f"{k} = :{k}" for k in fields)
    fields["id"] = contact_id
    with get_connection() as conn:
        conn.execute(f"UPDATE contacts SET {set_clause} WHERE id = :id", fields)
    return get(contact_id)


def delete(contact_id: str) -> bool:
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    return cursor.rowcount > 0


def assign_company(contact_id: str, company_id: Optional[str]) -> Optional[Contact]:
    """Assign a contact to a company, or pass None to unlink."""
    return update(contact_id, company_id=company_id)


def move_to_company(contact_id: str, new_company_id: str) -> Optional[Contact]:
    """Move a contact from their current company to a new one."""
    return update(contact_id, company_id=new_company_id)
