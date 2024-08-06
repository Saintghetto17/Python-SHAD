import dataclasses
from datetime import datetime, timedelta

import pytest

from . import time_to_range


@pytest.mark.parametrize('gtd, dt, expected', [
    (time_to_range.GranularityEnum.THIRTY_MIN, datetime(2020, 9, 30, 10, 21), datetime(2020, 9, 30, 10, 51)),
    (time_to_range.GranularityEnum.FIVE_MIN, datetime(2020, 9, 30, 10, 31), datetime(2020, 9, 30, 10, 36)),
    (time_to_range.GranularityEnum.HOUR, datetime(2020, 9, 30, 10, 30), datetime(2020, 9, 30, 11, 30)),
    (time_to_range.GranularityEnum.DAY, datetime(2020, 9, 30, 10, 00), datetime(2020, 10, 1, 10, 00)),
    (time_to_range.GranularityEnum.TWELVE_HOURS, datetime(2020, 9, 30, 10, 21), datetime(2020, 9, 30, 22, 21))
])
def test_granularity_enum(gtd: time_to_range.GranularityEnum, dt: datetime, expected: timedelta) -> None:
    assert dt + gtd.value == expected


@pytest.mark.parametrize('gtd, dt, truncated_dt', [
    (time_to_range.GranularityEnum.HOUR, datetime(2020, 9, 30, 23, 18, 24), datetime(2020, 9, 30, 23, 0, 0)),
    (time_to_range.GranularityEnum.THIRTY_MIN, datetime(2020, 9, 30, 10, 21), datetime(2020, 9, 30, 10, 00)),
    (time_to_range.GranularityEnum.THIRTY_MIN, datetime(2020, 9, 30, 10, 31), datetime(2020, 9, 30, 10, 30)),
    (time_to_range.GranularityEnum.THIRTY_MIN, datetime(2020, 9, 30, 10, 30), datetime(2020, 9, 30, 10, 30)),
    (time_to_range.GranularityEnum.THIRTY_MIN, datetime(2020, 9, 30, 10, 00), datetime(2020, 9, 30, 10, 00)),
    (time_to_range.GranularityEnum.FIVE_MIN, datetime(2020, 9, 30, 10, 21), datetime(2020, 9, 30, 10, 20)),
    (time_to_range.GranularityEnum.FIVE_MIN, datetime(2020, 9, 30, 10, 20), datetime(2020, 9, 30, 10, 20)),
    (time_to_range.GranularityEnum.FIVE_MIN, datetime(2020, 9, 30, 10, 19), datetime(2020, 9, 30, 10, 15)),
    (time_to_range.GranularityEnum.TWELVE_HOURS, datetime(2020, 9, 30, 0, 0), datetime(2020, 9, 30, 0, 0)),
    (time_to_range.GranularityEnum.TWELVE_HOURS, datetime(2020, 9, 30, 0, 1), datetime(2020, 9, 30, 0, 0)),
    (time_to_range.GranularityEnum.TWELVE_HOURS, datetime(2020, 9, 30, 11, 59), datetime(2020, 9, 30, 0, 0)),
    (time_to_range.GranularityEnum.TWELVE_HOURS, datetime(2020, 9, 30, 12, 0), datetime(2020, 9, 30, 12, 0)),
    (time_to_range.GranularityEnum.TWELVE_HOURS, datetime(2020, 9, 30, 12, 1), datetime(2020, 9, 30, 12, 0)),
    (time_to_range.GranularityEnum.TWELVE_HOURS, datetime(2020, 9, 30, 23, 59), datetime(2020, 9, 30, 12, 0)),
    (time_to_range.GranularityEnum.HOUR, datetime(2020, 9, 30, 10, 23), datetime(2020, 9, 30, 10, 0)),
    (time_to_range.GranularityEnum.HOUR, datetime(2020, 9, 30, 10, 1), datetime(2020, 9, 30, 10, 0)),
    (time_to_range.GranularityEnum.HOUR, datetime(2020, 9, 30, 10, 0), datetime(2020, 9, 30, 10, 0)),
    (time_to_range.GranularityEnum.HOUR, datetime(2020, 9, 30, 9, 59), datetime(2020, 9, 30, 9, 0)),
    (time_to_range.GranularityEnum.DAY, datetime(2020, 9, 30, 11, 23), datetime(2020, 9, 30, 0, 0)),
    (time_to_range.GranularityEnum.DAY, datetime(2020, 9, 30, 0, 0), datetime(2020, 9, 30, 0, 0)),
    (time_to_range.GranularityEnum.DAY, datetime(2019, 12, 31, 23, 59), datetime(2019, 12, 31, 0, 0)),
    (time_to_range.GranularityEnum.HOUR, datetime(2020, 9, 30, 0, 0, 1), datetime(2020, 9, 30, 0, 0)),
])
def test_truncate_to_granularity(gtd: time_to_range.GranularityEnum, dt: datetime, truncated_dt: timedelta) -> None:
    assert time_to_range.truncate_to_granularity(dt, gtd) == truncated_dt


