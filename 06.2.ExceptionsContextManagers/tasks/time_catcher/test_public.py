import time
import re

import pytest

from .time_catcher import TimeCatcher, SoftTimeoutException, HardTimeoutException, TimeoutException


# match string like: "Time consumed: 0.1234" or "Time consumed: 10.1234"
STR_PATTERN = re.compile(r'Time consumed: \d+\.\d{4}')


@pytest.mark.parametrize('soft_timeout,hard_timeout,correct', [
    (1, 2, True),
    (None, 2, True),
    (1, None, True),
    (None, None, True),
    (0.1, 0.1, True),
    (1, 1, True),
    (0, 2, False),
    (None, 0, False),
    (-1, 2, False),
    (-10, -2, False),
    (1, 0.1, False),
    (16, 8, False),
])
def test_params(soft_timeout: float | None, hard_timeout: float | None, correct: bool) -> None:
    if correct:
        with TimeCatcher(soft_timeout=soft_timeout, hard_timeout=hard_timeout):
            pass
    else:
        with pytest.raises(AssertionError):
            with TimeCatcher(soft_timeout=soft_timeout, hard_timeout=hard_timeout):
                pass


@pytest.mark.parametrize('sleep_time', [.1, 0.25, .5, 1])
def test_time_measure_in_progress(sleep_time: float) -> None:
    with TimeCatcher() as t:
        time.sleep(sleep_time)

    assert sleep_time < float(t) < sleep_time + 0.05
    assert re.search(STR_PATTERN, str(t))


@pytest.mark.parametrize('sleep_time', [.1, .2, .3, .5])
def test_time_measure(sleep_time: float) -> None:
    with TimeCatcher() as t:
        assert 0 < float(t) < 0 + 0.05
        time.sleep(sleep_time)
        assert sleep_time < float(t) < sleep_time + 0.05
        time.sleep(sleep_time)

    assert 2*sleep_time < float(t) < 2*sleep_time + 0.05


@pytest.mark.parametrize('sleep_time,soft_timeout,hard_timeout,exception', [
    (0.1, 0.01, None, SoftTimeoutException),
    (0.2, 0.1, 100, SoftTimeoutException),
    (0.5, 0.1, 1, SoftTimeoutException),
    (0.1, None, 0.01, HardTimeoutException),
    (0.6, 0.3, 0.5, HardTimeoutException),
    (0.6, 0.5, 0.5, HardTimeoutException),
])
def test_timeout(
        sleep_time: float, soft_timeout: float | None, hard_timeout: float, exception: type[TimeoutException]
) -> None:

    with pytest.raises(TimeoutException):
        with TimeCatcher(soft_timeout=soft_timeout, hard_timeout=hard_timeout):
            time.sleep(sleep_time)
