# mypy: ignore-errors

import pytest
import testlib

import pyarrow as pa
import pyarrow.parquet as pq

from .py_dict_to_parquet import save_rows_to_parquet


###################
# Structure asserts
###################


def test_docs() -> None:
    assert testlib.is_function_docstring_exists(save_rows_to_parquet)


###################
# Tests
###################


def test_fail_on_column_with_different_types(tmp_path) -> None:
    output_filepath = str(tmp_path / 'test_fail_on_column_with_different_types.parquet')
    rows = [
        {'column1': 10},
        {'column1': 'abc'},
    ]

    with pytest.raises(TypeError) as exc_info:
        save_rows_to_parquet(rows, output_filepath)
    assert str(exc_info.value) == 'Field column1 has different types'


def test_simple_schema(tmp_path) -> None:
    output_filepath = str(tmp_path / 'test_simple_schema.parquet')
    rows = [
        {'age': 29, 'name': 'Harry'},
        {'age': 19, 'name': 'Ann'},
        {'age': 35, 'name': 'Tomas'},
    ]

    save_rows_to_parquet(rows, output_filepath)

    table = pq.read_table(output_filepath)
    assert table.schema == pa.schema([
        pa.field('age', pa.int64(), nullable=False),
        pa.field('name', pa.string(), nullable=False),
    ])
    assert table.to_pylist() == rows


def test_complex_schema(tmp_path) -> None:
    output_filepath = str(tmp_path / 'test_complex_schema.parquet')
    rows = [
        {'age': 29, 'name': 'Harry', 'features': [1, 2, 3]},
        {'name': 'Ann', 'features': [5], 'meta': {'contract': 'XA-445FT-14'}},
        {'name': 'Tomas'},
    ]

    save_rows_to_parquet(rows, output_filepath)

    table = pq.read_table(output_filepath)
    assert table.schema == pa.schema([
        pa.field('age', pa.int64(), nullable=True),
        pa.field('name', pa.string(), nullable=False),
        pa.field('features', pa.list_(pa.int64()), nullable=True),
        pa.field('meta', pa.map_(pa.string(), pa.string()), nullable=True),
    ])
    # We have to manually check each rows due to adding None fields and map type convertion.
    table_data = table.to_pylist()
    assert len(table_data) == len(rows)
    assert table_data[0] == {
        'age': 29, 'name': 'Harry', 'features': [1, 2, 3], 'meta': None
    }
    assert table_data[1] == {
        'age': None, 'name': 'Ann', 'features': [5], 'meta': [('contract', 'XA-445FT-14')]
    }
    assert table_data[2] == {
        'age': None, 'name': 'Tomas', 'features': None, 'meta': None
    }
