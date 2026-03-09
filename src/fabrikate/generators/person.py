"""
Person generator — creates people that make sense in their locale.

v0.3.0: Added DOB, job title, salary, national ID, marital status,
blood type, height, weight, phone carrier, credit card type, username,
education, and vehicle. All locale-aware with realistic distributions.
"""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from fabrikate.context import Context
from fabrikate.locales import get_locale
from fabrikate.distributions import (
    bell_curve_int, log_normal_float, weighted_choice, skewed_choice, marital_status,
    BLOOD_TYPE_DIST, CHILDREN_DIST,
)
from fabrikate.reference_data import (
    JOB_TITLES, SALARY_RANGES, NATIONAL_ID_FORMATS, PAYMENT_METHODS,
    PHONE_CARRIERS, CREDIT_CARD_TYPES, UNIVERSITIES, DEGREE_TYPES,
    DEGREE_FIELDS, CAR_BRANDS, INSURANCE_PROVIDERS, BIOMETRICS,
)


@dataclass
class Address:
    street: str
    city: str
    postal_code: str
    country: str

    def __str__(self) -> str:
        return f"{self.street}, {self.city} {self.postal_code}, {self.country}"

    def to_dict(self) -> dict:
        return {"street": self.street, "city": self.city, "postal_code": self.postal_code, "country": self.country}


@dataclass
class Education:
    university: str = ""
    degree: str = ""
    field_of_study: str = ""
    graduation_year: int = 0

    def to_dict(self) -> dict:
        return {"university": self.university, "degree": self.degree, "field_of_study": self.field_of_study, "graduation_year": self.graduation_year}


@dataclass
class Vehicle:
    brand: str = ""
    year: int = 0
    plate_number: str = ""

    def to_dict(self) -> dict:
        return {"brand": self.brand, "year": self.year, "plate_number": self.plate_number}


@dataclass
class MedicalRecord:
    blood_type: str = ""
    height_cm: int = 0
    weight_kg: int = 0
    insurance_provider: str = ""

    def to_dict(self) -> dict:
        return {"blood_type": self.blood_type, "height_cm": self.height_cm, "weight_kg": self.weight_kg, "insurance_provider": self.insurance_provider}


