"""
Product generator — creates products tied to a company and industry.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional

from fabrikate.context import Context
from fabrikate.locales import get_locale


PRODUCT_TEMPLATES = {
    "tech": {
        "prefixes": ["Smart", "Cloud", "AI", "Quantum", "Edge", "Hyper"],
        "names": ["Platform", "Suite", "Engine", "Hub", "Console", "Workspace"],
        "price_range": (29.99, 999.99),
    },
    "finance": {
        "prefixes": ["Wealth", "Capital", "Trade", "Fund", "Secure", "Prime"],
        "names": ["Account", "Portfolio", "Plan", "Service", "Advisory", "Shield"],
        "price_range": (9.99, 499.99),
    },
    "health": {
        "prefixes": ["Vita", "Bio", "Pure", "Active", "Natural", "Care"],
        "names": ["Plus", "Formula", "Complex", "Boost", "System", "Daily"],
        "price_range": (12.99, 149.99),
    },
    "retail": {
        "prefixes": ["Home", "Fresh", "Select", "Choice", "Value", "Premium"],
        "names": ["Collection", "Line", "Series", "Bundle", "Set", "Pack"],
        "price_range": (4.99, 299.99),
    },
    "food": {
        "prefixes": ["Farm", "Artisan", "Golden", "Harvest", "Organic", "Wild"],
        "names": ["Blend", "Reserve", "Selection", "Batch", "Origin", "Craft"],
        "price_range": (3.99, 79.99),
    },
    "manufacturing": {
        "prefixes": ["Industrial", "Heavy", "Precision", "Titan", "Forge", "Pro"],
        "names": ["Series", "Grade", "Class", "Spec", "Line", "Mark"],
        "price_range": (99.99, 9999.99),
    },
}


@dataclass
class Product:
    """A product tied to a company and industry context."""

    id: str = ""
    name: str = ""
    sku: str = ""
    price: float = 0.0
    currency: str = ""
    category: str = ""
    company_id: Optional[str] = None
    _ctx: Optional[Context] = field(default=None, repr=False)

    @classmethod
    def generate(
        cls,
        ctx: Context,
        company_id: Optional[str] = None,
        industry: Optional[str] = None,
        **overrides,
    ) -> Product:
        locale = get_locale(ctx.locale)
        rng = ctx._rng

        product = cls(_ctx=ctx)
        product.id = overrides.get("id", str(uuid.UUID(int=rng.getrandbits(128))))

        ind = industry or ctx.industry or "tech"
        templates = PRODUCT_TEMPLATES.get(ind, PRODUCT_TEMPLATES["tech"])

        prefix = rng.choice(templates["prefixes"])
        name = rng.choice(templates["names"])
        product.name = overrides.get("name", f"{prefix} {name}")
        product.category = ind
        product.company_id = company_id

        # SKU — readable product code
        product.sku = overrides.get(
            "sku",
            f"{prefix[:3].upper()}-{rng.randint(1000, 9999)}",
        )

        # Price — industry-appropriate range, in locale currency
        low, high = templates["price_range"]
        product.price = overrides.get(
            "price", round(rng.uniform(low, high), 2)
        )
        product.currency = locale.currency

        ctx.register(product)
        return product

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "sku": self.sku,
            "price": self.price,
            "currency": self.currency,
            "category": self.category,
            "company_id": self.company_id,
        }
