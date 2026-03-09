"""
Company generator — creates companies with coherent employees,
products, and financial context.

A company inherits its locale context and passes it down to
any employees or products generated within it.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional

from fabrikate.context import Context
from fabrikate.locales import get_locale
from fabrikate.generators.person import Person


INDUSTRY_KEYWORDS = {
    "tech": ["Digital", "Cloud", "Data", "Cyber", "Net", "Quantum", "AI", "Logic"],
    "finance": ["Capital", "Trust", "Equity", "Asset", "Wealth", "Venture", "Harbor"],
    "health": ["Health", "Vita", "Med", "Bio", "Care", "Life", "Pharma", "Thera"],
    "retail": ["Market", "Store", "Shop", "Goods", "Trade", "Fresh", "Home"],
    "food": ["Fresh", "Harvest", "Kitchen", "Taste", "Green", "Farm", "Spice"],
    "manufacturing": ["Steel", "Forge", "Iron", "Works", "Craft", "Build", "Core"],
}

GENERIC_KEYWORDS = ["Global", "Prime", "Summit", "Atlas", "Apex", "Nova", "Arc"]


@dataclass
class Company:
    """
    A contextually coherent company.

    The company's name style, suffix, currency, and bank are locale-appropriate.
    Employees generated via `hire()` inherit the company's context.
    """

    id: str = ""
    name: str = ""
    industry: str = ""
    founded_year: int = 0
    employee_count: int = 0
    currency: str = ""
    bank: str = ""
    city: str = ""
    country: str = ""
    employees: list[Person] = field(default_factory=list)
    _ctx: Optional[Context] = field(default=None, repr=False)

    @classmethod
    def generate(cls, ctx: Context, **overrides) -> Company:
        """
        Generate a coherent company within the given context.

        Parameters
        ----------
        ctx : Context
            The generation context.
        **overrides
            Override any field: industry="tech", name="Acme Corp", etc.
        """
        locale = get_locale(ctx.locale)
        rng = ctx._rng

        company = cls(_ctx=ctx)
        company.id = overrides.get("id", str(uuid.UUID(int=rng.getrandbits(128))))

        # Industry
        company.industry = overrides.get("industry", ctx.industry or rng.choice(
            list(INDUSTRY_KEYWORDS.keys())
        ))

        # Company name — industry-appropriate + locale suffix
        keywords = INDUSTRY_KEYWORDS.get(company.industry, GENERIC_KEYWORDS)
        word1 = rng.choice(keywords)
        word2 = rng.choice(GENERIC_KEYWORDS)
        suffix = rng.choice(locale.company_suffixes)
        company.name = overrides.get("name", f"{word1}{word2} {suffix}")

        # Location
        company.city = overrides.get("city", rng.choice(locale.cities))
        company.country = locale.country_name

        # Financials
        company.currency = locale.currency
        company.bank = overrides.get("bank", rng.choice(locale.banks))
        company.founded_year = overrides.get(
            "founded_year", rng.randint(1970, ctx.year - 1)
        )
        company.employee_count = overrides.get(
            "employee_count", rng.choice([5, 12, 25, 50, 100, 250, 500, 1000])
        )

        ctx.register(company)
        return company

    def hire(self, count: int = 1, **person_overrides) -> list[Person]:
        """
        Generate employees that belong to this company.

        Employees inherit the company's context (locale, industry, etc.)
        and are linked to this company by ID.

        Parameters
        ----------
        count : int
            Number of employees to generate.
        **person_overrides
            Passed through to Person.generate().
        """
        new_employees = []
        for _ in range(count):
            person = Person.generate(
                self._ctx,
                company_id=self.id,
                **person_overrides,
            )
            new_employees.append(person)
            self.employees.append(person)
        return new_employees

    def to_dict(self) -> dict:
        """Export as a plain dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "industry": self.industry,
            "founded_year": self.founded_year,
            "employee_count": self.employee_count,
            "currency": self.currency,
            "bank": self.bank,
            "city": self.city,
            "country": self.country,
            "employees": [e.to_dict() for e in self.employees],
        }
