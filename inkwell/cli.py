"""inkwell command line: build invoices from JSON."""

import argparse
import json

from inkwell.model import parse_invoice
from inkwell.render import render_invoice


def _build(args: argparse.Namespace) -> int:
    with open(args.invoice, encoding="utf-8") as fh:
        data = json.load(fh)
    invoice = parse_invoice(data)
    html = render_invoice(invoice)
    out = args.out or "invoice.html"
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"wrote {out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="inkwell")
    sub = parser.add_subparsers(dest="command", required=True)

    build = sub.add_parser("build", help="build an HTML invoice from JSON")
    build.add_argument("invoice", help="path to the invoice JSON")
    build.add_argument("--out", help="output path (default: invoice.html)")
    build.set_defaults(func=_build)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
