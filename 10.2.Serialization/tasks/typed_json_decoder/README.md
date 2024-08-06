## Typed JSON

`json` `serialization`

### Условие

Десериализовать "типизированный" json. Внутри json-объектов может встречаться особый ключ: `"__custom_key_type__"` с именем типа. Если такой ключ есть, то остальные ключи в этом json-объекте нужно привести к указанному типу.
Возможные значения `"__custom_key_type__"`:
* `"int"`
* `"float"`
* `"decimal"`

**Важно:** В десериализованном результате ключа `"__custom_key_type__"` не должно быть. Он только пометка, о том, что нужно по особому интерпретировать тип ключей.

### Пример

```python
In [1]: from typed_json_decoder.typed_json_decoder import decode_typed_json

In [2]: decode_typed_json('{"1": "one", "__custom_key_type__": "int"}')
Out[2]: {1: 'one'}
```