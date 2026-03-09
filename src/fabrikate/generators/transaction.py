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


TRANSACTION_TYPES = ["purchase", "refund", "subscription", "transfer", "payment"]
STATUSES = ["completed", "pending", "failed", "cancelled"]


@dataclass
class Transaction:
    """A financial transaction linked to people, companies, and products."""

    id: str = ""
    type: str = ""
    amount: float = 0.0
    currency: str = ""
    status: str = ""
    date: str = ""
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

        tx = cls(_ctx=ctx)
        tx.id = overrides.get("id", str(uuid.UUID(int=rng.getrandbits(128))))

        tx.type = overrides.get("type", rng.choice(TRANSACTION_TYPES))
        tx.status = overrides.get(
            "status",
            rng.choices(
                STATUSES,
                weights=[70, 15, 10, 5],  # mostly completed
            )[0],
        )

        # Amount — realistic for the transaction type
        if tx.type == "subscription":
            tx.amount = round(rng.uniform(4.99, 99.99), 2)
        elif tx.type == "refund":
            tx.amount = -round(rng.uniform(5.0, 500.0), 2)
        else:
            tx.amount = round(rng.uniform(1.0, 5000.0), 2)
        tx.amount = overrides.get("amount", tx.amount)

        tx.currency = locale.currency
        tx.sender_id = sender_id
        tx.receiver_id = receiver_id
        tx.product_id = product_id

        # Date — within the context year
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
            "currency": self.currency,
            "status": self.status,
            "date": self.date,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "product_id": self.product_id,
            "description": self.description,
        }
