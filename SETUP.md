## Setup guide

Дальше описаны шаги, которые вам нужно предпринять, для того чтобы получать новые задачки, решать их и отправлять на проверку.

Вам нужно будет пройти следующие шаги:
- [Регистрация](#register)
- [Преднастройка системы](#pre)
- [Настройка git репозитория](#git)
- [Установка питона и пакетов](#install)
- [Настройка IDE](#ide)
- [Сдача заданий](#send)
- [Доступ к лекциям](#lectures)

---

### Регистрация <a id='register'/>

#### Регистрация на manytask

Прежде всего вам надо зарегистрироваться на [py.manytask.org](https://py.manytask.org/).

Если вы уже регистрировались в системе manytask на других курсах ШАД, например, курс С++, то у вас уже есть аккаунт, и можно просто нажать "Login".

Если вы не помните или не уверены, то можете попробовать зарегистрироваться, и в случае, если такой пользователь уже
имеется, получите сообщение об ошибке: "Email has already been taken". В таком случае тоже смело жмите "Login".

Кодовое слово, необходимое при регистрации, смотрите в [lms](https://lk.yandexdataschool.ru/courses/2022-autumn/7.1090-iazyk-python/).

Далее вы попадете на [gitlab.manytask.org](https://gitlab.manytask.org/), где должны будете залогиниться, используя логин-пароль, который вы вводили в форму регистрации ранее.
Если вы проходили эту процедуру ранее для других курсов, и гитлаб вас помнит, то этот шаг автоматически будет пропущен.

В итоге вы должны попасть на главную py.manytask.org:
<img src="https://i.imgur.com/FYDgaWj.png" width=600/>


#### Связь аккаунта в личном кабинете и manytask 

После этого не забудьте привязать свой аккаунт в lms и gitlab.manytask.org.  
Вам нужно пройти следующие шаги:  
lk -> профиль -> аккаунты -> подключить manytask
Кнопка должна загореться зелёным. В этом случая ваша оценка будет выставлена в lk в конце курса.  

### Преднастройка <a id='pre'/>

<details><summary><a>MacOS</a></summary>

В MacOS не хватает менеджера пакетов для удобно установки чего-либо (по типу apt-get).

Поэтому нужно установить `brew` по [официальной инструкции](https://brew.sh/).
```shell
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
</details>

<details><summary><a>Windows</a></summary>

В Windows 10 появилась такая фича как WSL: Windows Subsystem for Linux,
с её помощью можно запускать Linux-приложения на Windows.
Мы рекомендуем воспользоваться ею, и в дальнейшем следовать инструкциям,
как будто бы у вас стоит операционная система Linux.

Установить `wsl` нужно по [официальной инструкции](https://docs.microsoft.com/ru-ru/windows/wsl/install-win10)

При выборе операционной системы Linux берите Ubuntu 18.04 или 22.04.

Запустите установленную систему. При входе вы окажетесь в директории `/home/<username>`;
для того, чтобы иметь возможность работать с кодом из самой Windows (например, в PyCharm),
мы рекомендуем размещать директорию с задачами по адресу `"/mnt/c/Users/<username>/My Documents"`,
которая в самой Windows доступна по адресу `C:\Users\<username>\My Documents`.

Перейдите в указанную директорию:
```bash
$ cd "/mnt/c/Users/<username>/My Documents"
```
Следуйте по инструкции дальше

</details>

### Настройка git репозитория <a id='git'/>

Вся работа по получению, решению и сдаче заданий происходит через git репозиторий. Для начала нужно его получить, скачать и настроить доступ.
О том, что такое гит, и как вообще с ним работать, мы рассказывали в [лекции про гит](https://yadi.sk/i/YUe3SJYo11EChA).

#### Установка необходимого 

Нам нужно установить ssh-keygen (если его нет) и git.
С некоторой вероятностью они уже стоят, проверить можно так: 
```shell
$ git --version
$ ssh-keygen --help
```
Если же нет, то устанавливаем
<details><summary><a>Linux</a></summary>

Если у вас Ubuntu/Debian, то всё просто:

```bash
# Если не стоит ssh-keygen:
$ sudo apt-get install openssh-client
```
```bash
$ sudo apt-get install git
```

Если у вас другой дистрибутив, то думается, вы и сами знаете, как в нем поставить пакет.
</details>

<details><summary><a>MacOS</a></summary>

В MacOS по-умолчанию уже установлен `ssh-keygen`, а если вы ставили `xcode`, то и `git`

Если же вам хочется поставить git отдельно, то ставим его через brew:
```bash
$ brew install git
```

</details>


#### Создание ssh-ключа
Можно почитать [туториал гитлаба](https://docs.gitlab.com/ce/user/ssh.html) о том как создать и добавить в аккаунт ssh ключ, а можно проследовать инструкции ниже. 
Если вы используете инструкцию гитлаба, не забудьте пройти также по ссылке [declare what host](https://gitlab.manytask.org/help/ssh/README#working-with-non-default-ssh-key-pair-paths), 
где описано как указать какой ключ использовать для подключения к гитлабу.

Если же вы уже были участником других курсов с manytask, то, скорее всего, этот ключ у вас уже есть и 
или можно создать дополнительный или использовать старый (см. пункт "Как проверить себя?")

Если вы не делали по инструкции гитлаба:
- Воспользуйтесь `ssh-keygen` (возможно, вам придется поставить `openssh-client`), затем скопируйте **.pub** ключ:
  ```bash
  # Создаем ключ:
  $ ssh-keygen -t ed25519 -f ~/.ssh/manytask_ed25519
  # Обратите внимание, что вы можете не указывать пароль для ключа,
  # чтобы не приходилось его потом вводить на каждое действие c ключом
  # Это стандартная практика, хотя и не очень безопасная
  
  # Выводим содержимое **публичного** ключа в консоль:
  $ cat ~/.ssh/manytask_ed25519.pub
  ...
  # Его надо просто скопировать, как есть, включая подпись - обычно это "ваш-логин@имя-устройства"
  # ВАЖНО! Публичным ключом можно делиться, приватным (то же имя, без .pub на конце) - никогда,
  # иначе злоумышленник сможет представиться вами
  ```

  <details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/FMHgxsL.png" width=800/></details></br>

- Идете на [gitlab.manytask.org](https://gitlab.manytask.org/)

- Жмете на иконку с вашим профилем в правом верхнем углу -> `Settings` -> слева жмете на `SSH keys`

- Вставляете ключ в формочку, жмете "Add key"

  <details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/CSPBoGp.png" width=800/></details></br>

- Создайте ssh-config с таким содержимым, чтобы при подключении к `gitlab.manytask.org` использовался ваш новый ключ:
  ```bash
  $ cat ~/.ssh/config
  Host gitlab.manytask.org
      IdentityFile ~/.ssh/manytask_ed25519
  ```
  Создать файл можно с помощью редактора `nano`, если он установлен
  ```bash
  $ nano ~/.ssh/config
  ```
  Затем нужно вставить в файл содержимое и нажать ctrl + O для сохранения и ctrl + X для выхода из редактора.
  
  Либо с помощью команды 
  ```bash
  $ echo $'Host gitlab.manytask.org\n\tIdentityFile ~/.ssh/manytask_ed25519' > ~/.ssh/config
  ```

<details><summary><a>Как проверить себя?</a></summary>

Из консоли выполнить:
```bash
$ ssh git@gitlab.manytask.org
# Вывод должен быть примерно таким:
PTY allocation request failed on channel 0
Welcome to GitLab, @hiverus!
Connection to gitlab.manytask.org closed.
```
</details>

Если что-то не получилось - обращайтесь в чатик.

#### Клонирование и настройка репозитория

```bash
# Переходим в директорию, где вы хотите разместить репозиторий с задачами,
# обычно это домашняя директория - `/home/<username>` или /Users/<username>, она же обозначается как `~` (это тильда, если что)
$ cd <твоя выбранная директория>

# Клонируем свой репозиторий с gitlab.manytask.org (создается автоматически при регистрации)
# Имя репозитория доступно по ссылке "MY REPO" на py.manytask.org
$ git clone git@gitlab.manytask.org:python/students-fall-2023/<твой репозиторий>

# Переходим в директорию склонированного репозитория
$ cd <твой репозиторий>

# Настраиваем гит так, чтобы он знал нас "в лицо"
$ git config --local user.name "<твой логин с py.manytask.org>"
$ git config --local user.email "<твой емейл с py.manytask.org>"

# Настраиваем возможность получать обновления из публичного репозитория с задачами
$ git remote add upstream git@gitlab.manytask.org:python/public-2023-fall.git
```

### Установка интерпретатора и пакетов <a id='install'/>

Мы используем версию питона `3.11.5`.  
NB: Если у вас будет стоять другая версия питона мы не может гарантировать корректную работу всех задач и тестов.  

Сейчас вам нужно будет 
1. поставить [pyenv](https://github.com/pyenv/pyenv) (менеджер версий питона, позволяет одновременно иметь на компьютере несколько версий и переключаться между ними) 
2. создать [venv](https://docs.python.org/3/library/venv.html) (модуль для создания нескольких "virtual environments" с разными установленными библиотеками на одной конкретной версии питона).

Т.е. вы можете иметь несколько версий питона и в каждой из них иметь несколько разных сред с разными установленными пакетами.

Причем venv можно установить как в папку с проектом, так и общую папку на несколько проектов. Но так как у нас самодостаточный курс и всё используется в одном месте - мы будем использовать папку с проектом. 


- Поставьте pyenv [по инструкции](https://github.com/pyenv/pyenv#installation)  
  ВНИМАНИЕ: Откройте инструкцию и сделайте всё что написано в ней. Основные ошибки тоже описаны там.
  
  <details><summary><a>Linux</a></summary>

  ```bash
  # ДО этого установите всё что просит pyenv из инструкции выше!
  $ curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
  ```
  Будет много текста, который, скорее всего, закончится 
  ```bash
  WARNING: seems you still have not added 'pyenv' to the load path.
  
  # Load pyenv automatically by adding
  # the following to ~/.bashrc:
  
  $ export PATH="$HOME/.pyenv/bin:$PATH"
  $ eval "$(pyenv init -)"
  $ eval "$(pyenv virtualenv-init -)"
  ```

  Если при попытке установить питон вы получите ошибку в духе `bash: pyenv: command not found`, то нужно выполнить первую из команд, предлагаемых pyenv'ом, где задается PATH. Имейте в виду, что изменения команд в `~/.bashrc`, `~/.profile` и других подобных файлах – вступают в силу только после перезапуска терминала.

  </details>

  <details><summary><a>MacOS</a></summary>

  ```bash
  # ДО этого установите всё что просит pyenv из инструкции выше!
  $ brew install pyenv
  ```
  </details>

  <details><summary><a>Windows</a></summary>
  
  Выполняйте инструкцию для `Linux` в консоли WSL.
  Если под WSL не находится `llvm`, то можно взять `llvm-6.0-runtime llvm-6.0-dev`
  </details>

- Установите нужную версию питона
  ```bash
  $ pyenv install 3.11.5
  ```
  Если при установке возникают ошибки, то поставьте нужные пакеты в зависимости от вашего дистрибутива,
  следуя [этой инструкции](https://github.com/pyenv/pyenv/wiki/Common-build-problems).

- Разверните виртуальное окружение с нужной версией питона в репозитории с задачами
  ```bash
  $ cd <путь к склонированному репозиторию с задачами>
  $ ~/.pyenv/versions/3.11.5/bin/python -m venv shad_env
  ```

- Активируйте виртуальное окружение (будет активным, пока не закроете консоль, либо не выполните `deactivate`)
  ```bash
  $ source shad_env/bin/activate
  ```  
  Появится следующий префикс:
  ```bash
  (shad_env)$ ...
  ```

- Проверьте что всё активировалось и ссылки `python` и `pip` ведут на папку с `shad_env`
  ```bash
  (shad_env)$ which python
  <директория с задачками>/shad_env/bin/python
  (shad_env)$ which pip
  <директория с задачками>/shad_env/bin/pip
  ```

- Поставьте пакеты:
    * pytest для тестирования
    * flake8 для проверки на кодстайл
    * mypy для проверки типов
    * ./tools/testlib локальная библиотечка для удобства тестирования задачек 
    * другие пакеты для задачек
  
  Ставятся они через файл requirements.txt, который лежит в корне репозитория с задачками

  <details><summary><b>Для Apple Silicon M1/M2 (!)</b></summary>
  (updated fall 2022)

  Если у вас устройство на `Apple Silicon M1/M2`, то...  
  Мы НЕ гарантируем и не обещаем поддержку всего курса на такой архитектуре, но скорее всего всё будет ок.  
  Раньше было сложно установить пакеты. Из-за отличающейся архитектуры проца для части из них не было wheel (готовых пакетов), а часть не компилировалось.  
  Сейчас, кажется, большинство пакетов собираются под m1/m2 автоматически (или хотя бы компилятся)  
  
  Попробуйте установить по обычной инструкции (см. ниже).  
  Если же `pip install --upgrade` будет падать, то делаем следующее
  ```bash
  # Устанавливаем компиляторы 
  (shad_env)$ brew install openblas gfortran
  (shad_env)$ export OPENBLAS="$(brew --prefix openblas)"
  # Отдельно ставим биндинговые пакеты
  (shad_env)$ pip install cython pybind11 pythran
  # Ставим llvm, который нужен некоторым отдельным пакетам 
  (shad_env)$ brew install llvm@11
  (shad_env)$ export LLVM_CONFIG="/opt/homebrew/Cellar/llvm@11/11.1.0_2/bin/llvm-config"
  
  # Ставим отдельно llvmlite
  (shad_env)$ pip install llvmlite
  # Самое весёлое - пробуем собрать себе капризные библиотеки (это может занять время)
  (shad_env)$ pip install --no-binary :all: --no-use-pep517 [package]==[version]
  ```
  (замените `[package]==[version]` на пакет, который не может установиться и его версию из `requirements.txt`)
  </details>

  ```bash
  # установка основных зависимостей
  (shad_env)$ pip install --upgrade -r requirements.txt
  # установка локальной testlib для тестирования некоторых задачек
  (shad_env)$ pip install --upgrade --editable tools/testlib
  ```

- Проверьте версии:
  ```bash
  (shad_env)$ python --version
  Python 3.11.5
  (shad_env)$ pytest --version
  pytest 7.4.0
  (shad_env)$ flake8 --version
  6.1.0 <...>
  (shad_env)$ mypy --version
  mypy 1.5.1
  ```
  Иногда venv может криво подцеплять консольные приложения библиотек. Для уверенности используйте вызов вида 
  ```shell
  (shad_env)$ python -m pytest --version
  ```
  Который гарантированно вызовет pytest/flake8/mypy установленный в этот интерпретатор
  
<details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/hYZFUE7.png" width=800/></details></br>


### Установка и настройка IDE <a id='ide'/>

Мы рекомендуем вам воспользоваться [PyCharm](https://www.jetbrains.com/pycharm/download/).
Скачайте бесплатную Community-версию, установите и запустите.  
Проверьте, возможно ваше учебное заведение (т.ч. ШАД) предоставляет учебную лицензию на продукты JetBrains. Тогда вы можете установить Professional версию бесплатно. 

- Создайте новый проект (Create new project)
- Укажите путь до репозитория с задачами (см. пункт "Клонирование и настройка репозитория")
- Разверните меню "Project interpreter", выберите "Existing interpreter"
- Укажите путь до установленного интерпретатора: `<директория с задачками>/shad_env/bin/python`
- Подтвердите создание проекта
- [Опционально] Далее, при попытке воспользоваться дебаггером может быть необходимо зайти в Settings > Tools > Python Integrated Tools и поменять там Default Test Runner на pytest. Тогда при ПКМ на директории с задачей должен появиться пункт Debug 'pytest in \<folder name\>'. 


### Сдача заданий <a id='send'/>


#### Получаем новые задания
Для получения новых заданий надо выполнить `git pull upstream main`.  
Это загрузит последние обновления из публичного репозитория. Возможно нужно будет вмерджить изменения (см лекцию про гит)

#### Решаем задачу
Код, относящийся к отдельной задаче, находится в отдельной директории темы и задачи (`01.1.PythonTools/tasks/hello_world` и т.д.), нас будет интересовать её содержимое:
- условие задачи содержится в файле `README.md`
- заготовка с кодом задачи обычно лежит в файле с именем задачи `hello_world.py`
- публичные тесты к задаче находятся в файле `test_public.py`

<details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/4EtnZWG.png" width=800/></details>

Вам нужно дописать код в файл с именем задачи.

#### Проверяем себя из консоли
Все действия нужно производить из консоли, аналогично тому, как вы ставили нужную версию питона

```bash
$ source shad_env/bin/activate   # активируем виртуальное окружение, если не активировано
(shad_env)$ pytest 01.1.PythonTools/tasks/hello_world/  # запуск тестов
# ...
(shad_env)$ flake8 01.1.PythonTools/tasks/hello_world/  # запуск линтера и stylecheck'а
# ...
(shad_env)$ mypy 01.1.PythonTools/tasks/hello_world/    # запуск typecheck'а
```

NB: Заметьте, что запуск происходит из **корня проекта**. 
Если хочется запускать из папки с задачей, то нужно **указать путь** до `pyproject.toml` как аргумент для `pytest`/`flake8`/`mypy`. 

#### Проверяем себя из PyCharm

Аналогично возможно проверять задачи сразу в вашей IDE. Например, для PyCharm:  
Чтобы проверить pytest, можно нажать правой кнопкой на директорию с задачей и выбрать "pytest in ...".

После запуска pytest появится отдельное меню Run в котором будет список запускаемых тестов.
Любой из них можно запустить/продебажить нажав правой кнопкой мыши на него.

<details><summary>Картинка</summary>

![](https://i.imgur.com/sL0xfVa.png)

</details>

NB: В PyCharm можно настроить автоматический запуск `pytest`/`flake8`/`mypy` по кнопке тестирования, предоставляем вам возможность настроить это под себя. 
Для этого можно прочитать [официальную инструкцию](https://www.jetbrains.com/help/pycharm/pytest.html#run-pytest-test)

#### Отправляем задачу в тестирующую систему

Для этого задачу нужно просто закоммитить в ваш репозиторий и отправить в gitlab 
```bash
$ git add 01.1.PythonTools/tasks/hello_world/hello_world.py
$ git commit -m 'Add hello world task'
$ git push origin main
```

Вы можете наблюдать за результатами тестирования на странице `CI/CD -> Jobs` в своём репозитории, выбираем задачу, жмем на иконку статуса.

Там можно увидеть статусы посылок и результаты тестирования.

Выглядит это обычно так:
- Информация о последнем коммите и изменённых файлах (если в запушенных коммитах код решения задачи не был изменён, эта задача НЕ будет протестирована!)
- Для каждой тестируемой задачи (может быть несколько в одном коммите)
  - Проверка стиля (PEP8)
  - Проверка типов (type hints)
  - Поиск тестов
  - Запуск тестов и их результат

<details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/mehIkFl.png" width=800/></details>

Если хоть одна задача падает на тестах, в интерфейсе гитлаба запуск будет считаться неудавшимся (failed). Если хоть одна задача в комплекте прошла - баллы за неё поставятся в систему независимо от остальных. 


### Доступ к лекциям <a id='lectures'/>


#### Как открыть ноутбук с лекцией?

```bash
# Устанавливаем jupyter
(shad_env)$ pip install jupyter==1.0.0 jupyterlab

# Запускаем jupyter lab (рекомендуется)
(shad_env)$ jupyter lab

# Если предпочитайте классический ноутбук
(shad_env)$ jupyter notebook
```

Попадайте в меню jupyter, в левой панели можно дойти до нужной лекции и открыть её.


#### Как запустить лекцию в режиме презентации?

```bash
# Устанавливаем RISE
(shad_env)$ pip install rise>=5.7.0 jupyterlab-rise>=0.40.0

# Перезапускаем jupyter
(shad_env)$ jupyter lab
```

В jupyter появится кнопка "Enter/Exit RISE Slideshow"


#### Как подключить cell-typeсhecker?

```python
from IPython.core.magic import register_cell_magic

@register_cell_magic
def typecheck(line, cell):

    from mypy import api
    cell = '\n' + cell

    mypy_result = api.run(['-c', cell] + line.split())

    if mypy_result[0]:  # print mypy stdout
        print(mypy_result[0])

    if mypy_result[1]:  # print mypy stderr
        print(mypy_result[1])
```

```bash
# Дописываем код выше в файл typecheck.py
(shad_env)$ nano ~/.ipython/profile_default/startup/typecheck.py

# Перезапускаем jupyter
(shad_env)$ jupyter notebook
```

Для проверки типов добавить строчку `%%typecheck` в тестируемой ячейке.  
Для применения `mypy` ко всем запускаемым ячейкам можно использовать [Nb Mypy](https://pypi.org/project/nb-mypy/).
