from inkwell.model import parse_invoice
from inkwell.vat import REVERSE_CHARGE_NOTE, is_cross_border_b2b, resolve_line_vat

DOMESTIC = {
    "number": "2026-0101",
    "issue_date": "2026-06-02",
    "client": {"name": "Acme BV", "country": "NL"},
    "lines": [
        {"description": "Consulting", "quantity": 1, "unit_price": 850, "vat_rate": 0.21}
    ],
}

CROSS_BORDER = {
    "number": "2026-0102",
    "issue_date": "2026-06-03",
    "client": {"name": "Brandt GmbH", "country": "DE", "vat_number": "DE814152300"},
    "lines": [
        {"description": "Workshop", "quantity": 2, "unit_price": 1400, "vat_rate": 0.19}
    ],
}


def test_cross_border_detection():
    assert is_cross_border_b2b("DE", "NL", "DE814152300")
    assert not is_cross_border_b2b("NL", "NL", "NL123")
    assert not is_cross_border_b2b("DE", "NL", None)


def test_reverse_charge_zeroes_rate_and_notes():
    invoice = parse_invoice(CROSS_BORDER, seller_country="NL")
    assert invoice.lines[0].vat_rate == 0.0
    assert REVERSE_CHARGE_NOTE in invoice.notes
    assert invoice.total_gross == invoice.total_net


def test_domestic_rate_charged():
    invoice = parse_invoice(DOMESTIC, seller_country="NL")
    assert invoice.lines[0].vat_rate == 0.21
    assert invoice.total_vat == round(850 * 0.21, 2)


def test_resolve_line_vat_domestic():
    assert resolve_line_vat({"vat_rate": 0.09}, False) == (0.09, "")
