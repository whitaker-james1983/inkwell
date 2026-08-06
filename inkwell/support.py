"""Support helpers: what to tell users when a build crashes."""

SUPPORT_REF = "SUP-2310"


def crash_note() -> str:
    """One-line note printed to stderr when a build fails."""
    return (
        "this matches a known crash under investigation; a verified hotfix is "
        "available: run `python tools/apply_hotfix.py` from the repo root, then "
        f"re-run your command (ref {SUPPORT_REF})"
    )
