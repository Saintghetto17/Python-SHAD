## Контекстные менеджеры

`try...except` `contextmanager` `sys.exc_info` `traceback.format_exception_only` `exc.with_traceback`

### Условие

Чудесная штука – исключения. В комплекте же с контекстными менеджерами их возможности возрастают многократно.

Напишите несколько контекстных менеджеров для обработки исключений.

#### Глушитель исключений

```python
with supresser(type_one, ...):
    do_smth()
```

Перехватывает исключения заданых (и только заданных) типов и возвращает управление потоку. Исключение не пробрасывается дальше.

#### Переименователь исключений

```python
with retyper(type_from, type_to):
    do_smth()
```

Меняет тип исключения, оставляя неизменными содержимое ошибки (атрибут args) и трейсбек. Исключение пробрасывается дальше.

#### Дампер исключений

```python
with dumper(stream):
    do_smth()
```

Записывает в переданный поток сообщение об ошибке и пробрасывает его дальше.

### Уточнения

* Нужно, чтоб `dumper` по умолчанию писал в `sys.stderr`, если `stream is None`.
* Чтоб лучше разобраться в исключениях, что у него за аргументы и трейсбек, читайте в [exceptions](https://docs.python.org/3/library/exceptions.html)
* Для извлечения информации о перехваченном исключении использовать модуль [sys](https://docs.python.org/3/library/sys.html#sys.exc_info)
* Чтоб сдампить в dumper только исключение без трейсбека, можно воспользоваться [traceback.format_exception_only](https://docs.python.org/3/library/traceback.html#traceback.format_exception_only)
