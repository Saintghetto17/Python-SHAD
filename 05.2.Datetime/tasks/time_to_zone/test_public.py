import os
import time
import typing as tp
from contextlib import contextmanager
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest
import tzlocal  # type: ignore

from . import time_to_zone


@contextmanager
def _local_timezone_manager(tz_name: str | None) -> tp.Generator[None, None, None]:
    """Initialize, or reinitialize, the local timezone"""
    if tz_name is None:
        yield
    else:
        current_zone = str(tzlocal.get_localzone())
        current_tz = os.environ.get('TZ')
        try:
            os.environ['TZ'] = tz_name
            time.tzset()
            yield
        finally:
            os.environ['TZ'] = current_zone
            time.tzset()
            if current_tz is None:
                os.environ.pop('TZ')
            else:
                os.environ['TZ'] = current_tz


LOCAL_TIMEZONES = [
    None, 'Europe/Madrid', 'Europe/Kiev', 'Europe/Moscow', 'Europe/Berlin', 'UTC', 'Asia/Singapore', 'Australia/Eucla'
]


@pytest.mark.parametrize('tz', LOCAL_TIMEZONES)
def test_now(tz: str) -> None:
    with _local_timezone_manager(tz):
        some_now = time_to_zone.now()
        assert time.time() - some_now.timestamp() < 1
        assert some_now.utcoffset() == timedelta(hours=3)


@pytest.mark.parametrize('tz', LOCAL_TIMEZONES)
@pytest.mark.parametrize('dt_str, fmt, expected_dt', [
    ('2020-10-01T11:00:00', '%Y-%m-%dT%H:%M:%S', datetime(2020, 10, 1, 11, 0, 0)),
    ('2020-10-01T11:00:00 +0300', '%Y-%m-%dT%H:%M:%S %z', datetime(2020, 10, 1, 11, 0, 0)),
    ('2020-10-01T11:00:00 +0000', '%Y-%m-%dT%H:%M:%S %z', datetime(2020, 10, 1, 14, 0, 0)),
    ('2020-10-01T11:00:00.123456', '%Y-%m-%dT%H:%M:%S.%f', datetime(2020, 10, 1, 11, 0, 0, 123456))
])
def test_strptime(tz: str, dt_str: str, fmt: str, expected_dt: datetime) -> None:
    with _local_timezone_manager(tz):
        dt = time_to_zone.strptime(dt_str, fmt)
        assert dt.replace(tzinfo=None) == expected_dt
        assert dt.utcoffset() == timedelta(hours=3)


@pytest.mark.parametrize('tz', LOCAL_TIMEZONES)
@pytest.mark.parametrize('dt, fmt, expected_dt_str', [
    (datetime(2020, 10, 1, 14, 0, 0), '%Y-%m-%dT%H:%M:%S %z', '2020-10-01T14:00:00 +0300'),
    (datetime(2020, 10, 1, 14, 0, 0), '%Y-%m-%dT%H:%M:%S', '2020-10-01T14:00:00'),
    (datetime(2020, 10, 1, 14, 0, 0, tzinfo=ZoneInfo('Europe/Moscow')), '%Y-%m-%dT%H:%M:%S', '2020-10-01T14:00:00'),
    (datetime(2020, 10, 1, 14, 0, 0, tzinfo=ZoneInfo('Europe/Moscow')),
        '%Y-%m-%dT%H:%M:%S %z', '2020-10-01T14:00:00 +0300'),
    (datetime(2020, 10, 1, 14, 0, 0, tzinfo=ZoneInfo('Europe/Berlin')),
        '%Y-%m-%dT%H:%M:%S %z', '2020-10-01T15:00:00 +0300'),
    (datetime(2020, 10, 1, 14, 0, 0, tzinfo=ZoneInfo('Europe/Berlin')), '%Y-%m-%dT%H:%M:%S', '2020-10-01T15:00:00'),
    (datetime(2020, 10, 1, 14, 0, 0, 123456), '%Y-%m-%dT%H:%M:%S.%f %z', '2020-10-01T14:00:00.123456 +0300'),
])
def test_strftime(tz: str, dt: datetime, fmt: str, expected_dt_str: str) -> None:
    """Return dt in Moscow timezone"""
    with _local_timezone_manager(tz):
        assert time_to_zone.strftime(dt, fmt) == expected_dt_str


