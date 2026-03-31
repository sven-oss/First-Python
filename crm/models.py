from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import uuid


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _uuid() -> str:
    return str(uuid.uuid4())


@dataclass
class Company:
    name: str
    industry: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    notes: Optional[str] = None
    id: str = field(default_factory=_uuid)
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def display(self) -> str:
        lines = [f"  ID:       {self.id}", f"  Name:     {self.name}"]
        if self.industry:  lines.append(f"  Industry: {self.industry}")
        if self.website:   lines.append(f"  Website:  {self.website}")
        if self.email:     lines.append(f"  Email:    {self.email}")
        if self.phone:     lines.append(f"  Phone:    {self.phone}")
        address = ", ".join(filter(None, [self.street, self.city, self.state, self.zip_code, self.country]))
        if address:        lines.append(f"  Address:  {address}")
        if self.notes:     lines.append(f"  Notes:    {self.notes}")
        lines.append(f"  Created:  {self.created_at[:10]}")
        return "\n".join(lines)


@dataclass
class Contact:
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    company_id: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    notes: Optional[str] = None
    id: str = field(default_factory=_uuid)
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def display(self, company_name: Optional[str] = None) -> str:
        lines = [f"  ID:         {self.id}", f"  Name:       {self.full_name}"]
        if self.job_title:   lines.append(f"  Title:      {self.job_title}")
        if self.department:  lines.append(f"  Department: {self.department}")
        if company_name:     lines.append(f"  Company:    {company_name}")
        elif self.company_id: lines.append(f"  Company ID: {self.company_id}")
        if self.email:       lines.append(f"  Email:      {self.email}")
        if self.phone:       lines.append(f"  Phone:      {self.phone}")
        if self.mobile:      lines.append(f"  Mobile:     {self.mobile}")
        address = ", ".join(filter(None, [self.street, self.city, self.state, self.zip_code, self.country]))
        if address:          lines.append(f"  Address:    {address}")
        if self.notes:       lines.append(f"  Notes:      {self.notes}")
        lines.append(f"  Created:    {self.created_at[:10]}")
        return "\n".join(lines)
