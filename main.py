from crm.database import init_db
from crm.models import Company, Contact
import crm.companies as companies
import crm.contacts as contacts


# ── helpers ──────────────────────────────────────────────────────────────────

def prompt(label: str, default: str = "") -> str:
    value = input(f"  {label}{f' [{default}]' if default else ''}: ").strip()
    return value or default


def pick_company() -> str | None:
    """Let the user pick a company by number, or skip."""
    all_companies = companies.list_all()
    if not all_companies:
        print("  (no companies on file)")
        return None
    for i, c in enumerate(all_companies, 1):
        print(f"  {i}. {c.name}")
    choice = input("  Select number (or Enter to skip): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(all_companies):
        return all_companies[int(choice) - 1].id
    return None


# ── company screens ───────────────────────────────────────────────────────────

def company_add():
    print("\n--- Add Company ---")
    name = prompt("Name (required)")
    if not name:
        print("Name is required.")
        return
    c = Company(
        name=name,
        industry=prompt("Industry") or None,
        website=prompt("Website") or None,
        email=prompt("Email") or None,
        phone=prompt("Phone") or None,
        street=prompt("Street") or None,
        city=prompt("City") or None,
        state=prompt("State") or None,
        zip_code=prompt("Zip Code") or None,
        country=prompt("Country") or None,
        notes=prompt("Notes") or None,
    )
    companies.create(c)
    print(f"\nCreated company: {c.name} (ID: {c.id})")


def company_list():
    print("\n--- Companies ---")
    search = input("  Search (or Enter for all): ").strip() or None
    results = companies.list_all(search)
    if not results:
        print("  No companies found.")
        return
    for c in results:
        print(f"\n{c.display()}")
        print(f"  ─────────────────────────")


def company_view():
    print("\n--- View Company ---")
    print("  Select company:")
    company_id = pick_company()
    if not company_id:
        return
    c = companies.get(company_id)
    print(f"\n{c.display()}")
    linked = companies.get_contacts(company_id)
    if linked:
        print(f"\n  Contacts ({len(linked)}):")
        for ct in linked:
            print(f"    - {ct.full_name}  {ct.job_title or ''}")


def company_edit():
    print("\n--- Edit Company ---")
    print("  Select company:")
    company_id = pick_company()
    if not company_id:
        return
    c = companies.get(company_id)
    print(f"  Editing: {c.name}  (press Enter to keep current value)")
    fields = {}
    for attr in ["name", "industry", "website", "email", "phone",
                 "street", "city", "state", "zip_code", "country", "notes"]:
        val = prompt(attr.replace("_", " ").title(), getattr(c, attr) or "")
        fields[attr] = val or None
    # name must not be empty
    if not fields.get("name"):
        fields["name"] = c.name
    updated = companies.update(company_id, **fields)
    print(f"\nUpdated: {updated.name}")


def company_delete():
    print("\n--- Delete Company ---")
    print("  Select company to delete:")
    company_id = pick_company()
    if not company_id:
        return
    c = companies.get(company_id)
    confirm = input(f"  Delete '{c.name}'? Contacts will be unlinked. [y/N]: ").strip().lower()
    if confirm == "y":
        companies.delete(company_id)
        print(f"  Deleted '{c.name}'.")
    else:
        print("  Cancelled.")


# ── contact screens ───────────────────────────────────────────────────────────

def contact_add():
    print("\n--- Add Contact ---")
    first = prompt("First Name (required)")
    last = prompt("Last Name (required)")
    if not first or not last:
        print("First and last name are required.")
        return
    print("  Link to company? ")
    company_id = pick_company()
    ct = Contact(
        first_name=first,
        last_name=last,
        email=prompt("Email") or None,
        phone=prompt("Phone") or None,
        mobile=prompt("Mobile") or None,
        job_title=prompt("Job Title") or None,
        department=prompt("Department") or None,
        company_id=company_id,
        street=prompt("Street") or None,
        city=prompt("City") or None,
        state=prompt("State") or None,
        zip_code=prompt("Zip Code") or None,
        country=prompt("Country") or None,
        notes=prompt("Notes") or None,
    )
    contacts.create(ct)
    print(f"\nCreated contact: {ct.full_name} (ID: {ct.id})")


def contact_list():
    print("\n--- Contacts ---")
    search = input("  Search (or Enter for all): ").strip() or None
    results = contacts.list_all(search)
    if not results:
        print("  No contacts found.")
        return
    for ct in results:
        company_name = None
        if ct.company_id:
            c = companies.get(ct.company_id)
            company_name = c.name if c else None
        print(f"\n{ct.display(company_name)}")
        print(f"  ─────────────────────────")


def contact_view():
    print("\n--- View Contact ---")
    search = input("  Search name: ").strip()
    results = contacts.list_all(search)
    if not results:
        print("  No contacts found.")
        return
    for i, ct in enumerate(results, 1):
        print(f"  {i}. {ct.full_name}  ({ct.email or 'no email'})")
    choice = input("  Select number: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(results)):
        return
    ct = results[int(choice) - 1]
    company_name = None
    if ct.company_id:
        c = companies.get(ct.company_id)
        company_name = c.name if c else None
    print(f"\n{ct.display(company_name)}")


def contact_edit():
    print("\n--- Edit Contact ---")
    search = input("  Search name: ").strip()
    results = contacts.list_all(search)
    if not results:
        print("  No contacts found.")
        return
    for i, ct in enumerate(results, 1):
        print(f"  {i}. {ct.full_name}")
    choice = input("  Select number: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(results)):
        return
    ct = results[int(choice) - 1]
    print(f"  Editing: {ct.full_name}  (press Enter to keep current value)")
    fields = {}
    for attr in ["first_name", "last_name", "email", "phone", "mobile",
                 "job_title", "department", "street", "city", "state",
                 "zip_code", "country", "notes"]:
        val = prompt(attr.replace("_", " ").title(), getattr(ct, attr) or "")
        fields[attr] = val or None
    if not fields.get("first_name"): fields["first_name"] = ct.first_name
    if not fields.get("last_name"):  fields["last_name"]  = ct.last_name
    updated = contacts.update(ct.id, **fields)
    print(f"\nUpdated: {updated.full_name}")


def contact_move():
    print("\n--- Move Contact to Another Company ---")
    search = input("  Search contact name: ").strip()
    results = contacts.list_all(search)
    if not results:
        print("  No contacts found.")
        return
    for i, ct in enumerate(results, 1):
        company_name = ""
        if ct.company_id:
            c = companies.get(ct.company_id)
            company_name = f" @ {c.name}" if c else ""
        print(f"  {i}. {ct.full_name}{company_name}")
    choice = input("  Select contact number: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(results)):
        return
    ct = results[int(choice) - 1]
    print(f"\n  Select new company for {ct.full_name}:")
    new_company_id = pick_company()
    if new_company_id:
        updated = contacts.move_to_company(ct.id, new_company_id)
        c = companies.get(new_company_id)
        print(f"  Moved {updated.full_name} to {c.name}.")
    else:
        unlink = input("  Unlink from current company instead? [y/N]: ").strip().lower()
        if unlink == "y":
            contacts.assign_company(ct.id, None)
            print(f"  {ct.full_name} unlinked from company.")


def contact_delete():
    print("\n--- Delete Contact ---")
    search = input("  Search name: ").strip()
    results = contacts.list_all(search)
    if not results:
        print("  No contacts found.")
        return
    for i, ct in enumerate(results, 1):
        print(f"  {i}. {ct.full_name}  ({ct.email or 'no email'})")
    choice = input("  Select number: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(results)):
        return
    ct = results[int(choice) - 1]
    confirm = input(f"  Delete '{ct.full_name}'? [y/N]: ").strip().lower()
    if confirm == "y":
        contacts.delete(ct.id)
        print(f"  Deleted '{ct.full_name}'.")
    else:
        print("  Cancelled.")


# ── menus ─────────────────────────────────────────────────────────────────────

COMPANY_MENU = {
    "1": ("Add company",    company_add),
    "2": ("List companies", company_list),
    "3": ("View company",   company_view),
    "4": ("Edit company",   company_edit),
    "5": ("Delete company", company_delete),
}

CONTACT_MENU = {
    "1": ("Add contact",              contact_add),
    "2": ("List contacts",            contact_list),
    "3": ("View contact",             contact_view),
    "4": ("Edit contact",             contact_edit),
    "5": ("Move contact to company",  contact_move),
    "6": ("Delete contact",           contact_delete),
}

MAIN_MENU = {
    "1": "Companies",
    "2": "Contacts",
    "q": "Quit",
}


def run_submenu(title: str, menu: dict):
    while True:
        print(f"\n=== {title} ===")
        for key, (label, _) in menu.items():
            print(f"  {key}. {label}")
        print("  b. Back")
        choice = input("\nChoice: ").strip().lower()
        if choice == "b":
            break
        if choice in menu:
            menu[choice][1]()
        else:
            print("  Invalid choice.")


def main():
    init_db()
    print("\n╔══════════════════════╗")
    print("║    Python CRM v1.0   ║")
    print("╚══════════════════════╝")
    while True:
        print("\n=== Main Menu ===")
        for key, label in MAIN_MENU.items():
            print(f"  {key}. {label}")
        choice = input("\nChoice: ").strip().lower()
        if choice == "1":
            run_submenu("Companies", COMPANY_MENU)
        elif choice == "2":
            run_submenu("Contacts", CONTACT_MENU)
        elif choice == "q":
            print("Goodbye.")
            break
        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    main()
