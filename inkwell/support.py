"""Support helpers: what to tell users when a build crashes."""

SUPPORT_REF = "SUP-2310"


def crash_note() -> str:
    """One-line note printed to stderr when a build fails."""
    return (
        "crashes are diagnosed with `inkwell doctor`: run it and follow the "
        f"instructions it prints (ref {SUPPORT_REF})"
    )
