## Steganography tool

`cli` `steganography` `png` `setuptools` `wheel` `click`

### Условие

В этой задачке нужно собрать свой пакет простенькой LSB стенографией.  
Основные функции уже написаны за вас, нужно только обернуть это всё в маленький пакетик и написать cli.  

Про саму LSB стенографию можно почитать, например, [в посте на хабре](https://habr.com/ru/post/422593/). Кратко её можно изобразить следующим образом:
![lsb_steganography](./lsb_steganography.png)


Формально вам нужно:

* Написать консольный интерфейс чтобы можно было вызвать `steganography-tool`
* Написать установщик (`setup`)
* Проверить, что модуль собирается в `wheel` 
* Проверить, что все тесты корректно запускаются на вашем модуле


### Некоторые моменты 

Современный способ написания конфигурации к пакету: `pyproject.toml` - он требуется в этой задачке. 
Однако некоторые библиотеки ещё используют старый `setup.cfg` (тоже статическая конфигурация, довольно близкая структура) - он требуется в соседней.  
Также Вам нужно будет написать dummy `setup.py` файлик. Сейчас такая конфигурация почти не используется (и не стоит использовать без веской причины), однако такой файл из 2х строчек обеспечит совместимость со старыми версиями `pip`. 


* Весь код в папке будет установлен в тестирующую систему через `pip wheel` & `pip install`
* Обращайтесь к [официальной документации python](https://packaging.python.org/tutorials/packaging-projects/#configuring-metadata)
* В этом модуле используется библиотечка `PIL` (`Pillow`). Её **нет** в тестирующей системе, но можно прописать её в requires к модулю 
* Нужно написать свой `cli`. Для этого можно использовать _что угодно_, но мы рекомендуем [click](https://palletsprojects.com/p/click/) (тоже нет в тестирующей системе, нужно установить через реквы)
* Все сообщения нужно скрывать в картинке `lenna.png`. Чтобы получить к ней доступ после установки нужно пробросить её как `package data` 
* Тесты без установки, скорее всего, не запустятся 

### Как запустить тесты?

Перед тем, как запустить тесты, нужно установить библиотеку.

```bash
# Собрать wheel для библиотеки steganography_tool
(shad_env)$ pip wheel --wheel-dir 06.1.ModulesPackagesImport/tasks/steganography_tool/dist 06.1.ModulesPackagesImport/tasks/steganography_tool/

# Посмотреть какие файлы упаковались в wheel
(shad_env)$ tar --list -f 06.1.ModulesPackagesImport/tasks/steganography_tool/dist/steganography_tool-0.0.1-py3-none-any.whl  

# Устанавливаем собранный wheel для steganography_tool
(shad_env)$ pip install 06.1.ModulesPackagesImport/tasks/steganography_tool/ --prefer-binary --force-reinstall --find-links 06.1.ModulesPackagesImport/tasks/steganography_tool/dist/

# Стал доступен модуль steganography_tool в интерпретаторе
(shad_env)$ steganography-tool

# Теперь можете запустить тесты, которые используют модуль steganography_tool в импортах
(shad_env)$ pytest 06.1.ModulesPackagesImport/tasks/steganography_tool
```
Причем нужно переустанавливать пакет если вы меняете metadata.


### Command line interface

Нужно реализовать простенький cli. Для этого рекомендуем хорошую и модную библиотечку [click](https://palletsprojects.com/p/click/).  
Более конкретно:

* `steganography-tool` - только help и описание
* `steganography-tool encode [OUTPUT_FILENAME] [SECRET_MESSAGE]` - скрывает сообщение в `lenna.png` и сохраняет в файл
* `steganography-tool decode [INPUT_FILENAME]` - выводит найденное в файле сообщение

После установки это должно выглядеть примерно так
```bash
(shad_env)$ steganography-tool --help
(shad_env)$ steganography-tool encode --help
(shad_env)$ steganography-tool encode encoded.png secret-message 
(shad_env)$ steganography-tool decode --help
(shad_env)$ steganography-tool decode encoded.png
```


## Полезные материалы 
* [документация setuptools для pyproject.toml](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html)
* [документация python для упаковки пакетов](https://packaging.python.org/tutorials/packaging-projects/)
* [документация питон про модули](https://docs.python.org/3/tutorial/modules.html)
* [про lsb](https://habr.com/ru/post/422593/)
* [_древняя_ статья про wheels. только для общего понимания](https://habr.com/ru/post/210450/)
* [click](https://palletsprojects.com/p/click/)
