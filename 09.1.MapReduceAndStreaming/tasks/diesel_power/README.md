## Map-Reduce

`mapreduce` `generators` `mapper` `reducer` `joiner` `heapq`

### Условие

Часть библиотеки для удобного запуска вычислений над таблицами.


### Операции



Казалось бы, операции над таблицами можно объявлять просто, как функции, принимающие таблицу и
возвращающие новую. Но я поступил иначе: наши операции будут работать со строками таблицы, а не
с таблицей целиком. Так их будет проще применять - можно будет избегать лишних копирований
и много чего еще.

```python
class Operation(ABC):
    @abstractmethod
    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        pass
```

**Замечание**: конструкция с `abstractmethod`'ом позволяет создавать т.н. абстрактные классы - классы,
объекты которых нельзя создать. Это сделано для того, чтобы указать – данный класс не является
"самостоятельным", требуется создать класс-наследник с конкретной реализацией метода (или методов).
Объекты такого класса уже могут быть созданы. Обычно абстрактные классы используются для описания т.н.
интерфейса - некоторого шаблона, которому должны соответствовать потомки.

1. **`Map`** — операция, которая вызывает переданный генератор (называемый `Mapper`'ом) от каждой
из строк таблицы. Значения, выданные генератором, образуют таблицу-результат.
(Подходит для элементарных операций над строками - фильтраций, преобразований типов, элементарных
операций над полями таблицы etc).

```python
class Map(Operation):
    def __init__(self, mapper: Mapper) -> None:
        self.mapper = mapper

    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        pass
```

Мап  не тождественен функции `map` из python, которая реализует соответствие 1-к-1
(наша по каждой строке может вернуть любое число строк).

Простейший маппер может быть таким:

```python
class DummyMapper(Mapper):
    def __call__(self, row: TRow) -> TRowsGenerator:
        yield row
```

Он просто пропускает через себя строки (довольно бесполезно, не правда ли?).



2. **`Reduce`** принимает на вход таблицу, группирует её строки по ключу (где ключ - значение какого-то
подмножества колонок таблицы) и вызывает `Reducer` для строк с одинаковым ключом.

```python
class Reduce(Operation):
    def __init__(self, reducer: Reducer, keys: tp.Sequence[str]) -> None:
        self.reducer = reducer
        self.keys = keys

    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        pass
```

Для эффективной работы этой операции (за O(n)) таблица, подаваемая на вход, должна быть отсортирована
по колонкам, на которых операция запускается. Если посмотреть на запуски тестов редьюса, там это условие
явно выполняется.

Интерфейс редьюсера:

```python
class Reducer(ABC):
    @abstractmethod
    def __call__(self, group_key: tp.Tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        pass
```

**Обратите внимание**: передаются не только строки таблицы, но и названия колонок, являющихся ключом.

Это важно для редьюсеров-сверток, которые осуществляют операцию сворачивания (`fold`) нескольких
строк в одну, применяя какую-нибудь ассоциативную операцию (например, суммируют значение в колонке).

Для колонок, не являющихся ключом группы, и на которые не распространяется операция свертки, есть
неоднозначность, поэтому данные колонки удаляются из вывода (см. `test_sum`, колонка `player_id`).

Пример редьюсера:

```python
class FirstReducer(Reducer):
    def __call__(self, group_key: tp.Tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        for row in rows:
            yield row
            break
```
Возвращает первую строчку из своей группы (такой `head` для бедных).


3. **`Join`** — самая непростая операция, объединяющая информацию из двух таблиц в одну по ключу.
Строки новой таблицы будут созданы из строк двух таблиц, участвовавших в джойне. Интерфейс самой операции
похож на интерфейс `Reduce`:

```python
class Join(Operation):
    def __init__(self, joiner: Joiner, keys: tp.Sequence[str]) -> None:
        self.keys = keys
        self.joiner = joiner

    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        pass
```

`Join` разбивает потоки на блоки по заданному ключу, и передает их 
в некоторый объект `Joiner`, который уточняет требуемую стратегию слияния:

```python
class Joiner(ABC):
    def __init__(self, suffix_a: str = '_1', suffix_b: str = '_2') -> None:
        self._a_suffix = suffix_a
        self._b_suffix = suffix_b

    @abstractmethod
    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        pass

```

Дело в том, что для join надо существуют несколько стратегий — `inner`, `outer`, `left` и `right`,
которые отличаются поведением при объединении колонок (например, что делать, если такого значения по 
данному ключу в одной из колонок нет).



Для каждой стратегии имеет заглушку:

```python
class InnerJoiner(Joiner):
    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        pass
```
