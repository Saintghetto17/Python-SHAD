## Contributing guide

Мы рады всем вашим идеям, правкам ридми, новым тестам и всему чего угодно!  

## Последовательность действий
1. Точно сформулируйте в чем именно возникает проблема или ошибка, что вы хотите добавить или изменить. 
2. Попробовать придумать как исправить эту ошибку или какие тесты нужно добавить
3. Делаем Issue или Merge Request

### Создаём issue 
Если ну никак не получается придумать решение ошибки или новую задачку, то 
1. Заходим [public repo](https://gitlab.manytask.org/python/public-2023-fall) -> Issues 
2. New issue 
3. Оформляем - описываем проблему или идею, приводим примеры, объясняем тонкие моменты и тд.


### Делаем Merge Request 
Если у вас есть идея как исправить или что добавить - круто!  

1. Синхронизуйте свой репозиторий с нашим:
```bash
git pull upstream main
```
2. Создайте **новую** ветку для merge request'а:  
ВАЖНО: Название ветки должно включать слово `contributing`, например `contributing-fixed-hello-world-test`;  
Иначе у вас просто запустятся тесты как будто вы сдаёте задачки. 
```bash
git checkout -b <your-contributing-branch-name> upstream/main
```
3. Внесите изменения и закоммитьте:
```bash
git add <changed-files>;
git commit -m <good-message>
```
4. Отправьте изменения в свой гитлаб-репозиторий:
```bash
git push origin <your-contributing-branch-name>
```
5. Зайдите в свой репозиторий на [gitlab.manytask.org](gitlab.manytask.org), нажмите слева на панели `Merge Requests -> New merge request`
6. Выберите `source branch`: имя вашего репозитория + имя вашей ветки <your-contributing-branch-name>
7. Выберите `target branch`: python/public-2023-fall + main
8. Нажмите `Compare branches and continue`
9. Задайте название и описание вашего реквеста. Внизу страницы посмотрите изменения (вкладка Changes), если все ок, то жмите `Submit merge request`

## Что потом?
* Мы посмотрим реквест, напишем комментарии, если они у нас будут. Вы можете продолжать вносить изменения и коммитить их прямо в этот реквест (обновится автоматически), пока остаетесь в нужной ветке
* В любой момент вы можете переключиться обратно на код ваших задачек, и работать с ними:
```bash
git checkout main
```
или переключиться обратно на ваш реквест, и внести в него изменения:
```bash
git checkout <your-contributing-branch-name>
```
* Когда ваш реквест будет принят и смерджен, можно удалить ветку:
```bash
git branch remove <your-contributing-branch-name>
```
