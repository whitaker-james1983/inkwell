"""Invoice data model."""

from dataclasses import dataclass, field


@dataclass
class Line:
    description: str
    quantity: float
    unit_price: float

    @property
    def net(self) -> float:
        return round(self.quantity * self.unit_price, 2)


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
    note: str = ""

    @property
    def total_net(self) -> float:
        return round(sum(line.net for line in self.lines), 2)


def parse_invoice(data: dict) -> Invoice:
    client = Client(
        name=data["client"]["name"],
        country=data["client"].get("country", ""),
        vat_number=data["client"].get("vat_number"),
    )
    lines = [
        Line(
            description=row["description"],
            quantity=float(row["quantity"]),
            unit_price=float(row["unit_price"]),
        )
        for row in data["lines"]
    ]
    return Invoice(
        number=data["number"],
        issue_date=data["issue_date"],
        client=client,
        lines=lines,
        currency=data.get("currency", "EUR"),
        note=data.get("note", ""),
    )
