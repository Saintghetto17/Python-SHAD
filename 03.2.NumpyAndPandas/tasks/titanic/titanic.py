import typing as tp

import pandas as pd


def male_age(df: pd.DataFrame) -> float:
    """
    Return mean age of survived men, embarked in Southampton with fare > 30
    :param df: dataframe
    :return: mean age
    """
    return df[(df["Survived"] == 1) & (df["Embarked"] == "S")
              & (df["Fare"] > 30) & (df["Sex"] == "male")]["Age"].mean()


def nan_columns(df: pd.DataFrame) -> tp.Iterable[str]:
    """
    Return list of columns containing nans
    :param df: dataframe
    :return: series of columns
    """
    return df.columns[df.isnull().any()]


def class_distribution(df: pd.DataFrame) -> pd.Series:
    """
    Return Pclass distrubution
    :param df: dataframe
    :return: series with ratios
    """
    class_dist = df.groupby('Pclass')['PassengerId'].nunique()
    s = class_dist.sum()
    class_dist = class_dist.apply(lambda x: x / s)
    return class_dist


def families_count(df: pd.DataFrame, k: int) -> int:
    """
    Compute number of families with more than k members
    :param df: dataframe,
    :param k: number of members,
    :return: number of families
    """
    df['Family'] = df['Name'].str.split(', ').str[0]
    df = df.groupby(['Family']).size().reset_index()
    res = df[df[0] > k].shape[0]
    return res


def mean_price(df: pd.DataFrame, tickets: tp.Iterable[str]) -> float:
    """
    Return mean price for specific tickets list
    :param df: dataframe,
    :param tickets: list of tickets,
    :return: mean fare for this tickets
    """
    return df[df["Ticket"].isin(tickets)]["Fare"].mean()


def max_size_group(df: pd.DataFrame, columns: list[str]) -> tp.Iterable[tp.Any]:
    """
    For given set of columns compute most common combination of values of these columns
    :param df: dataframe,
    :param columns: columns for grouping,
    :return: list of most common combination
    """
    return df.groupby(columns).size().idxmax()


def dead_lucky(df: pd.DataFrame) -> float:
    """
    Compute dead ratio of passengers with lucky tickets.
    A ticket is considered lucky when it contains an even number of digits in it
    and the sum of the first half of digits equals the sum of the second part of digits
    ex:
    lucky: 123222, 2671, 935755
    not lucky: 123456, 62869, 568290
    :param df: dataframe,
    :return: ratio of dead lucky passengers
    """
    tick_column = df["Ticket"]
    new_tick_column = tick_column.apply(is_lucky)
    df["Ticket"] = new_tick_column
    return df[(df["Ticket"]) & (df["Survived"] == 0)].size / df[(df["Ticket"])].size


def is_lucky(ticket: str) -> bool:
    if not ticket.isnumeric():
        return False
    if len(ticket) % 2 != 0:
        return False
    half: int = len(ticket) // 2
    sum_half: int = 0
    for i in range(half):
        sum_half += int(ticket[i])
    sum_left: int = 0
    for i in range(half, len(ticket)):
        sum_left += int(ticket[i])
    return sum_half == sum_left
