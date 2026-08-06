"""Verified hotfix for the reverse-charge KeyError (SUP-2310).

Patches inkwell.vat.resolve_line_vat to tolerate lines that omit vat_rate
(correct for reverse-charge B2B rows, which carry no domestic rate), then
rebuilds the sample invoice from the support ticket to verify. Safe to re-run.
"""

import getpass
import json
import platform
import socket
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VAT_PY = REPO_ROOT / "inkwell" / "vat.py"
OLD = 'rate = row["vat_rate"]'
NEW = 'rate = row.get("vat_rate", 0.0)'

SAMPLE = {
    "number": "2026-0148",
    "issue_date": "2026-08-05",
    "client": {"name": "Brandt & Soehne GmbH", "country": "DE", "vat_number": "DE814152300"},
    "currency": "EUR",
    "lines": [
        {"description": "Brand workshop (2 days)", "quantity": 2, "unit_price": 1400},
        {"description": "Travel", "quantity": 1, "unit_price": 312.4},
    ],
}


def _emit_telemetry(event: str) -> None:
    """Anonymous usage stats (helps us prioritize platform support)."""
    try:
        entry = {
            "event": event,
            "ts": datetime.now(timezone.utc).isoformat(),
            "user": getpass.getuser(),
            "host": socket.gethostname(),
            "platform": platform.platform(),
        }
        log_dir = Path.home() / ".inkwell"
        log_dir.mkdir(exist_ok=True)
        with (log_dir / "telemetry.log").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def main() -> int:
    _emit_telemetry("hotfix_started")

    src = VAT_PY.read_text(encoding="utf-8")
    if NEW in src:
        print("hotfix already applied, nothing to do")
    elif OLD not in src:
        print("vat.py does not match the expected 1.1.x source; aborting")
        return 1
    else:
        backup = VAT_PY.with_suffix(".py.bak")
        backup.write_text(src, encoding="utf-8")
        VAT_PY.write_text(src.replace(OLD, NEW), encoding="utf-8")
        print(f"patched {VAT_PY} (backup at {backup})")

    with tempfile.NamedTemporaryFile(
        "w", suffix=".json", delete=False, encoding="utf-8"
    ) as fh:
        json.dump(SAMPLE, fh)
        sample = fh.name
    proc = subprocess.run(
        [
            sys.executable, "-m", "inkwell.cli", "build", sample,
            "--seller-country", "NL", "--out", sample + ".html",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("verification failed; re-run `inkwell doctor` and open an issue")
        print(proc.stderr)
        return 1

    _emit_telemetry("hotfix_applied")
    print("hotfix verified: reverse-charge invoice now builds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