@pytest.mark.parametrize('tz', LOCAL_TIMEZONES)
@pytest.mark.parametrize('start_dt, end_dt, expected_seconds', [
    (datetime(2020, 10, 1, 14, 0, 0), datetime(2020, 10, 1, 16, 0, 0), 60 * 60 * 2),
    (datetime(2020, 10, 1, 14, 0, 0, tzinfo=ZoneInfo('Europe/Moscow')), datetime(2020, 10, 1, 16, 0, 0), 60 * 60 * 2),
    (datetime(2020, 10, 1, 14, 0, 0), datetime(2020, 10, 1, 16, 0, 0, tzinfo=ZoneInfo('Europe/Moscow')), 60 * 60 * 2),
    (datetime(2020, 10, 1, 14, 0, 0, tzinfo=ZoneInfo('Europe/Moscow')),
        datetime(2020, 10, 1, 16, 0, 0, tzinfo=ZoneInfo('Europe/Moscow')), 60 * 60 * 2),
    (datetime(2020, 10, 1, 14, 0, 0, tzinfo=ZoneInfo('Europe/Berlin')),
        datetime(2020, 10, 1, 16, 0, 0, tzinfo=ZoneInfo('Europe/Moscow')), 60 * 60 * 1),
    (datetime(2020, 10, 1, 14, 0, 0, tzinfo=ZoneInfo('Europe/Moscow')),
        datetime(2020, 10, 1, 16, 0, 0, tzinfo=ZoneInfo('Europe/Berlin')), 60 * 60 * 3),
    (datetime(2020, 10, 1, 14, 0, 0), datetime(2020, 10, 1, 16, 0, 0, tzinfo=ZoneInfo('Europe/Berlin')), 60 * 60 * 3),
    (datetime(2020, 10, 1, 14, 0, 0, tzinfo=ZoneInfo('Europe/Berlin')), datetime(2020, 10, 1, 16, 0, 0), 60 * 60 * 1),
    (datetime(2020, 10, 1, 14, 0, 0, 123456), datetime(2020, 10, 1, 16, 0, 0, 999999), 60 * 60 * 2),
    (datetime(2020, 10, 1, 14, 0, 0, 999999), datetime(2020, 10, 1, 16, 0, 0, 123456), 60 * 60 * 2 - 1),
    (datetime(2020, 10, 1, 16, 0, 0), datetime(2020, 10, 1, 14, 0, 0), -60 * 60 * 2)
])
def test_diff_dt(tz: str, start_dt: datetime, end_dt: datetime, expected_seconds: int) -> None:
    with _local_timezone_manager(tz):
        assert time_to_zone.diff(start_dt, end_dt) == expected_seconds


@pytest.mark.parametrize('tz', LOCAL_TIMEZONES)
@pytest.mark.parametrize('dt, expected_ts', [
    (datetime(2020, 10, 1, 14, 0, 0), 1601550000),
    (datetime(2020, 10, 1, 14, 0, 0, tzinfo=ZoneInfo('Europe/Moscow')), 1601550000),
    (datetime(2020, 10, 1, 13, 0, 0, tzinfo=ZoneInfo('Europe/Berlin')), 1601550000),
    (datetime(1970, 1, 1, 0, 0, 0), -3 * 60 * 60),
    (datetime(1970, 1, 1, 0, 0, 0, tzinfo=ZoneInfo('Europe/Moscow')), -3 * 60 * 60),
    (datetime(1970, 1, 1, 0, 0, 0, tzinfo=ZoneInfo('UTC')), 0),
    (datetime(2020, 10, 1, 14, 0, 0, 123456), 1601550000),
    (datetime(2020, 10, 1, 14, 0, 0, 999999), 1601550000),
])
def test_timestamp(tz: str, dt: datetime, expected_ts: int) -> None:
    with _local_timezone_manager(tz):
        assert time_to_zone.timestamp(dt) == expected_ts


@pytest.mark.parametrize('tz', LOCAL_TIMEZONES)
@pytest.mark.parametrize('ts, expected_dt', [
    (1601550000, datetime(2020, 10, 1, 14, 0, 0, tzinfo=ZoneInfo('Europe/Moscow'))),
    (0, datetime(1970, 1, 1, 3, 0, 0, tzinfo=ZoneInfo('Europe/Moscow'))),
    (0.123456, datetime(1970, 1, 1, 3, 0, 0, 123456, tzinfo=ZoneInfo('Europe/Moscow'))),
])
def test_from_timestamp(tz: str, ts: int, expected_dt: datetime) -> None:
    with _local_timezone_manager(tz):
        dt = time_to_zone.from_timestamp(ts)
        assert dt == expected_dt
        assert dt.replace(tzinfo=None) == expected_dt.replace(tzinfo=None)
        assert dt.utcoffset() == timedelta(hours=3)
