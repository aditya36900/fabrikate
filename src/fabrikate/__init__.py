"""
fabrikate — Contextually coherent mock data generation.

Unlike random fake data, fabrikate generates data that makes sense together.
A person in Tokyo gets a Japanese name, address, phone format, and bank.
A company's employees, products, and transactions are internally consistent.
"""

__version__ = "0.3.0"

from fabrikate.context import Context
from fabrikate.world import World
from fabrikate.generators.person import Person, Address, Education, Vehicle, MedicalRecord
from fabrikate.generators.company import Company
from fabrikate.generators.transaction import Transaction
from fabrikate.generators.product import Product
from fabrikate.locales import supported_locales

__all__ = [
    "Context",
    "World",
    "Person",
    "Address",
    "Education",
    "Vehicle",
    "MedicalRecord",
    "Company",
    "Transaction",
    "Product",
    "supported_locales",
]
