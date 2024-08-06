import typing as tp
from pathlib import Path

import pytest
import numpy as np
import pandas as pd
from pandas.testing import assert_series_equal

from .titanic import male_age, nan_columns, class_distribution, \
    families_count, mean_price, max_size_group, dead_lucky


FILE_PATH = Path(__file__).parent / 'titanic.csv'


@pytest.fixture(scope='function')
def dataframe() -> pd.DataFrame:
    df = pd.read_csv(FILE_PATH, sep='\t')
    yield df


def test_male_age(dataframe: pd.DataFrame) -> None:
    np.testing.assert_allclose(male_age(dataframe), 30.)


def test_nan_columns(dataframe: pd.DataFrame) -> None:
    assert set(nan_columns(dataframe)) == {'Age', 'Cabin', 'Embarked'}


def test_class_distribution(dataframe: pd.DataFrame) -> None:
    class_distr_ans = pd.Series(data=[0.192308, 0.192308, 0.615385], index=[1, 2, 3], name='Pclass')
    assert_series_equal(class_distribution(dataframe).sort_index(), class_distr_ans,
                        check_index_type=False, check_names=False)  # added for new Pandas stuff


@pytest.mark.parametrize('count_members,count_families', [
    (0, 141),
    (1, 13),
    (2, 1),
    (3, 1),
    (4, 0),
])
def test_families_count(count_members: int, count_families: int, dataframe: pd.DataFrame) -> None:
    assert families_count(dataframe, count_members) == count_families


def test_mean_price(dataframe: pd.DataFrame) -> None:
    np.testing.assert_allclose(
        mean_price(dataframe, dataframe['Ticket'].unique()),
        dataframe['Fare'].mean()
    )

    for i, row in dataframe.iterrows():
        np.testing.assert_allclose(mean_price(dataframe, [row['Ticket']]), row['Fare'])

    value = 26.0
    tickets = dataframe[np.isclose(dataframe['Fare'], value)]['Ticket']
    assert mean_price(dataframe, tickets) == pytest.approx(value)


@pytest.mark.parametrize('columns,expected_result', [
    (['Survived', 'Sex'], (0, 'male')),
    (['Survived', 'Sex', 'Cabin'], (0, 'male', 'D26')),
    (['Embarked', 'Pclass'], ('S', 3)),
    (['Age'], (21.00,)),
])
def test_max_size_group(columns: list[str], expected_result: tuple[tp.Any], dataframe: pd.DataFrame) -> None:
    assert max_size_group(dataframe, columns) == expected_result


def test_dead_lucky(dataframe: pd.DataFrame) -> None:
    assert dead_lucky(dataframe) == pytest.approx(0.75)
