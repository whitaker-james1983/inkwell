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
</style>
</head>
<body>
<h1>Invoice {number}</h1>
<p><strong>Date:</strong> {issue_date}<br>
<strong>Bill to:</strong> {client}</p>
{table}
{totals}
</body>
</html>
"""


def _money(amount: float, currency: str) -> str:
    return f"{amount:,.2f} {currency}"


def render_invoice(invoice: Invoice) -> str:
    rows = "\n".join(
        '<tr><td>{desc}</td><td class="num">{qty:g}</td>'
        '<td class="num">{price}</td><td class="num">{net}</td></tr>'.format(
            desc=html.escape(line.description),
            qty=line.quantity,
            price=_money(line.unit_price, invoice.currency),
            net=_money(line.net, invoice.currency),
        )
        for line in invoice.lines
    )
    table = (
        '<table>\n<tr><th>Description</th><th class="num">Qty</th>'
        '<th class="num">Unit price</th><th class="num">Net</th></tr>\n'
        + rows
        + "\n</table>"
    )
    totals = (
        '<table>\n<tr><td><strong>Total</strong></td>'
        f'<td class="num"><strong>{_money(invoice.total_net, invoice.currency)}'
        "</strong></td></tr>\n</table>"
    )
    return PAGE.format(
        number=html.escape(invoice.number),
        issue_date=html.escape(invoice.issue_date),
        client=html.escape(invoice.client.name),
        table=table,
        totals=totals,
    )
