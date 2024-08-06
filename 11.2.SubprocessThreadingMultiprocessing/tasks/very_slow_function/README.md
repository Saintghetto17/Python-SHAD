## Очень медленная функция

`threading.Thread` `multiprocessing.Pool`

### Условие

Дана Очень Медленная Функция (`very_slow_function`), которая вычисляет квадрат числа приблизительно за 0.3 с.

Необходимо реализовать три функции, использующие `very_slow_function`.
Они должны принимать на вход число `bound`, а возвращать возведенные в квадрат числа на полуинтервале [0; `bound`):
1. `calc_squares_simple(bound)` — в один поток
2. `calc_squares_multithreading(bound)` — с использованием `threading.Thread`
3. `calc_squares_multiprocessing(bound)` — с использованием `multiprocessing.Pool`

В тесте `test_speed` выводится время работы каждой из этих функций.
Необходимо, чтобы функция `calc_squares_multiprocessing` работала быстрее`calc_squares_simple`.