@dataclass
class Person:
    """
    A contextually coherent person with full demographic detail.

    All attributes are consistent with the context's locale — names, address,
    phone, email, bank, salary, ID format, and more.
    """

    # Identity
    id: str = ""
    first_name: str = ""
    last_name: str = ""
    full_name: str = ""
    gender: str = ""
    age: int = 0
    date_of_birth: str = ""
    nationality: str = ""
    national_id: str = ""
    marital_status: str = ""
    children: int = 0

    # Contact
    email: str = ""
    phone: str = ""
    phone_carrier: str = ""
    username: str = ""
    address: Optional[Address] = None

    # Financial
    bank: str = ""
    credit_card_type: str = ""
    salary: float = 0.0
    salary_currency: str = ""

    # Employment
    job_title: str = ""
    department: str = ""
    company_id: Optional[str] = None

    # Education
    education: Optional[Education] = None

    # Vehicle
    vehicle: Optional[Vehicle] = None

    # Medical
    medical: Optional[MedicalRecord] = None

    _ctx: Optional[Context] = field(default=None, repr=False)

    @classmethod
    def generate(cls, ctx: Context, **overrides) -> Person:
        locale = get_locale(ctx.locale)
        rng = ctx._rng
        cc = ctx.country_code

        person = cls(_ctx=ctx)
        person.id = overrides.get("id", str(uuid.UUID(int=rng.getrandbits(128))))

        # --- Gender ---
        person.gender = overrides.get("gender", rng.choice(["male", "female"]))

        # --- Name (skewed — common names more likely) ---
        if person.gender == "male":
            person.first_name = overrides.get("first_name", skewed_choice(rng, locale.first_names_male, skew=1.3))
        else:
            person.first_name = overrides.get("first_name", skewed_choice(rng, locale.first_names_female, skew=1.3))
        person.last_name = overrides.get("last_name", skewed_choice(rng, locale.last_names, skew=1.4))

        if locale.name_order == "family_given":
            person.full_name = f"{person.last_name} {person.first_name}"
        else:
            person.full_name = f"{person.first_name} {person.last_name}"

        # --- Age (bell curve centered at 35) ---
        person.age = overrides.get("age", bell_curve_int(rng, 18, 70, mean=35, sd=12))

        # --- Date of birth ---
        birth_year = ctx.year - person.age
        birth_month = rng.randint(1, 12)
        birth_day = rng.randint(1, 28)
        person.date_of_birth = overrides.get("date_of_birth", f"{birth_year}-{birth_month:02d}-{birth_day:02d}")

        # --- Nationality ---
        person.nationality = overrides.get("nationality", locale.country_name)

        # --- National ID ---
        id_info = NATIONAL_ID_FORMATS.get(cc, {"name": "ID", "format": "############"})
        person.national_id = overrides.get("national_id", _format_id(id_info["format"], rng))

        # --- Marital status (age-dependent) ---
        person.marital_status = overrides.get("marital_status", marital_status(rng, person.age))

        # --- Children (locale-dependent distribution) ---
        children_dist = CHILDREN_DIST.get(cc, CHILDREN_DIST["US"])
        kids = list(children_dist.keys())
        kid_weights = list(children_dist.values())
        if person.age < 25:
            person.children = overrides.get("children", weighted_choice(rng, [0, 0, 1, 0], [80, 5, 10, 5]))
        else:
            person.children = overrides.get("children", weighted_choice(rng, kids, kid_weights))

        # --- Phone ---
        person.phone = _format_pattern(locale.phone_format, rng)

        # --- Phone carrier ---
        carriers = PHONE_CARRIERS.get(cc, ["Unknown"])
        person.phone_carrier = overrides.get("phone_carrier", rng.choice(carriers))

        # --- Address ---
        city = rng.choice(locale.cities)
        street_names = _get_street_names(cc)
        street_fmt = rng.choice(locale.street_formats)
        street = street_fmt.format(
            number=rng.randint(1, 9999),
            name=rng.choice(street_names),
            city=city,
            ward=rng.choice(_DISTRICTS.get(cc, {}).get("wards", ["Central"])),
            district=rng.choice(_DISTRICTS.get(cc, {}).get("districts", ["Central"])),
        )
        postal = _format_postal(locale.postal_code_format, rng)
        person.address = Address(street=street, city=city, postal_code=postal, country=locale.country_name)

        # --- Email & username ---
        name_slug = f"{_romanize(person.first_name)}.{_romanize(person.last_name)}".lower().replace(" ", "")
        domain = rng.choice(locale.email_domains)
        person.email = overrides.get("email", f"{name_slug}@{domain}")
        person.username = overrides.get("username", f"{name_slug}{rng.randint(1, 999)}")

        # --- Bank ---
        person.bank = overrides.get("bank", rng.choice(locale.banks))

        # --- Credit card type (locale-weighted) ---
        cc_types = CREDIT_CARD_TYPES.get(cc, CREDIT_CARD_TYPES["US"])
        cc_items = [t[0] for t in cc_types]
        cc_weights = [t[1] for t in cc_types]
        person.credit_card_type = overrides.get("credit_card_type", weighted_choice(rng, cc_items, cc_weights))

        # --- Salary (log-normal, locale-appropriate) ---
        sal_range = SALARY_RANGES.get(cc, (30000, 60000, 150000))
        person.salary = overrides.get("salary", log_normal_float(rng, sal_range[1], sigma=0.6, low=sal_range[0], high=sal_range[2]))
        person.salary_currency = locale.currency

        # --- Job title ---
        industry = ctx.industry or "general"
        titles = JOB_TITLES.get(industry, JOB_TITLES["general"])
        person.job_title = overrides.get("job_title", rng.choice(titles))

        # --- Department ---
        from fabrikate.reference_data import DEPARTMENTS
        person.department = overrides.get("department", rng.choice(DEPARTMENTS))

        # --- Company link ---
        person.company_id = overrides.get("company_id", None)

        # --- Education ---
        unis = UNIVERSITIES.get(cc, UNIVERSITIES.get("US", ["University"]))
        deg_items = [d[0] for d in DEGREE_TYPES]
        deg_weights = [d[1] for d in DEGREE_TYPES]
        degree = weighted_choice(rng, deg_items, deg_weights)
        grad_offset = {"Bachelor's": 22, "Master's": 24, "PhD": 28, "Associate's": 20, "Diploma": 19}
        grad_year = birth_year + grad_offset.get(degree, 22) + rng.randint(-1, 2)
        person.education = Education(
            university=rng.choice(unis),
            degree=degree,
            field_of_study=rng.choice(DEGREE_FIELDS),
            graduation_year=min(grad_year, ctx.year),
        )

        # --- Vehicle (70% chance of having one) ---
        if rng.random() < 0.70:
            car_data = CAR_BRANDS.get(cc, CAR_BRANDS["US"])
            brands = [c[0] for c in car_data]
            brand_weights = [c[1] for c in car_data]
            car_year = rng.randint(max(ctx.year - 15, 2005), ctx.year)
            plate = _format_plate(cc, rng)
            person.vehicle = Vehicle(
                brand=weighted_choice(rng, brands, brand_weights),
                year=car_year,
                plate_number=plate,
            )

        # --- Medical ---
        bt_dist = BLOOD_TYPE_DIST.get(cc, BLOOD_TYPE_DIST["US"])
        bt_items = list(bt_dist.keys())
        bt_weights = list(bt_dist.values())
        bio = BIOMETRICS.get(cc, BIOMETRICS["US"])
        h_key = "height_m" if person.gender == "male" else "height_f"
        w_key = "weight_m" if person.gender == "male" else "weight_f"
        ins_providers = INSURANCE_PROVIDERS.get(cc, ["National Insurance"])
        person.medical = MedicalRecord(
            blood_type=weighted_choice(rng, bt_items, bt_weights),
            height_cm=bell_curve_int(rng, int(bio[h_key][0]), int(bio[h_key][2]), mean=bio[h_key][1]),
            weight_kg=bell_curve_int(rng, int(bio[w_key][0]), int(bio[w_key][2]), mean=bio[w_key][1]),
            insurance_provider=rng.choice(ins_providers),
        )

        ctx.register(person)
        return person

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "gender": self.gender,
            "age": self.age,
            "date_of_birth": self.date_of_birth,
            "nationality": self.nationality,
            "national_id": self.national_id,
            "marital_status": self.marital_status,
            "children": self.children,
            "email": self.email,
            "phone": self.phone,
            "phone_carrier": self.phone_carrier,
            "username": self.username,
            "address": self.address.to_dict() if self.address else None,
            "bank": self.bank,
            "credit_card_type": self.credit_card_type,
            "salary": self.salary,
            "salary_currency": self.salary_currency,
            "job_title": self.job_title,
            "department": self.department,
            "company_id": self.company_id,
            "education": self.education.to_dict() if self.education else None,
            "vehicle": self.vehicle.to_dict() if self.vehicle else None,
            "medical": self.medical.to_dict() if self.medical else None,
        }


