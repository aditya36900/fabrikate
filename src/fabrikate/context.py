"""
Context holds the shared state that keeps generated data coherent.

When you create a person in a context set to "Tokyo", everything about
that person — name, address, phone, bank — will be Japanese. When you
create a company, its employees inherit the company's context.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Context:
    """
    A generation context that ensures coherent mock data.

    Parameters
    ----------
    locale : str
        A locale code like "ja_JP", "en_US", "de_DE", "pt_BR".
        Controls names, addresses, phone formats, currencies, etc.
    seed : int or None
        Random seed for reproducibility. Same seed = same data every time.
    year : int
        The reference year for generating dates and ages.
    industry : str or None
        Industry context for companies and products (e.g., "tech", "finance").
    """

    locale: str = "en_US"
    seed: Optional[int] = None
    year: int = 2025
    industry: Optional[str] = None
    _rng: random.Random = field(default_factory=random.Random, repr=False)
    _entity_registry: list = field(default_factory=list, repr=False)

    def __post_init__(self):
        if self.seed is not None:
            self._rng.seed(self.seed)

    @property
    def country_code(self) -> str:
        """Extract country code from locale, e.g. 'ja_JP' -> 'JP'."""
        if "_" in self.locale:
            return self.locale.split("_")[1]
        return self.locale.upper()

    @property
    def language_code(self) -> str:
        """Extract language code from locale, e.g. 'ja_JP' -> 'ja'."""
        if "_" in self.locale:
            return self.locale.split("_")[0]
        return self.locale.lower()

    def child(self, **overrides) -> Context:
        """
        Create a child context that inherits settings but can override them.

        Useful when a company in Tokyo has a branch in New York — the branch
        gets a child context with locale="en_US" but shares the same seed
        progression.
        """
        params = {
            "locale": self.locale,
            "seed": None,  # child uses parent's rng progression
            "year": self.year,
            "industry": self.industry,
        }
        params.update(overrides)
        child_ctx = Context(**params)
        child_ctx._rng = self._rng  # share RNG for determinism
        return child_ctx

    def register(self, entity) -> None:
        """Register an entity so other generators can reference it."""
        self._entity_registry.append(entity)

    def find(self, entity_type: type, **filters) -> list:
        """
        Find registered entities by type and optional attribute filters.

        Example: ctx.find(Person, company_id=company.id)
        """
        results = [e for e in self._entity_registry if isinstance(e, entity_type)]
        for key, value in filters.items():
            results = [e for e in results if getattr(e, key, None) == value]
        return results
