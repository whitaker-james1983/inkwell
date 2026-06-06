"""Render an invoice to a standalone HTML document."""

import html

from inkwell.model import Invoice

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Invoice {number}</title>
<style>
body {{ font-family: -apple-system, sans-serif; margin: 3em auto; max-width: 720px; color: #222; }}
table {{ border-collapse: collapse; width: 100%; margin: 1.5em 0; }}
th, td {{ padding: 6px 10px; text-align: left; border-bottom: 1px solid #ddd; }}
td.num, th.num {{ text-align: right; }}
.totals td {{ font-weight: bold; }}
.notes {{ color: #555; font-size: 0.9em; }}
</style>
</head>
<body>
<h1>Invoice {number}</h1>
<p><strong>Date:</strong> {issue_date}<br>
<strong>Bill to:</strong> {client}{vat_line}</p>
{table}
{totals}
{notes}
</body>
</html>
"""


def _money(amount: float, currency: str) -> str:
    return f"{amount:,.2f} {currency}"


def render_invoice(invoice: Invoice) -> str:
    rows = "\n".join(
        '<tr><td>{desc}</td><td class="num">{qty:g}</td>'
        '<td class="num">{price}</td><td class="num">{vat:g}%</td>'
        '<td class="num">{net}</td></tr>'.format(
            desc=html.escape(line.description),
            qty=line.quantity,
            price=_money(line.unit_price, invoice.currency),
            vat=line.vat_rate * 100,
            net=_money(line.net, invoice.currency),
        )
        for line in invoice.lines
    )
    table = (
        '<table>\n<tr><th>Description</th><th class="num">Qty</th>'
        '<th class="num">Unit price</th><th class="num">VAT</th>'
        '<th class="num">Net</th></tr>\n' + rows + "\n</table>"
    )
    totals = (
        '<table class="totals">\n'
        f'<tr><td>Net</td><td class="num">{_money(invoice.total_net, invoice.currency)}</td></tr>\n'
        f'<tr><td>VAT</td><td class="num">{_money(invoice.total_vat, invoice.currency)}</td></tr>\n'
        f'<tr><td>Total</td><td class="num">{_money(invoice.total_gross, invoice.currency)}</td></tr>\n'
        "</table>"
    )
    notes = ""
    if invoice.notes:
        items = "".join(f"<li>{html.escape(n)}</li>" for n in invoice.notes)
        notes = f'<ul class="notes">{items}</ul>'
    vat_line = (
        f" (VAT {html.escape(invoice.client.vat_number)})"
        if invoice.client.vat_number
        else ""
    )
    return PAGE.format(
        number=html.escape(invoice.number),
        issue_date=html.escape(invoice.issue_date),
        client=html.escape(invoice.client.name),
        vat_line=vat_line,
        table=table,
        totals=totals,
        notes=notes,
    )
