"""
Person generator — creates people that make sense in their locale.

A person generated in ja_JP will have a Japanese name, a Tokyo address,
a Japanese phone number, and a Japanese bank account. Everything coheres.
"""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass, field
from typing import Optional

from fabrikate.context import Context
from fabrikate.locales import get_locale


@dataclass
class Address:
    street: str
    city: str
    postal_code: str
    country: str

    def __str__(self) -> str:
        return f"{self.street}, {self.city} {self.postal_code}, {self.country}"


@dataclass
class Person:
    """
    A contextually coherent person.

    All attributes are consistent with the context's locale — names, address,
    phone, email, and bank are all from the same cultural context.
    """

    id: str = ""
    first_name: str = ""
    last_name: str = ""
    full_name: str = ""
    gender: str = ""
    age: int = 0
    email: str = ""
    phone: str = ""
    address: Optional[Address] = None
    bank: str = ""
    company_id: Optional[str] = None
    _ctx: Optional[Context] = field(default=None, repr=False)

    @classmethod
    def generate(cls, ctx: Context, **overrides) -> Person:
        """
        Generate a coherent person within the given context.

        Parameters
        ----------
        ctx : Context
            The generation context (determines locale, seed, etc.)
        **overrides
            Override any generated field, e.g. gender="female", age=30.
        """
        locale = get_locale(ctx.locale)
        rng = ctx._rng

        person = cls(_ctx=ctx)
        person.id = overrides.get("id", str(uuid.UUID(int=rng.getrandbits(128))))

        # Gender
        person.gender = overrides.get("gender", rng.choice(["male", "female"]))

        # Name — culturally appropriate
        if person.gender == "male":
            person.first_name = overrides.get(
                "first_name", rng.choice(locale.first_names_male)
            )
        else:
            person.first_name = overrides.get(
                "first_name", rng.choice(locale.first_names_female)
            )
        person.last_name = overrides.get("last_name", rng.choice(locale.last_names))

        if locale.name_order == "family_given":
            person.full_name = f"{person.last_name} {person.first_name}"
        else:
            person.full_name = f"{person.first_name} {person.last_name}"

        # Age — reasonable working age by default
        person.age = overrides.get("age", rng.randint(22, 65))

        # Phone — locale format
        person.phone = _format_pattern(locale.phone_format, rng)

        # Address — locale city, street format, postal code
        city = rng.choice(locale.cities)
        street_names = _get_street_names(ctx.country_code)
        street_fmt = rng.choice(locale.street_formats)
        street = street_fmt.format(
            number=rng.randint(1, 9999),
            name=rng.choice(street_names),
            city=city,
            ward=rng.choice(_DISTRICTS.get(ctx.country_code, {}).get("wards", ["Central"])),
            district=rng.choice(_DISTRICTS.get(ctx.country_code, {}).get("districts", ["Central"])),
        )
        postal = _format_postal(locale.postal_code_format, rng)
        person.address = Address(
            street=street,
            city=city,
            postal_code=postal,
            country=locale.country_name,
        )

        # Email — derived from name for coherence
        name_part = (
            f"{_romanize(person.first_name)}.{_romanize(person.last_name)}"
            .lower()
            .replace(" ", "")
        )
        domain = rng.choice(locale.email_domains)
        person.email = overrides.get("email", f"{name_part}@{domain}")

        # Bank — locale appropriate
        person.bank = overrides.get("bank", rng.choice(locale.banks))

        # Company link
        person.company_id = overrides.get("company_id", None)

        ctx.register(person)
        return person

    def to_dict(self) -> dict:
        """Export as a plain dictionary (useful for JSON serialization)."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "gender": self.gender,
            "age": self.age,
            "email": self.email,
            "phone": self.phone,
            "address": str(self.address) if self.address else None,
            "bank": self.bank,
            "company_id": self.company_id,
        }


def _format_pattern(pattern: str, rng) -> str:
    """Replace '#' with random digits in a pattern like '###-####'."""
    return "".join(
        str(rng.randint(0, 9)) if c == "#" else c for c in pattern
    )


def _format_postal(pattern: str, rng) -> str:
    """
    Format postal codes. '#' becomes a digit, '?' becomes an uppercase letter.
    Handles UK-style '??# #??' and standard numeric formats.
    """
    result = []
    for c in pattern:
        if c == "#":
            result.append(str(rng.randint(0, 9)))
        elif c == "?":
            result.append(chr(rng.randint(65, 90)))  # A-Z
        else:
            result.append(c)
    return "".join(result)


def _romanize(text: str) -> str:
    """
    Simple romanization — strips non-ASCII and returns a usable slug.
    For Japanese/Korean names, we use the romanized version if available.
    """
    ascii_chars = [c for c in text if ord(c) < 128 and c.isalpha()]
    if ascii_chars:
        return "".join(ascii_chars)
    # Fallback: use a hash-based slug for non-latin scripts
    h = hashlib.md5(text.encode()).hexdigest()[:8]
    return f"user{h}"


# --- Locale-specific street names ---

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
    "JP": {
        "wards": ["中央", "港", "新宿", "渋谷", "千代田", "品川", "目黒", "世田谷"],
        "districts": ["本町", "元町", "旭町", "栄町", "幸町", "緑町"],
    },
    "KR": {
        "wards": ["강남", "서초", "마포", "영등포", "종로", "용산", "송파", "강서"],
        "districts": ["역삼", "삼성", "논현", "신사", "청담", "대치"],
    },
    "SA": {
        "wards": ["العليا", "السلامة", "النزهة", "الروضة", "المروج"],
        "districts": ["الورود", "الملز", "السليمانية", "الربوة", "المرسلات"],
    },
    "IN": {
        "wards": ["Andheri", "Bandra", "Koramangala", "Whitefield", "Salt Lake", "T Nagar", "Jubilee Hills"],
        "districts": ["Sector 5", "Block A", "Phase 2", "Extension", "Layout", "Nagar"],
    },
}


def _get_street_names(country_code: str) -> list[str]:
    """Get locale-appropriate street names, falling back to generic English."""
    return _STREET_NAMES.get(country_code, _STREET_NAMES["US"])
