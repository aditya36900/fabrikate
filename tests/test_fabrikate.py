"""Tests for fabrikate v0.3.0 — contextually coherent mock data."""

import json
from fabrikate import World, Context, Person, Company, Product, Transaction
from fabrikate.locales import get_locale, supported_locales


def test_person_coherence_japan():
    world = World(locale="ja_JP", seed=1)
    person = world.person()
    assert person.phone.startswith("+81")
    assert person.address.country == "日本"
    assert person.bank in get_locale("ja_JP").banks


def test_person_coherence_us():
    world = World(locale="en_US", seed=2)
    person = world.person()
    assert person.phone.startswith("+1")
    assert person.address.country == "United States"


def test_person_coherence_germany():
    world = World(locale="de_DE", seed=3)
    person = world.person()
    assert person.phone.startswith("+49")
    assert person.address.country == "Deutschland"
    assert person.bank in get_locale("de_DE").banks


def test_company_employees_inherit_context():
    world = World(locale="pt_BR", seed=10)
    company = world.company(industry="tech")
    employees = company.hire(5)
    assert len(employees) == 5
    assert company.currency == "BRL"
    for emp in employees:
        assert emp.company_id == company.id
        assert emp.address.country == "Brasil"
        assert emp.phone.startswith("+55")


def test_seed_reproducibility():
    world1 = World(locale="en_US", seed=42)
    world2 = World(locale="en_US", seed=42)
    p1 = world1.person()
    p2 = world2.person()
    assert p1.first_name == p2.first_name
    assert p1.last_name == p2.last_name
    assert p1.phone == p2.phone
    assert p1.email == p2.email


def test_products_industry_appropriate():
    world = World(locale="en_US", seed=5, industry="health")
    product = world.product()
    assert product.currency == "USD"
    assert product.category == "health"


def test_transactions_link_entities():
    world = World(locale="en_US", seed=7)
    alice = world.person()
    company = world.company()
    tx = world.transaction(sender=alice, receiver=company)
    assert tx.sender_id == alice.id
    assert tx.receiver_id == company.id
    assert tx.currency == "USD"


def test_world_dataset_export():
    world = World(locale="de_DE", seed=99)
    world.company(industry="tech").hire(3)
    world.people(2)
    world.products(4)
    world.transactions(10)
    dataset = world.dataset()
    assert len(dataset["companies"]) == 1
    assert len(dataset["people"]) == 5
    assert len(dataset["products"]) == 4
    assert len(dataset["transactions"]) == 10
    json_str = world.to_json()
    parsed = json.loads(json_str)
    assert parsed["metadata"]["locale"] == "de_DE"


def test_context_child():
    ctx = Context(locale="ja_JP", seed=1, industry="tech")
    child = ctx.child(locale="en_US")
    assert child.locale == "en_US"
    assert child.industry == "tech"


def test_gender_override():
    world = World(locale="en_US", seed=1)
    p = world.person(gender="female")
    assert p.gender == "female"


# --- New v0.3.0 tests ---

def test_person_has_new_fields():
    """Person should have all new v0.3.0 fields populated."""
    world = World(locale="en_US", seed=42)
    p = world.person()
    assert p.date_of_birth != ""
    assert p.national_id != ""
    assert p.marital_status in ["single", "married", "engaged", "divorced", "widowed"]
    assert p.children >= 0
    assert p.phone_carrier != ""
    assert p.username != ""
    assert p.credit_card_type != ""
    assert p.salary > 0
    assert p.salary_currency == "USD"
    assert p.job_title != ""
    assert p.department != ""
    assert p.education is not None
    assert p.education.university != ""
    assert p.education.degree != ""
    assert p.medical is not None
    assert p.medical.blood_type != ""
    assert p.medical.height_cm > 0
    assert p.medical.weight_kg > 0
    assert p.medical.insurance_provider != ""


def test_person_india_new_fields():
    """Indian person should have India-specific new fields."""
    world = World(locale="hi_IN", seed=42)
    p = world.person()
    assert p.nationality == "India"
    assert p.phone_carrier in ["Jio", "Airtel", "Vi (Vodafone Idea)", "BSNL", "MTNL"]
    assert p.salary_currency == "INR"
    assert p.salary >= 300000  # minimum Indian salary in data


def test_company_has_new_fields():
    """Company should have tax_id, revenue, website, departments."""
    world = World(locale="en_US", seed=42)
    c = world.company()
    assert c.tax_id != ""
    assert c.annual_revenue > 0
    assert c.website.startswith("https://")
    assert len(c.departments) >= 2


def test_transaction_has_new_fields():
    """Transaction should have payment_method, tax, invoice."""
    world = World(locale="hi_IN", seed=42)
    tx = world.transaction()
    assert tx.payment_method != ""
    assert tx.tax_amount >= 0
    assert tx.total_amount != 0
    assert tx.invoice_number.startswith("INV-")


def test_transaction_payment_method_locale():
    """Indian transactions should use Indian payment methods."""
    world = World(locale="hi_IN", seed=42)
    methods = set()
    for _ in range(50):
        tx = world.transaction()
        methods.add(tx.payment_method)
    assert "UPI" in methods  # UPI should appear for India


def test_vehicle_generation():
    """Vehicles should be locale-appropriate."""
    world = World(locale="hi_IN", seed=42)
    people_with_cars = [p for p in world.people(20) if p.vehicle is not None]
    assert len(people_with_cars) > 0
    brands = {p.vehicle.brand for p in people_with_cars}
    assert "Maruti Suzuki" in brands or "Hyundai" in brands or "Tata" in brands


def test_all_locales_generate_without_error():
    """Every supported locale should generate a full dataset without crashing."""
    for loc in supported_locales():
        world = World(locale=loc, seed=100)
        company = world.company()
        company.hire(3)
        world.products(2, company=company)
        world.transactions(5)
        data = world.dataset()
        assert len(data["people"]) == 3, f"{loc}: expected 3 people"
        assert len(data["companies"]) == 1, f"{loc}: expected 1 company"
        assert len(data["products"]) == 2, f"{loc}: expected 2 products"
        assert len(data["transactions"]) == 5, f"{loc}: expected 5 transactions"


def test_person_to_dict_complete():
    """to_dict should include all new fields."""
    world = World(locale="en_US", seed=1)
    d = world.person().to_dict()
    required_keys = [
        "id", "first_name", "last_name", "full_name", "gender", "age",
        "date_of_birth", "nationality", "national_id", "marital_status",
        "children", "email", "phone", "phone_carrier", "username", "address",
        "bank", "credit_card_type", "salary", "salary_currency", "job_title",
        "department", "education", "vehicle", "medical",
    ]
    for key in required_keys:
        assert key in d, f"Missing key: {key}"


if __name__ == "__main__":
    import sys
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    passed = 0
    for test in tests:
        try:
            test()
            print(f"  ✓ {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} tests passed")
    sys.exit(0 if passed == len(tests) else 1)
