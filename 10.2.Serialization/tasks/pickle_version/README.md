## Pickle protocol version

`serialization` `pickle`

### Условие

Реализовать функцию, которая по сериализованному через pickle объекту будет возвращать используемую версию протокола. Возвращать нужно объет типа `PickleVersion` (объявлен в `pickle_version.py`).
Заполнять его нужно следующим образом:
* `is_new_version` - `False` для версий 0 и 1. `True` для все более старших версий.
* `version` - `-1` для версий 0 и 1. Значение версии для более старших версий.

Таким образом старые версии 0 и 1 отличаться не должны.
Для них возвращается `PickleVersion(False, -1)`

Полезные ссылки:
* ["Исполняемая" документация Pickle](https://github.com/python/cpython/blob/master/Lib/pickletools.py)
* [Python реализация pickle](https://github.com/python/cpython/blob/master/Lib/pickle.py)

**Примечание:** В этой задаче предполагается решение без перебора всех версий протокола.

### Пример

```python
In [1]: from pickle_version.pickle_version import get_pickle_version

In [2]: get_pickle_version(b'\x80\x03X\x04\x00\x00\x001265q\x00.')
Out[2]: PickleVersion(is_new_format=True, version=3)
```
