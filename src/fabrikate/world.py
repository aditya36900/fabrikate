"""
World — the high-level API for generating entire coherent datasets.

A World is a self-contained universe of mock data. Create a world,
add companies and people, and everything stays internally consistent.

    world = World(locale="ja_JP", seed=42)
    company = world.company(industry="tech")
    employees = company.hire(10)
    products = world.products(5, company=company)
    transactions = world.transactions(100)
"""

from __future__ import annotations

import json
from typing import Optional

from fabrikate.context import Context
from fabrikate.generators.company import Company
from fabrikate.generators.person import Person
from fabrikate.generators.product import Product
from fabrikate.generators.transaction import Transaction


class World:
    """
    A coherent mock data universe.

    Parameters
    ----------
    locale : str
        Locale code (e.g., "ja_JP", "en_US", "de_DE", "pt_BR").
    seed : int or None
        Random seed for full reproducibility.
    year : int
        Reference year for dates and ages.
    industry : str or None
        Default industry for companies/products.
    """

    def __init__(
        self,
        locale: str = "en_US",
        seed: Optional[int] = None,
        year: int = 2025,
        industry: Optional[str] = None,
    ):
        self.ctx = Context(
            locale=locale,
            seed=seed,
            year=year,
            industry=industry,
        )

    def person(self, **overrides) -> Person:
        """Generate a single coherent person."""
        return Person.generate(self.ctx, **overrides)

    def people(self, count: int, **overrides) -> list[Person]:
        """Generate multiple coherent people."""
        return [Person.generate(self.ctx, **overrides) for _ in range(count)]

    def company(self, **overrides) -> Company:
        """Generate a single coherent company."""
        return Company.generate(self.ctx, **overrides)

    def companies(self, count: int, **overrides) -> list[Company]:
        """Generate multiple coherent companies."""
        return [Company.generate(self.ctx, **overrides) for _ in range(count)]

    def product(
        self,
        company: Optional[Company] = None,
        **overrides,
    ) -> Product:
        """Generate a product, optionally tied to a company."""
        return Product.generate(
            self.ctx,
            company_id=company.id if company else None,
            industry=company.industry if company else None,
            **overrides,
        )

    def products(
        self,
        count: int,
        company: Optional[Company] = None,
        **overrides,
    ) -> list[Product]:
        """Generate multiple products."""
        return [self.product(company=company, **overrides) for _ in range(count)]

    def transaction(
        self,
        sender: Optional[Person] = None,
        receiver: Optional[Person | Company] = None,
        product: Optional[Product] = None,
        **overrides,
    ) -> Transaction:
        """Generate a transaction between entities."""
        return Transaction.generate(
            self.ctx,
            sender_id=sender.id if sender else None,
            receiver_id=receiver.id if receiver else None,
            product_id=product.id if product else None,
            **overrides,
        )

    def transactions(
        self,
        count: int,
        sender: Optional[Person] = None,
        receiver: Optional[Person | Company] = None,
        **overrides,
    ) -> list[Transaction]:
        """Generate multiple transactions."""
        return [
            self.transaction(sender=sender, receiver=receiver, **overrides)
            for _ in range(count)
        ]

    def dataset(self) -> dict:
        """
        Export all registered entities as a structured dictionary.

        Useful for dumping the entire world to JSON for test fixtures.
        """
        people = [e.to_dict() for e in self.ctx.find(Person)]
        companies = [e.to_dict() for e in self.ctx.find(Company)]
        products = [e.to_dict() for e in self.ctx.find(Product)]
        txns = [e.to_dict() for e in self.ctx.find(Transaction)]

        return {
            "metadata": {
                "locale": self.ctx.locale,
                "seed": self.ctx.seed,
                "year": self.ctx.year,
                "industry": self.ctx.industry,
            },
            "people": people,
            "companies": companies,
            "products": products,
            "transactions": txns,
        }

    def to_json(self, indent: int = 2) -> str:
        """Export the entire world as a JSON string."""
        return json.dumps(self.dataset(), indent=indent, ensure_ascii=False)
