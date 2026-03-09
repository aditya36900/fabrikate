"""
fabrikate — Contextually coherent mock data generation.

Unlike random fake data, fabrikate generates data that makes sense together.
A person in Tokyo gets a Japanese name, address, phone format, and bank.
A company's employees, products, and transactions are internally consistent.
"""

__version__ = "0.2.1"

from fabrikate.context import Context
from fabrikate.world import World
from fabrikate.generators.person import Person
from fabrikate.generators.company import Company
from fabrikate.generators.transaction import Transaction
from fabrikate.generators.product import Product

__all__ = [
    "Context",
    "World",
    "Person",
    "Company",
    "Transaction",
    "Product",
]
