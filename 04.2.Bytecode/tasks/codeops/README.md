## CODEOPS

`dis.get_instructions` `instruction.argval` `instruction.opname` `types.CodeType`

### Условие

В этом задании вы познакомитесь с байткодом питона и поработаете с функцией `get_instructions` модуля `dis`, которая пригодится вам в первой большой домашке.

Вам нужно написать функцию `count_operations`, которая для данного code object'а возвращает какие bytecode-операции и сколько раз в нём встретились.

Некоторые операции вызываются над другими code object'ами, их тоже нужно учесть. Вам нужно обойти дерево выполнения, извлекая все операции.

### Пример

Например, дан такой код:

```python
In [4]: func_text = """
   ...: def f():
   ...:     a = 1
   ...: print(f())
   ...: """
```

Можно вызвать функцию dis, чтобы посмотреть на байткод:

```python
In [6]: import dis
In [7]: dis.dis(func_text)
  2           0 LOAD_CONST               0 (<code object f at 0x103ff4150, file "<dis>", line 2>)
              2 LOAD_CONST               1 ('f')
              4 MAKE_FUNCTION            0
              6 STORE_NAME               0 (f)

  4           8 LOAD_NAME                1 (print)
             10 LOAD_NAME                0 (f)
             12 CALL_FUNCTION            0
             14 CALL_FUNCTION            1
             16 POP_TOP
             18 LOAD_CONST               2 (None)
             20 RETURN_VALUE

Disassembly of <code object f at 0x103ff4150, file "<dis>", line 2>:
  3           0 LOAD_CONST               1 (1)
              2 STORE_FAST               0 (a)
              4 LOAD_CONST               0 (None)
              6 RETURN_VALUE
```

Здесь есть основной контекст выполнения, где происходит вызов функции `print`, и вложенный, который содержит информацию про функцию `f`.

Функция `count_operations` должна дать такой ответ:
```python
{
    'CALL_FUNCTION': 2,
    'LOAD_CONST': 5,
    'LOAD_NAME': 2,
    'MAKE_FUNCTION': 1,
    'POP_TOP': 1,
    'RETURN_VALUE': 2,
    'STORE_FAST': 1,
    'STORE_NAME': 1,
}
```

### Что почитать?

* Как интерпретировать глазами выхлоп `dis.dis` можно почитать на [stackoverflow](https://stackoverflow.com/a/47529318/1115624).
* Как достать инструкции - [dis.get_instructions](https://docs.python.org/3/library/dis.html#dis.get_instructions)
* Как достать имя инструкции - [opname](https://docs.python.org/3/library/dis.html#dis.Instruction.opname)
* Где найти вложеный байткод - [argval](https://docs.python.org/3/library/dis.html#dis.Instruction.argval)
* [Описание bytecode-операций](https://docs.python.org/3/library/dis.html#python-bytecode-instructions)
