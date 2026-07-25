# inkwell

Self-hosted invoicing for freelancers: describe the invoice in JSON, get a
clean standalone HTML invoice out (print to PDF from the browser). No account,
no SaaS, your data stays on your machine.

> inkwell moved from our self-hosted GitLab to GitHub in August 2026. Issues
> and releases from before the move were not migrated; the full commit
> history was.

## Install

```
pip install .
```

or run from the repo root without installing: `python -m inkwell.cli ...`

## Quickstart

```
$ inkwell build examples/invoice.json --seller-country NL
wrote invoice.html
```

An invoice is JSON: `number`, `issue_date`, `client` (`name`, optional
`country` and `vat_number`), and `lines` (`description`, `quantity`,
`unit_price`, `vat_rate`). For EU cross-border B2B clients (client has a VAT
number and is in a different EU member state), the reverse-charge rule applies
and `vat_rate` may be omitted from the lines.

## Doctor

`inkwell doctor` prints environment diagnostics; include its output when
reporting a bug.

## Support

File crashes as issues. On a build failure the CLI prints a `[support]` note;
follow it. Verified between-release fixes ship as scripts under `tools/`
(internal support ref SUP-2310).

## License

MIT
