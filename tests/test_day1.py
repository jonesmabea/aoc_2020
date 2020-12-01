import pytest
from src.util import arr_sum


@pytest.mark.parametrize("test_input, test_expected", [([1,2,3],6)])
def test_arr_sum(test_input, test_expected):
    assert arr_sum(test_input) == test_expected