# ============================================================
# Helper functions
# ============================================================

def _format_pattern(pattern: str, rng) -> str:
    return "".join(str(rng.randint(0, 9)) if c == "#" else c for c in pattern)


def _format_postal(pattern: str, rng) -> str:
    result = []
    for c in pattern:
        if c == "#":
            result.append(str(rng.randint(0, 9)))
        elif c == "?":
            result.append(chr(rng.randint(65, 90)))
        else:
            result.append(c)
    return "".join(result)


def _format_id(pattern: str, rng) -> str:
    """Format national ID: # = digit, ? = letter, * = alphanumeric."""
    result = []
    for c in pattern:
        if c == "#":
            result.append(str(rng.randint(0, 9)))
        elif c == "?":
            result.append(chr(rng.randint(65, 90)))
        elif c == "*":
            result.append(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"))
        else:
            result.append(c)
    return "".join(result)


def _format_plate(country_code: str, rng) -> str:
    """Generate a locale-appropriate license plate."""
    formats = {
        "US": "??? ####",
        "JP": "?? ###-####",
        "DE": "?? ?? ####",
        "BR": "??? #?##",
        "IN": "?? ## ?? ####",
        "GB": "??## ???",
        "FR": "??-###-??",
        "KR": "## ? ####",
        "ES": "#### ???",
        "SA": "??? ####",
        "NG": "???-###??",
    }
    fmt = formats.get(country_code, "??? ####")
    return _format_id(fmt, rng)


def _romanize(text: str) -> str:
    ascii_chars = [c for c in text if ord(c) < 128 and c.isalpha()]
    if ascii_chars:
        return "".join(ascii_chars)
    h = hashlib.md5(text.encode()).hexdigest()[:8]
    return f"user{h}"


_STREET_NAMES = {
    "US": ["Maple", "Oak", "Cedar", "Elm", "Pine", "Main", "Park", "Washington", "Lincoln", "Jefferson"],
    "JP": ["桜", "梅", "松", "竹", "富士", "大和", "瑞穂"],
    "DE": ["Goethe", "Schiller", "Mozart", "Bach", "Beethoven", "Linden", "Berliner", "Münchner", "Rhein"],
    "BR": ["Ipanema", "Copacabana", "Liberdade", "Consolação", "Augusta", "Paulista", "Tiradentes"],
    "IN": ["Mahatma Gandhi", "Nehru", "Tagore", "Subhash", "Patel", "Ambedkar", "Shivaji", "Rajaji", "Tilak"],
    "GB": ["Victoria", "Church", "High", "Station", "Mill", "King", "Queen", "Castle", "Bridge", "Manor"],
    "FR": ["Victor Hugo", "Pasteur", "Voltaire", "Molière", "Liberté", "République", "Gambetta", "Leclerc"],
    "KR": ["세종대", "강남대", "테헤란", "올림픽", "영동대", "압구정", "삼성"],
    "ES": ["Gran Vía", "Castellana", "Alcalá", "Cervantes", "Colón", "Goya", "Serrano", "Velázquez"],
    "SA": ["الملك فهد", "الملك عبدالعزيز", "العروبة", "التحلية", "الأمير سلطان", "الثلاثين"],
    "NG": ["Broad", "Marina", "Ahmadu Bello", "Herbert Macaulay", "Adeola Odeku", "Allen", "Awolowo"],
}

_DISTRICTS = {
    "JP": {"wards": ["中央", "港", "新宿", "渋谷", "千代田", "品川", "目黒", "世田谷"], "districts": ["本町", "元町", "旭町", "栄町", "幸町", "緑町"]},
    "KR": {"wards": ["강남", "서초", "마포", "영등포", "종로", "용산", "송파", "강서"], "districts": ["역삼", "삼성", "논현", "신사", "청담", "대치"]},
    "SA": {"wards": ["العليا", "السلامة", "النزهة", "الروضة", "المروج"], "districts": ["الورود", "الملز", "السليمانية", "الربوة", "المرسلات"]},
    "IN": {"wards": ["Andheri", "Bandra", "Koramangala", "Whitefield", "Salt Lake", "T Nagar", "Jubilee Hills"], "districts": ["Sector 5", "Block A", "Phase 2", "Extension", "Layout", "Nagar"]},
}


def _get_street_names(country_code: str) -> list[str]:
    return _STREET_NAMES.get(country_code, _STREET_NAMES["US"])
