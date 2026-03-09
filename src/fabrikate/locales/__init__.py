"""
Locale-specific data for coherent mock generation.

Each locale contains names, addresses, phone formats, banks, and other
culturally-appropriate data. This is what makes fabrikate different from
random generators — everything stays consistent within a locale.

v0.2.0: Expanded to ~100 names per gender per locale (200+ names total).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from importlib import import_module


@dataclass
class LocaleData:
    first_names_male: list[str] = field(default_factory=list)
    first_names_female: list[str] = field(default_factory=list)
    last_names: list[str] = field(default_factory=list)
    name_order: str = "given_family"  # or "family_given"
    cities: list[str] = field(default_factory=list)
    street_formats: list[str] = field(default_factory=list)
    postal_code_format: str = "#####"
    phone_format: str = "+1 (###) ###-####"
    currency: str = "USD"
    currency_symbol: str = "$"
    banks: list[str] = field(default_factory=list)
    email_domains: list[str] = field(default_factory=list)
    company_suffixes: list[str] = field(default_factory=list)
    country_name: str = "United States"


def _load_locale(module_name: str) -> LocaleData:
    """Load a LocaleData from a data module."""
    mod = import_module(f"fabrikate.locales.data.{module_name}")
    return LocaleData(
        first_names_male=mod.FIRST_NAMES_MALE,
        first_names_female=mod.FIRST_NAMES_FEMALE,
        last_names=mod.LAST_NAMES,
        name_order=getattr(mod, "NAME_ORDER", "given_family"),
        cities=mod.CITIES,
        street_formats=mod.STREET_FORMATS,
        postal_code_format=mod.POSTAL_CODE_FORMAT,
        phone_format=mod.PHONE_FORMAT,
        currency=mod.CURRENCY,
        currency_symbol=mod.CURRENCY_SYMBOL,
        banks=mod.BANKS,
        email_domains=mod.EMAIL_DOMAINS,
        company_suffixes=mod.COMPANY_SUFFIXES,
        country_name=mod.COUNTRY_NAME,
    )


# Supported locale codes mapped to their data module names
_LOCALE_MODULES = {
    "en_US": "en_US",
    "ja_JP": "ja_JP",
    "de_DE": "de_DE",
    "pt_BR": "pt_BR",
    "hi_IN": "hi_IN",
    "en_GB": "en_GB",
    "fr_FR": "fr_FR",
    "ko_KR": "ko_KR",
    "es_ES": "es_ES",
    "ar_SA": "ar_SA",
    "en_NG": "en_NG",
}

# Cache loaded locales
_cache: dict[str, LocaleData] = {}


def get_locale(code: str) -> LocaleData:
    """Get locale data, falling back to en_US for unknown locales."""
    if code in _cache:
        return _cache[code]

    if code in _LOCALE_MODULES:
        locale = _load_locale(_LOCALE_MODULES[code])
        _cache[code] = locale
        return locale

    # Try matching just the language part
    lang = code.split("_")[0] if "_" in code else code
    for key, mod_name in _LOCALE_MODULES.items():
        if key.startswith(lang):
            locale = _load_locale(mod_name)
            _cache[code] = locale
            return locale

    # Fallback
    return get_locale("en_US")


def supported_locales() -> list[str]:
    """Return list of all supported locale codes."""
    return list(_LOCALE_MODULES.keys())
