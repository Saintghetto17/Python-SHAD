## TYPY GENERIC

`typing` `generic` `selfreference`

### Условие

Нужно реализовать и аннотировать класс Pair, который является Generic классом с параметром. 
Как ограничивать входные типы - смотрите в тестах.


### Про задачу

* Здесь вам нужно вспомнить, как создавать [классы-генерики](https://mypy.readthedocs.io/en/latest/generics.html)
* Для того, чтоб в методе ```__iadd__``` сослаться на себя, нужно воспользоваться [Forward reference](https://mypy.readthedocs.io/en/latest/runtime_troubles.html?highlight=forward%20reference#class-name-forward-references)
* TypeVar для генериков нужно сделать [с ограничениями](https://mypy.readthedocs.io/en/latest/generics.html#type-variables-with-value-restriction)
* В тестах проверяется:
  * Что вы везде навесили аннотации
  * Что в случае плохих переданных значений mypy падает, а в случае хороших - успешно проходит

Воспринимайте тесты, как условия, которым должен удовлетворять интерфейс ваших функций и классов.
