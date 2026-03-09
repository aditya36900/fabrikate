"""
Transaction generator — creates financial transactions between
entities that make sense: correct currency, realistic amounts,
proper date ranges, and references to existing people/companies.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

from fabrikate.context import Context
from fabrikate.locales import get_locale
from fabrikate.distributions import log_normal_float, weighted_choice
from fabrikate.reference_data import PAYMENT_METHODS


TRANSACTION_TYPES = ["purchase", "refund", "subscription", "transfer", "payment", "invoice"]
STATUSES = ["completed", "pending", "failed", "cancelled"]

# Tax rates by country (approximate standard rates)
TAX_RATES: dict[str, float] = {
    "US": 0.08, "JP": 0.10, "DE": 0.19, "BR": 0.17, "IN": 0.18,
    "GB": 0.20, "FR": 0.20, "KR": 0.10, "ES": 0.21, "SA": 0.15, "NG": 0.075,
}


@dataclass
class Transaction:
    """A financial transaction with payment method, tax, and invoice."""

    id: str = ""
    type: str = ""
    amount: float = 0.0
    tax_amount: float = 0.0
    total_amount: float = 0.0
    currency: str = ""
    status: str = ""
    date: str = ""
    payment_method: str = ""
    invoice_number: str = ""
    sender_id: Optional[str] = None
    receiver_id: Optional[str] = None
    product_id: Optional[str] = None
    description: str = ""
    _ctx: Optional[Context] = field(default=None, repr=False)

    @classmethod
    def generate(
        cls,
        ctx: Context,
        sender_id: Optional[str] = None,
        receiver_id: Optional[str] = None,
        product_id: Optional[str] = None,
        **overrides,
    ) -> Transaction:
        locale = get_locale(ctx.locale)
        rng = ctx._rng
        cc = ctx.country_code

        tx = cls(_ctx=ctx)
        tx.id = overrides.get("id", str(uuid.UUID(int=rng.getrandbits(128))))

        tx.type = overrides.get("type", rng.choice(TRANSACTION_TYPES))
        tx.status = overrides.get(
            "status",
            rng.choices(STATUSES, weights=[70, 15, 10, 5])[0],
        )

        # Amount — log-normal (many small, few large)
        if tx.type == "subscription":
            tx.amount = round(log_normal_float(rng, 15.0, sigma=0.7, low=4.99, high=99.99), 2)
        elif tx.type == "refund":
            tx.amount = -round(log_normal_float(rng, 50.0, sigma=0.8, low=5.0, high=500.0), 2)
        else:
            tx.amount = round(log_normal_float(rng, 120.0, sigma=1.0, low=1.0, high=10000.0), 2)
        tx.amount = overrides.get("amount", tx.amount)

        # Tax
        tax_rate = TAX_RATES.get(cc, 0.10)
        tx.tax_amount = overrides.get("tax_amount", round(abs(tx.amount) * tax_rate, 2))
        tx.total_amount = round(tx.amount + (tx.tax_amount if tx.amount > 0 else -tx.tax_amount), 2)

        tx.currency = locale.currency
        tx.sender_id = sender_id
        tx.receiver_id = receiver_id
        tx.product_id = product_id

        # Payment method — locale-weighted
        pm_data = PAYMENT_METHODS.get(cc, PAYMENT_METHODS["US"])
        pm_items = [p[0] for p in pm_data]
        pm_weights = [p[1] for p in pm_data]
        tx.payment_method = overrides.get("payment_method", weighted_choice(rng, pm_items, pm_weights))

        # Invoice number
        tx.invoice_number = overrides.get(
            "invoice_number",
            f"INV-{ctx.year}-{rng.randint(10000, 99999)}",
        )

        # Date
        base = datetime(ctx.year, 1, 1)
        offset = timedelta(days=rng.randint(0, 364))
        tx.date = overrides.get("date", (base + offset).strftime("%Y-%m-%d"))

        tx.description = overrides.get(
            "description",
            f"{tx.type.title()} — {locale.currency_symbol}{abs(tx.amount):.2f}",
        )

        ctx.register(tx)
        return tx

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "amount": self.amount,
            "tax_amount": self.tax_amount,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "status": self.status,
            "date": self.date,
            "payment_method": self.payment_method,
            "invoice_number": self.invoice_number,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "product_id": self.product_id,
            "description": self.description,
        }
