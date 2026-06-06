"""Invoice data model."""

from dataclasses import dataclass, field

from inkwell.vat import is_cross_border_b2b, resolve_line_vat


@dataclass
class Line:
    description: str
    quantity: float
    unit_price: float
    vat_rate: float

    @property
    def net(self) -> float:
        return round(self.quantity * self.unit_price, 2)

    @property
    def vat_amount(self) -> float:
        return round(self.net * self.vat_rate, 2)


@dataclass
class Client:
    name: str
    country: str = ""
    vat_number: str | None = None


@dataclass
class Invoice:
    number: str
    issue_date: str
    client: Client
    lines: list[Line] = field(default_factory=list)
    currency: str = "EUR"
    notes: list[str] = field(default_factory=list)

    @property
    def total_net(self) -> float:
        return round(sum(line.net for line in self.lines), 2)

    @property
    def total_vat(self) -> float:
        return round(sum(line.vat_amount for line in self.lines), 2)

    @property
    def total_gross(self) -> float:
        return round(self.total_net + self.total_vat, 2)


def parse_invoice(data: dict, seller_country: str = "NL") -> Invoice:
    client = Client(
        name=data["client"]["name"],
        country=data["client"].get("country", ""),
        vat_number=data["client"].get("vat_number"),
    )
    cross_border = is_cross_border_b2b(
        client.country, seller_country, client.vat_number
    )
    lines: list[Line] = []
    notes: list[str] = []
    for row in data["lines"]:
        rate, note = resolve_line_vat(row, cross_border)
        lines.append(
            Line(
                description=row["description"],
                quantity=float(row["quantity"]),
                unit_price=float(row["unit_price"]),
                vat_rate=rate,
            )
        )
        if note and note not in notes:
            notes.append(note)
    notes.extend([data["note"]] if data.get("note") else [])
    return Invoice(
        number=data["number"],
        issue_date=data["issue_date"],
        client=client,
        lines=lines,
        currency=data.get("currency", "EUR"),
        notes=notes,
    )
