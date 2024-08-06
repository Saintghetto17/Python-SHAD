import datetime
import enum
import typing as tp  # noqa


class GranularityEnum(enum.Enum):
    """
    Enum for describing granularity
    """
    DAY = datetime.timedelta(days=1)
    TWELVE_HOURS = datetime.timedelta(hours=12)
    HOUR = datetime.timedelta(hours=1)
    THIRTY_MIN = datetime.timedelta(minutes=30)
    FIVE_MIN = datetime.timedelta(minutes=5)


def truncate_to_granularity(dt: datetime.datetime, gtd: GranularityEnum) -> datetime.datetime:
    """
    :param dt: datetime to truncate
    :param gtd: granularity
    :return: resulted datetime
    """
    if gtd.name == 'DAY':
        return datetime.datetime(year=dt.year, month=dt.month, day=dt.day, hour=0, minute=0)
    elif gtd.name == 'HOUR':
        return datetime.datetime(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour, minute=0)
    elif gtd.name == 'TWELVE_HOURS':
        return datetime.datetime(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour // 12 * 12, minute=0)
    elif gtd.name == 'THIRTY_MIN':
        return datetime.datetime(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour, minute=dt.minute // 30 * 30)
    elif gtd.name == 'FIVE_MIN':
        return datetime.datetime(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour, minute=dt.minute // 5 * 5)
    return datetime.datetime(year=0, month=0, day=0, hour=0, minute=0)


class DtRange:
    def __init__(
            self,
            before: int,
            after: int,
            shift: int,
            gtd: GranularityEnum
    ) -> None:
        """
        :param before: number of datetimes should take before `given datetime`
        :param after: number of datetimes should take after `given datetime`
        :param shift: shift of `given datetime`
        :param gtd: granularity
        """
        self._before = before
        self._after = after
        self._shift = shift
        self._gtd = gtd

    def __call__(self, dt: datetime.datetime) -> list[datetime.datetime]:
        """
        :param dt: given datetime
        :return: list of datetimes in range
        """
        lst_res: list[datetime.datetime] = []
        shifted = dt + self._shift * self._gtd.value
        shifted_time = truncate_to_granularity(shifted, self._gtd)
        for i in range(self._before):
            elem = shifted_time - (self._before - i) * self._gtd.value
            lst_res.append(truncate_to_granularity(elem, self._gtd))
        lst_res.append(shifted_time)
        for i in range(self._after):
            elem = shifted_time + (i + 1) * self._gtd.value
            lst_res.append(truncate_to_granularity(elem, self._gtd))
        return lst_res


def get_interval(
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        gtd: GranularityEnum
) -> list[datetime.datetime]:
    """
    :param start_time: start of interval
    :param end_time: end of interval
    :param gtd: granularity
    :return: list of datetimes according to granularity
    """
    lst_res: list[datetime.datetime] = []
    if gtd.name == 'HOUR':
        rng = (end_time - start_time).seconds
        if rng < 3600:
            return []
        else:
            amount = rng // 3600
            if start_time.minute != 0 or start_time.second != 0 or start_time.microsecond != 0:
                if start_time.hour == 23:
                    amount += 1
                truncated_first = truncate_to_granularity(start_time, gtd) + GranularityEnum.HOUR.value
            else:
                truncated_first = truncate_to_granularity(start_time, gtd)
            amount -= 1
            lst_res.append(truncated_first)
            for i in range(amount):
                lst_res.append(truncated_first + (i + 1) * gtd.value)
            print(lst_res)
            return lst_res
    elif gtd.name == 'TWELVE_HOURS':
        if start_time.hour == 12 and start_time.minute == 0 and start_time.second == 0 and start_time.microsecond == 0:
            truncated_first = start_time
            lst_res.append(truncated_first)
        else:
            truncated_first = truncate_to_granularity(start_time, gtd) + GranularityEnum.TWELVE_HOURS.value
            lst_res.append(truncated_first)
        truncated = truncated_first + GranularityEnum.TWELVE_HOURS.value
        while truncated <= end_time:
            lst_res.append(truncated)
            truncated += GranularityEnum.TWELVE_HOURS.value
        return lst_res
    elif gtd.name == 'FIVE_MIN':
        truncated = truncate_to_granularity(start_time, gtd)
        if truncated == start_time:
            lst_res.append(truncated)
        else:
            truncated = truncated + GranularityEnum.FIVE_MIN.value
        while truncated <= end_time:
            lst_res.append(truncated)
            truncated = truncated + GranularityEnum.FIVE_MIN.value
        return lst_res
    return []
