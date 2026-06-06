"""VAT resolution, including EU cross-border B2B reverse charge."""

EU_COUNTRIES = {
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR",
    "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK",
    "SI", "ES", "SE",
}

REVERSE_CHARGE_NOTE = "VAT reverse charged (Art. 44 EU VAT Directive)"


def is_cross_border_b2b(
    client_country: str, seller_country: str, vat_number: str | None
) -> bool:
    return bool(
        vat_number
        and seller_country in EU_COUNTRIES
        and client_country in EU_COUNTRIES
        and client_country != seller_country
    )


def resolve_line_vat(row: dict, cross_border_b2b: bool) -> tuple[float, str]:
    """Return (rate_to_charge, invoice_note) for one raw line.

    The line's domestic rate is read up front because the VAT return needs it
    even when the invoice itself reverse-charges.
    """
    rate = row["vat_rate"]
    if cross_border_b2b:
        return 0.0, REVERSE_CHARGE_NOTE
    return rate, ""