@dataclasses.dataclass
class Case:
    before: int
    after: int
    shift: int
    gtd: time_to_range.GranularityEnum
    dt: datetime
    expected: list[datetime]


TEST_CASES = [
    Case(before=1, after=1, shift=-2, gtd=time_to_range.GranularityEnum.HOUR,
         dt=datetime(2020, 9, 30, 23, 18, 24),
         expected=[datetime(2020, 9, 30, 20, 0, 0), datetime(2020, 9, 30, 21, 0, 0), datetime(2020, 9, 30, 22, 0, 0)]),
    Case(before=1, after=1, shift=0, gtd=time_to_range.GranularityEnum.HOUR,
         dt=datetime(2020, 9, 30, 10),
         expected=[datetime(2020, 9, 30, 9), datetime(2020, 9, 30, 10), datetime(2020, 9, 30, 11)]),
    Case(before=1, after=1, shift=0, gtd=time_to_range.GranularityEnum.TWELVE_HOURS,
         dt=datetime(2020, 9, 30, 10),
         expected=[datetime(2020, 9, 29, 12), datetime(2020, 9, 30, 0), datetime(2020, 9, 30, 12)]),
    Case(before=1, after=1, shift=0, gtd=time_to_range.GranularityEnum.DAY,
         dt=datetime(2020, 9, 30),
         expected=[datetime(2020, 9, 29), datetime(2020, 9, 30), datetime(2020, 10, 1)]),
    Case(before=1, after=1, shift=0, gtd=time_to_range.GranularityEnum.FIVE_MIN,
         dt=datetime(2020, 9, 30, 10, 0, 0),
         expected=[datetime(2020, 9, 30, 9, 55), datetime(2020, 9, 30, 10, 0), datetime(2020, 9, 30, 10, 5)]),
    Case(before=1, after=1, shift=0, gtd=time_to_range.GranularityEnum.HOUR,
         dt=datetime(2020, 9, 30, 10, 59, 59),
         expected=[datetime(2020, 9, 30, 9), datetime(2020, 9, 30, 10), datetime(2020, 9, 30, 11)]),
    Case(before=0, after=1, shift=0, gtd=time_to_range.GranularityEnum.HOUR,
         dt=datetime(2020, 9, 30, 10, 59, 59),
         expected=[datetime(2020, 9, 30, 10), datetime(2020, 9, 30, 11)]),
    Case(before=1, after=2, shift=14, gtd=time_to_range.GranularityEnum.HOUR,
         dt=datetime(2020, 9, 30, 10, 59, 59),
         expected=[datetime(2020, 9, 30, 23), datetime(2020, 10, 1, 0),
                   datetime(2020, 10, 1, 1), datetime(2020, 10, 1, 2)]),
    Case(before=2, after=1, shift=-10, gtd=time_to_range.GranularityEnum.HOUR,
         dt=datetime(2020, 9, 30, 10, 59, 59),
         expected=[datetime(2020, 9, 29, 22), datetime(2020, 9, 29, 23),
                   datetime(2020, 9, 30, 0), datetime(2020, 9, 30, 1)]),
    Case(before=1, after=1, shift=-1, gtd=time_to_range.GranularityEnum.HOUR,
         dt=datetime(2020, 9, 30, 23, 18, 24, 1),
         expected=[datetime(2020, 9, 30, 21, 0, 0), datetime(2020, 9, 30, 22, 0, 0), datetime(2020, 9, 30, 23, 0, 0)]),
]


