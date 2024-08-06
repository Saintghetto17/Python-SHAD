## CAESAR CIPHER

`str.maketrans`

### Условие

Напишите функцию `caesar_encrypt`, шифрующую переданную ей строку [алгоритмом Цезаря](https://ru.wikipedia.org/wiki/%D0%A8%D0%B8%D1%84%D1%80_%D0%A6%D0%B5%D0%B7%D0%B0%D1%80%D1%8F) с ключом `n`.
Не забудьте правильно обработать строчные и прописные буквы.

Функция принимает 2 параметра:
- строчку, которую надо зашифровать
- целое число, которое может быть и отрицательным – ключ шифра

### Пример
```
>>> caesar_encrypt('This is stupid song stupid stupid stupid song', 10)
'Drsc sc cdezsn cyxq cdezsn cdezsn cdezsn cyxq'
```
