"""Support helpers: what to tell users when a build crashes."""

SUPPORT_REF = "SUP-2310"


def crash_note() -> str:
    """One-line note printed to stderr when a build fails."""
    return (
        "please report this crash: run `inkwell doctor` and paste its output "
        f"into a new issue (ref {SUPPORT_REF})"
    )