@pytest.mark.parametrize('t', TEST_CASES)
def test_dt_range(t: Case) -> None:
    assert all(mth.startswith('_') for mth in dir(time_to_range.DtRange)), "You shouldn't make any public methods." \
                                                                           "They are not part of public interface"

    dt_range = time_to_range.DtRange(before=t.before, after=t.after, shift=t.shift, gtd=t.gtd)
    assert dt_range(t.dt) == t.expected

    assert all(attr.startswith('_') for attr in dt_range.__dict__), "You shouldn't make any public attributes. " \
                                                                    "They are not part of public interface"


@dataclasses.dataclass
class IntervalCase:
    start_dt: datetime
    end_dt: datetime
    gtd: time_to_range.GranularityEnum
    expected: list[datetime]


INTERVAL_TEST_CASES = [
    IntervalCase(
        start_dt=datetime(2020, 9, 30, 23, 18, 24), end_dt=datetime(2020, 10, 1, 2, 0, 0),
        gtd=time_to_range.GranularityEnum.HOUR,
        expected=[datetime(2020, 10, 1, 0, 0, 0), datetime(2020, 10, 1, 1, 0, 0), datetime(2020, 10, 1, 2, 0, 0)]
    ),
    IntervalCase(
        start_dt=datetime(2020, 9, 30, 12, 0, 0), end_dt=datetime(2020, 10, 1, 12, 0),
        gtd=time_to_range.GranularityEnum.TWELVE_HOURS,
        expected=[datetime(2020, 9, 30, 12), datetime(2020, 10, 1, 0), datetime(2020, 10, 1, 12)]
    ),
    IntervalCase(
        start_dt=datetime(2020, 9, 30, 12, 0, 0, 1), end_dt=datetime(2020, 10, 1, 12, 0),
        gtd=time_to_range.GranularityEnum.TWELVE_HOURS,
        expected=[datetime(2020, 10, 1, 0), datetime(2020, 10, 1, 12)]
    ),
    IntervalCase(
        start_dt=datetime(2020, 9, 30, 18, 10, 8),  end_dt=datetime(2020, 10, 1, 12, 0),
        gtd=time_to_range.GranularityEnum.TWELVE_HOURS,
        expected=[datetime(2020, 10, 1, 0), datetime(2020, 10, 1, 12)]
    ),
    IntervalCase(
        start_dt=datetime(2020, 9, 30, 18, 10, 8),  end_dt=datetime(2020, 9, 30, 18, 12),
        gtd=time_to_range.GranularityEnum.HOUR,
        expected=[]
    ),
    IntervalCase(
        start_dt=datetime(2020, 9, 30, 18, 10, 8), end_dt=datetime(2020, 9, 30, 19, 12),
        gtd=time_to_range.GranularityEnum.HOUR,
        expected=[datetime(2020, 9, 30, 19)]
    ),
    IntervalCase(
        start_dt=datetime(2020, 9, 30, 18, 8, 12), end_dt=datetime(2020, 9, 30, 18, 20, 11),
        gtd=time_to_range.GranularityEnum.FIVE_MIN,
        expected=[datetime(2020, 9, 30, 18, 10), datetime(2020, 9, 30, 18, 15),
                  datetime(2020, 9, 30, 18, 20)]
    )
]


@pytest.mark.parametrize('t', INTERVAL_TEST_CASES)
def test_get_interval(t: IntervalCase) -> None:
    assert time_to_range.get_interval(t.start_dt, t.end_dt, t.gtd) == t.expected
