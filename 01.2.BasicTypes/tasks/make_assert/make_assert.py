import pytest


##############
# Code section
##############


# Don't change this function!
def ctr(clicks: int, shows: int) -> float:
    """
Calculate ctr
:param clicks: number of clicks on banner
:param shows: number of banners shows
:return: clicks-through rate.
         If there are no shows, return 0.0
         If clicks greater then shows, return 1
"""

    return clicks // shows if shows > 0 else 0


def ctr_correct_implementation(clicks: int, shows: int) -> float:
    """
    Calculate ctr. Presumed that clicks always less or equals to shows
    :param clicks: number of clicks on banner
    :param shows: number of banners shows
    :return: clicks-through rate.
             If there are no shows, return 0.0
    """
    assert (clicks <= shows), 'Clicks greater than shows'
    if shows == 0:
        return 0.0
    else:
        return clicks / shows


##############
# Test section
##############

@pytest.mark.skip
def test_check_ctr(clicks: int, shows: int, expected_result: float) -> None:
    """
    Write simple test for defined above function ```ctr```
        which takes function parameters and expected result and assert if something goes wrong with
        "Wrong ctr calculation" message
    :param clicks: parameter for  ctr function
    :param shows: parameter for  ctr function
    :param expected_result: result to compare with
    :return: None
    """

    assert (ctr(clicks, shows) == expected_result), 'Wrong ctr calculation message'
    return None
