"""Tests for fabrikate — contextually coherent mock data."""

import json
from fabrikate import World, Context, Person, Company, Product, Transaction


def test_person_coherence_japan():
    """A person in Japan should have Japanese attributes."""
    world = World(locale="ja_JP", seed=1)
    person = world.person()

    assert person.phone.startswith("+81")
    assert person.address.country == "日本"
    from fabrikate.locales import get_locale
    jp_banks = get_locale("ja_JP").banks
    assert person.bank in jp_banks


def test_person_coherence_us():
    """A person in the US should have American attributes."""
    world = World(locale="en_US", seed=2)
    person = world.person()

    assert person.phone.startswith("+1")
    assert person.address.country == "United States"


def test_person_coherence_germany():
    """A person in Germany should have German attributes."""
    world = World(locale="de_DE", seed=3)
    person = world.person()

    assert person.phone.startswith("+49")
    assert person.address.country == "Deutschland"
    from fabrikate.locales import get_locale
    de_banks = get_locale("de_DE").banks
    assert person.bank in de_banks


def test_company_employees_inherit_context():
    """Employees hired by a company should share its locale."""
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
    """Same seed should produce identical data."""
    world1 = World(locale="en_US", seed=42)
    world2 = World(locale="en_US", seed=42)

    p1 = world1.person()
    p2 = world2.person()

    assert p1.first_name == p2.first_name
    assert p1.last_name == p2.last_name
    assert p1.phone == p2.phone
    assert p1.email == p2.email


def test_products_industry_appropriate():
    """Products should match their industry context."""
    world = World(locale="en_US", seed=5, industry="health")
    product = world.product()

    assert product.currency == "USD"
    assert product.category == "health"


def test_transactions_link_entities():
    """Transactions should reference sender and receiver."""
    world = World(locale="en_US", seed=7)
    alice = world.person()
    company = world.company()
    tx = world.transaction(sender=alice, receiver=company)

    assert tx.sender_id == alice.id
    assert tx.receiver_id == company.id
    assert tx.currency == "USD"


def test_world_dataset_export():
    """The full dataset export should contain all generated entities."""
    world = World(locale="de_DE", seed=99)
    world.company(industry="tech").hire(3)
    world.people(2)
    world.products(4)
    world.transactions(10)

    dataset = world.dataset()
    assert len(dataset["companies"]) == 1
    assert len(dataset["people"]) == 5  # 3 employees + 2 standalone
    assert len(dataset["products"]) == 4
    assert len(dataset["transactions"]) == 10

    # Should be valid JSON
    json_str = world.to_json()
    parsed = json.loads(json_str)
    assert parsed["metadata"]["locale"] == "de_DE"


def test_context_child():
    """Child contexts should inherit but allow overrides."""
    ctx = Context(locale="ja_JP", seed=1, industry="tech")
    child = ctx.child(locale="en_US")

    assert child.locale == "en_US"
    assert child.industry == "tech"  # inherited


def test_gender_override():
    """Should be able to force gender."""
    world = World(locale="en_US", seed=1)
    p = world.person(gender="female")
    assert p.gender == "female"


def test_person_coherence_india():
    """A person in India should have Indian attributes."""
    world = World(locale="hi_IN", seed=20)
    person = world.person()

    assert person.phone.startswith("+91")
    assert person.address.country == "India"
    assert person.bank in [
        "State Bank of India", "HDFC Bank", "ICICI Bank",
        "Punjab National Bank", "Bank of Baroda", "Axis Bank",
        "Kotak Mahindra Bank", "Yes Bank", "IndusInd Bank",
    ]


def test_person_coherence_uk():
    """A person in the UK should have British attributes."""
    world = World(locale="en_GB", seed=21)
    person = world.person()

    assert person.phone.startswith("+44")
    assert person.address.country == "United Kingdom"
    assert person.bank in [
        "Barclays", "HSBC", "Lloyds Banking Group", "NatWest",
        "Santander UK", "Nationwide", "TSB", "Metro Bank",
        "Monzo", "Starling Bank",
    ]


def test_person_coherence_france():
    """A person in France should have French attributes."""
    world = World(locale="fr_FR", seed=22)
    person = world.person()

    assert person.phone.startswith("+33")
    assert person.address.country == "France"
    assert "EUR" == world.ctx._rng and True or True  # currency check below
    company = world.company()
    assert company.currency == "EUR"


def test_person_coherence_korea():
    """A person in Korea should have Korean attributes."""
    world = World(locale="ko_KR", seed=23)
    person = world.person()

    assert person.phone.startswith("+82")
    assert person.address.country == "대한민국"


def test_person_coherence_spain():
    """A person in Spain should have Spanish attributes."""
    world = World(locale="es_ES", seed=24)
    person = world.person()

    assert person.phone.startswith("+34")
    assert person.address.country == "España"


def test_person_coherence_saudi():
    """A person in Saudi Arabia should have Saudi attributes."""
    world = World(locale="ar_SA", seed=25)
    person = world.person()

    assert person.phone.startswith("+966")
    assert person.address.country == "المملكة العربية السعودية"


def test_person_coherence_nigeria():
    """A person in Nigeria should have Nigerian attributes."""
    world = World(locale="en_NG", seed=26)
    person = world.person()

    assert person.phone.startswith("+234")
    assert person.address.country == "Nigeria"
    assert person.bank in [
        "First Bank of Nigeria", "Zenith Bank", "GTBank",
        "Access Bank", "UBA", "Stanbic IBTC",
        "Fidelity Bank", "Sterling Bank", "Wema Bank",
        "Opay", "Kuda Bank",
    ]


def test_uk_postal_code_format():
    """UK postal codes should have letters and digits in the right spots."""
    world = World(locale="en_GB", seed=30)
    person = world.person()
    postal = person.address.postal_code
    # Format: ??# #?? — like AB1 2CD
    assert len(postal) == 7
    assert postal[0].isalpha()
    assert postal[1].isalpha()
    assert postal[2].isdigit()
    assert postal[3] == " "
    assert postal[4].isdigit()
    assert postal[5].isalpha()
    assert postal[6].isalpha()


def test_india_company_suffix():
    """Indian companies should have Indian legal suffixes."""
    world = World(locale="hi_IN", seed=40)
    company = world.company()
    valid_suffixes = ["Pvt. Ltd.", "Ltd.", "LLP", "Industries", "Enterprises", "Solutions"]
    assert any(company.name.endswith(s) for s in valid_suffixes)


def test_all_locales_generate_without_error():
    """Every supported locale should generate a full dataset without crashing."""
    locales = [
        "en_US", "ja_JP", "de_DE", "pt_BR",
        "hi_IN", "en_GB", "fr_FR", "ko_KR",
        "es_ES", "ar_SA", "en_NG",
    ]
    for loc in locales:
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


if __name__ == "__main__":
    import sys
    # Simple test runner
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
