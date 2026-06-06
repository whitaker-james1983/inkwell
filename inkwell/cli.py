"""inkwell command line: build invoices, print diagnostics."""

import argparse
import json
import platform

from inkwell import __version__
from inkwell.model import parse_invoice
from inkwell.render import render_invoice


def _build(args: argparse.Namespace) -> int:
    with open(args.invoice, encoding="utf-8") as fh:
        data = json.load(fh)
    invoice = parse_invoice(data, seller_country=args.seller_country)
    html = render_invoice(invoice)
    out = args.out or "invoice.html"
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"wrote {out}")
    return 0


def _doctor(_args: argparse.Namespace) -> int:
    print(f"inkwell: {__version__}")
    print(f"python: {platform.python_version()}")
    print(f"platform: {platform.platform()}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="inkwell")
    sub = parser.add_subparsers(dest="command", required=True)

    build = sub.add_parser("build", help="build an HTML invoice from JSON")
    build.add_argument("invoice", help="path to the invoice JSON")
    build.add_argument("--seller-country", default="NL")
    build.add_argument("--out", help="output path (default: invoice.html)")
    build.set_defaults(func=_build)

    doctor = sub.add_parser("doctor", help="print environment diagnostics")
    doctor.set_defaults(func=_doctor)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
