from inkwell.model import parse_invoice

DATA = {
    "number": "2026-0001",
    "issue_date": "2026-01-05",
    "client": {"name": "Acme BV"},
    "currency": "EUR",
    "lines": [
        {"description": "Consulting (day)", "quantity": 3, "unit_price": 850},
        {"description": "Expenses", "quantity": 1, "unit_price": 120.5},
    ],
}


def test_parse_builds_lines():
    invoice = parse_invoice(DATA)
    assert len(invoice.lines) == 2
    assert invoice.lines[0].net == 2550.0


def test_total_net():
    assert parse_invoice(DATA).total_net == 2670.5


def test_currency_defaults_to_eur():
    data = {k: v for k, v in DATA.items() if k != "currency"}
    assert parse_invoice(data).currency == "EUR"
