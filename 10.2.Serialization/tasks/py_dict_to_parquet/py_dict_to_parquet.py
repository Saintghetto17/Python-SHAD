import pyarrow as pa
import pyarrow.parquet as pq
<<<<<<< HEAD
import typing as tp

ValueType = int | list[int] | str | dict[str, str] | None
=======


ValueType = int | list[int] | str | dict[str, str]
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b


def save_rows_to_parquet(rows: list[dict[str, ValueType]], output_filepath: str) -> None:
    """
    Save rows to parquet file.

    :param rows: list of rows containing data.
    :param output_filepath: local filepath for the resulting parquet file.
    :return: None.
    """
<<<<<<< HEAD
    map_types: dict[type, tp.Any] = {int: pa.int64(), list: pa.list_(pa.int64()), str: pa.string(),
                                     dict: pa.map_(pa.string(), pa.string())}
    lst_fields: list[tp.Any] = []

    # let us create dict with current key-values support key-values that we have seen
    current_condition: dict[str, tp.Any] = dict()
    # count_keys
    count_keys: dict[str, int] = dict()
    for row in rows:
        for key, val in row.items():
            if key in current_condition.keys():
                if type(current_condition[key]) is not type(val):
                    raise TypeError('Field {field_name} has different types'.format(field_name=key))
                count_keys[key] += 1
                continue
            count_keys[key] = 1
            current_condition[key] = val
    for key in current_condition.keys():
        # every correct key should be counted len(rows) times because it should be in every row
        lst_fields.append(pa.field(key, map_types[type(current_condition[key])], len(rows) != count_keys[key]))
        # parquet automatically put None in place where it is Null
        table = pa.Table.from_pylist(rows, pa.schema(lst_fields))
        pq.write_table(table, output_filepath)
=======
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b
