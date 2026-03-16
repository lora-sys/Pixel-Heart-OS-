"""Example test file to verify pytest setup works."""

import pytest


def test_example_pass():
    """Example test that should always pass."""
    assert 1 + 1 == 2


def test_example_fail():
    """Example test that should fail (for testing test setup)."""
    # This intentionally fails to verify test framework catches it
    # assert False, "This test should fail"
    pass


@pytest.mark.parametrize(
    "input_val,expected",
    [
        (1, 1),
        (2, 4),
        (3, 9),
    ],
)
def test_parametrized_example(input_val, expected):
    """Example parametrized test."""
    assert input_val**2 == expected
