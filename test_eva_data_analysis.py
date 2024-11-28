import pytest

from src.eva_data_analysis import text_to_duration
from src.eva_data_analysis import calculate_crew_size

def test_text_to_duration_integer():
    """
    Test that text_to_duration() returns expected ground truth values
    for typical durations with only hours and zero minutes.
    """
    
    input_value = "10:00"
    expected_result = 10

    assert text_to_duration(input_value) == expected_result


def test_text_to_duration_float1():
    """
    Test that text_to_duration() returns expected ground truth values
    for typical durations with only hours and non-zero minutes,
    where minutes result in a .
    """
    
    input_value = "10:15"
    expected_result = 10.25

    assert text_to_duration(input_value) == expected_result


def test_text_to_duration_float2():
    """
    Test that ...
    """
    
    input_value = "10:20"
    expected_result = 10.33333333

    assert text_to_duration(input_value) == pytest.approx(expected_result) 


def test_calculate_crew_size_none():
    """
    Test that function returns 'None' if the crew list is empty.
    """

    actual_result =  calculate_crew_size("")
    expected_result = 0
    assert actual_result == expected_result


def test_calculate_crew_size_none_sep():
    """
    Test that function returns 'None' if the crew list is empty
    but has separators (semi-colons).
    """

    actual_result =  calculate_crew_size(";;;")
    expected_result = 0
    assert actual_result == expected_result


def test_calculate_crew_size_one():
    """
    Test that function returns 1 if the crew list has only one entry.
    """

    actual_result =  calculate_crew_size("Yuri Gagarin;")
    expected_result = 1
    assert actual_result == expected_result


def test_calculate_crew_size_several():
    """
    Test that function returns 3 if the crew list has three entries.
    """

    actual_result =  calculate_crew_size("Neil Armstrong; Buzz Aldrin; Michael Collins;")
    expected_result = 3
    assert actual_result == expected_result


def test_calculate_crew_size_several_empty_entry():
    """
    Test that function returns 2 if the crew list has two real entries
    and one empty entry with a semi-colon separator.
    """

    actual_result =  calculate_crew_size("Neil Armstrong; Buzz Aldrin;;")
    expected_result = 2
    assert actual_result == expected_result  

