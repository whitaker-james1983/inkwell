from inkwell.model import parse_invoice
from inkwell.render import render_invoice

DATA = {
    "number": "2026-0002",
    "issue_date": "2026-01-12",
    "client": {"name": "Acme & Sons"},
    "lines": [{"description": "Workshop", "quantity": 1, "unit_price": 1400, "vat_rate": 0.21}],
}


def test_render_contains_client_and_number():
    out = render_invoice(parse_invoice(DATA))
    assert "Acme &amp; Sons" in out
    assert "2026-0002" in out


def test_render_contains_total():
    assert "1,400.00 EUR" in render_invoice(parse_invoice(DATA))
