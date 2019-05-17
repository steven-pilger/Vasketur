import pytest

from vasketur.machinestate.utilities import (
    write_machine_state_to_db,
    extract_machine_state,
    parse_machine_state,
)


# @pytest.mark.django_db(transaction=True)
# def test_write_machine_state_to_db(fixture_machine_state):
#     rms = fixture_machine_state
#     ms = extract_machine_state(rms)
#     ms = parse_machine_state(ms)
#     res = write_machine_state_to_db(ms[0])
#     assert res[1] is True
