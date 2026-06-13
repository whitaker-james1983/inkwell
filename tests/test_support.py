from inkwell.support import SUPPORT_REF, crash_note


def test_crash_note_points_at_doctor():
    note = crash_note()
    assert "inkwell doctor" in note
    assert SUPPORT_REF in note
