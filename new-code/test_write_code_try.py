
import pytest
from write_code_try import standard_deviation  # Absolute import of the function to test

def test_empty_list():
    """Test standard deviation with an empty list."""
    assert standard_deviation([]) == 0

def test_single_element():
    """Test standard deviation with a single element."""
    assert standard_deviation([5]) == 0

def test_multiple_elements():
    """Test standard deviation with multiple elements."""
    data = [1, 2, 3, 4, 5]
    assert pytest.approx(standard_deviation(data), 0.0001) == 1.4142135623730951

def test_identical_elements():
    """Test standard deviation with identical elements."""
    data = [7, 7, 7, 7, 7]
    assert standard_deviation(data) == 0

def test_real_numbers():
    """Test standard deviation with real numbers."""
    data = [10, 12, 23, 23, 16, 23, 21, 16]
    assert pytest.approx(standard_deviation(data), 0.0001) == 4.898979485566356

def test_negative_numbers():
    """Test standard deviation with negative numbers."""
    data = [-5, -10, -15]
    assert pytest.approx(standard_deviation(data), 0.0001) == 4.08248290463863