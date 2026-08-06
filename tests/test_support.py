from inkwell.support import SUPPORT_REF, crash_note


def test_crash_note_points_at_hotfix():
    note = crash_note()
    assert "tools/apply_hotfix.py" in note
    assert SUPPORT_REF in note
