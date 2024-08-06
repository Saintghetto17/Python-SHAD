## Testlib 

Это небольшая библиотечка для облегчения тестирования задач.  
Отвечает за вещи зачастую искусственные в промышленном тестировании, такие как:  
  * Анализ использования модулей 
  * Анализ байткода 
  * Явная проверка наличия докстринга 


### Installation

```bash
pip install --editable tools/testlib
```


### Structure 

* `docs` - докстринги 
* `functions` - функции, разложение их на байткод  
* `memory` - memory тесты 
* `modules` - импорты и тд


[comment]: <> (### Migration )

[comment]: <> (Посколько миграция происходит посреди курса, то не у всех студентов может быть установлена библиотечка. )

[comment]: <> (Проверяем в тестах есть ли библа и скипаем все тесты с ней если нет. )

[comment]: <> (```python)

[comment]: <> (import pytest)

[comment]: <> (try:)

[comment]: <> (    import testlib)

[comment]: <> (except ImportError:)

[comment]: <> (    testlib = None  # type: ignore)

    
[comment]: <> (testlib_installed = pytest.mark.skipif&#40;testlib is None, reason='`testlib` is not installed'&#41;)


[comment]: <> (@testlib_installed)

[comment]: <> (def test_smth&#40;&#41;:)

[comment]: <> (    pass)

[comment]: <> (```)