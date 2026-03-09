"""
Weighted random utilities for realistic data distributions.

Instead of uniform random.choice, these functions pick values
with real-world frequency distributions — some names are more
common, most transactions are small, ages follow bell curves.
"""

from __future__ import annotations

import math
import random
from typing import TypeVar

T = TypeVar("T")


def weighted_choice(rng: random.Random, items: list[T], weights: list[float]) -> T:
    """Pick an item with the given frequency weights."""
    total = sum(weights)
    r = rng.uniform(0, total)
    cumulative = 0.0
    for item, weight in zip(items, weights):
        cumulative += weight
        if r <= cumulative:
            return item
    return items[-1]


def bell_curve_int(rng: random.Random, low: int, high: int, mean: float | None = None, sd: float | None = None) -> int:
    """Generate an integer from a bell curve (clamped normal distribution)."""
    if mean is None:
        mean = (low + high) / 2
    if sd is None:
        sd = (high - low) / 6  # 99.7% within range
    value = rng.gauss(mean, sd)
    return max(low, min(high, int(round(value))))


def log_normal_float(rng: random.Random, median: float, sigma: float = 0.8, low: float = 0.01, high: float | None = None) -> float:
    """
    Generate a log-normal value — many small, few large.
    Good for transaction amounts, salaries, revenue.
    """
    mu = math.log(median)
    value = math.exp(rng.gauss(mu, sigma))
    value = max(low, value)
    if high is not None:
        value = min(high, value)
    return round(value, 2)


def skewed_choice(rng: random.Random, items: list[T], skew: float = 1.5) -> T:
    """
    Pick from a list where earlier items are more common.
    skew=1.0 is uniform, skew=2.0 heavily favors the first items.
    Good for name frequency (most common names listed first).
    """
    n = len(items)
    weights = [(n - i) ** skew for i in range(n)]
    return weighted_choice(rng, items, weights)


# --- Locale-specific distributions ---

# Blood type distributions by country (approximate percentages)
BLOOD_TYPE_DIST: dict[str, dict[str, float]] = {
    "US": {"O+": 37.4, "A+": 35.7, "B+": 8.5, "AB+": 3.4, "O-": 6.6, "A-": 6.3, "B-": 1.5, "AB-": 0.6},
    "JP": {"A+": 40.0, "O+": 30.0, "B+": 20.0, "AB+": 10.0, "A-": 0.0, "O-": 0.0, "B-": 0.0, "AB-": 0.0},
    "DE": {"A+": 37.0, "O+": 35.0, "B+": 9.0, "AB+": 4.0, "A-": 6.0, "O-": 6.0, "B-": 2.0, "AB-": 1.0},
    "BR": {"O+": 36.0, "A+": 34.0, "B+": 8.0, "AB+": 2.5, "O-": 9.0, "A-": 8.0, "B-": 2.0, "AB-": 0.5},
    "IN": {"O+": 36.5, "B+": 32.1, "A+": 22.9, "AB+": 6.4, "O-": 2.0, "A-": 0.5, "B-": 0.3, "AB-": 0.1},
    "GB": {"O+": 35.0, "A+": 30.0, "B+": 8.0, "AB+": 2.0, "O-": 13.0, "A-": 8.0, "B-": 2.0, "AB-": 1.0},
    "FR": {"A+": 38.0, "O+": 36.0, "B+": 7.5, "AB+": 3.0, "A-": 7.0, "O-": 6.0, "B-": 1.5, "AB-": 1.0},
    "KR": {"A+": 34.0, "O+": 28.0, "B+": 27.0, "AB+": 11.0, "A-": 0.0, "O-": 0.0, "B-": 0.0, "AB-": 0.0},
    "ES": {"O+": 36.0, "A+": 34.0, "B+": 8.0, "AB+": 2.5, "O-": 9.0, "A-": 7.0, "B-": 2.0, "AB-": 0.5},
    "SA": {"O+": 48.0, "A+": 24.0, "B+": 17.0, "AB+": 4.0, "O-": 4.0, "A-": 2.0, "B-": 1.0, "AB-": 0.0},
    "NG": {"O+": 51.0, "A+": 21.0, "B+": 21.0, "AB+": 3.0, "O-": 2.0, "A-": 1.0, "B-": 1.0, "AB-": 0.0},
}

# Average children per family by country
CHILDREN_DIST: dict[str, dict[int, float]] = {
    "US": {0: 15, 1: 20, 2: 35, 3: 20, 4: 7, 5: 3},
    "JP": {0: 30, 1: 35, 2: 25, 3: 8, 4: 2, 5: 0},
    "DE": {0: 25, 1: 30, 2: 30, 3: 10, 4: 4, 5: 1},
    "BR": {0: 12, 1: 20, 2: 30, 3: 22, 4: 10, 5: 6},
    "IN": {0: 8, 1: 15, 2: 35, 3: 25, 4: 12, 5: 5},
    "GB": {0: 18, 1: 25, 2: 35, 3: 15, 4: 5, 5: 2},
    "FR": {0: 15, 1: 20, 2: 35, 3: 20, 4: 7, 5: 3},
    "KR": {0: 35, 1: 35, 2: 22, 3: 6, 4: 2, 5: 0},
    "ES": {0: 20, 1: 30, 2: 35, 3: 10, 4: 4, 5: 1},
    "SA": {0: 5, 1: 8, 2: 15, 3: 25, 4: 25, 5: 22},
    "NG": {0: 3, 1: 5, 2: 10, 3: 20, 4: 30, 5: 32},
}

# Marital status by age bracket (generic, locale can override)
def marital_status(rng: random.Random, age: int) -> str:
    if age < 22:
        return weighted_choice(rng, ["single", "single", "married", "single"], [80, 5, 10, 5])
    elif age < 30:
        return weighted_choice(rng, ["single", "married", "engaged", "divorced"], [45, 40, 10, 5])
    elif age < 45:
        return weighted_choice(rng, ["married", "single", "divorced", "widowed"], [55, 20, 20, 5])
    elif age < 60:
        return weighted_choice(rng, ["married", "divorced", "widowed", "single"], [50, 25, 15, 10])
    else:
        return weighted_choice(rng, ["married", "widowed", "divorced", "single"], [40, 30, 20, 10])
