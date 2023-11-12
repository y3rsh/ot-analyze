import pytest
from ot_simulate import simulate

import test_data.data as td


@pytest.mark.skip(reason="Not implementing simulate yet.")
def test_simulate_ot2_positive():
    simulate(td.POSITIVE_OT2)


@pytest.mark.skip(reason="Not implementing simulate yet.")
def test_simulate_flex_positive():
    simulate(td.POSITIVE_FLEX)
