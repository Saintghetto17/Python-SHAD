import copy
import zoneinfo
from datetime import datetime

DEFAULT_TZ_NAME = "Europe/Moscow"


def now() -> datetime:
    """Return now in default timezone"""
    return datetime.now(tz=zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))


def strftime(dt: datetime, fmt: str) -> str:
    """Return dt converted to string according to format in default timezone"""
    if dt.tzinfo is None:
        dt_real = dt.replace(tzinfo=zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
        return dt_real.strftime(fmt)
    else:
        dt_real = copy.deepcopy(dt)
        tz = zoneinfo.ZoneInfo(DEFAULT_TZ_NAME)
        dt_real = dt_real.astimezone(tz)
        return dt_real.strftime(fmt)


def strptime(dt_str: str, fmt: str) -> datetime:
    """Return dt parsed from string according to format in default timezone"""
    dt = datetime.strptime(dt_str, fmt)
    if dt.tzinfo is None:
        dt_real = dt.replace(tzinfo=zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
        return dt_real
    dt_real = dt.astimezone(zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
    return dt_real


def diff(first_dt: datetime, second_dt: datetime) -> int:
    """Return seconds between two datetimes rounded down to closest int"""
    if first_dt.tzinfo is None:
        dt_first = datetime(first_dt.year, first_dt.month, first_dt.day, first_dt.hour, first_dt.minute,
                            first_dt.second, first_dt.microsecond,
                            tzinfo=zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
    else:
        dt_first = copy.deepcopy(first_dt)
    if second_dt.tzinfo is None:
        dt_second = datetime(second_dt.year, second_dt.month, second_dt.day, second_dt.hour, second_dt.minute,
                             second_dt.second, second_dt.microsecond,
                             tzinfo=zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
    else:
        dt_second = copy.deepcopy(second_dt)
    # TZ = zoneinfo.ZoneInfo(DEFAULT_TZ_NAME)
    # dt_first.astimezone(TZ)
    # dt_second.astimezone(TZ)
    time_delta = dt_second - dt_first
    total = time_delta.total_seconds()
    return int(total)


def timestamp(dt: datetime) -> int:
    """Return timestamp for given datetime rounded down to closest int"""
    if dt.tzinfo is None:
        dt_real = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
                           tzinfo=zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
    else:
        dt_real = copy.deepcopy(dt)
    return int(datetime.timestamp(dt_real))


def from_timestamp(ts: float) -> datetime:
    """Return datetime from given timestamp"""
    dt = datetime.fromtimestamp(ts, tz=zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
    return dt
