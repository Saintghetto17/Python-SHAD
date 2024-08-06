## FizzBuzz question

`control flow` `range` `list` `%` `job interview`

### Условие

Вернуть список чисел от 1 до n. При этом вместо чисел, кратных трем, там должно быть слово "Fizz", 
а вместо чисел, кратных пяти — слово "Buzz". Если число кратно и 3, и 5, то вместо них должно быть  слово "FizzBuzz".

* Постарайтесь написать самый простой и читабельный вариант решения
* Постарайтесь написать задачу за 5 минут и с первого раза
* Если будут проблемы с `mypy` из-за несовместимости `int` и `str`, 
то вам поможет задать для нового списка тип:
```
fizz_buzz_list: List[Union[int, str]] = []
```

### Пример

```python
In [1]: from fizz_buzz.fizz_buzz import get_fizz_buzz

In [2]: get_fizz_buzz(3)
Out[2]: [1, 2, "Fizz"]
```

### Про задачу

Классическая задача, имя которой стало нарицательным - "FizzBuzz question". 

Она используется для предварительных собеседований. Предварительные собеседования нужны потому, что
> the fact that 199 out of 200 applicants for every programming job can’t write code at all

И как говорится в одной статье про успехи в решении:
> The majority of comp sci graduates can't. 
> I've also seen self-proclaimed senior programmers take more than 10-15 minutes to write a solution.

В реальных задачах возвращать список с элементами разных типов - антипаттерн. 
Старайтесь так не делать в своем продакшен коде.


