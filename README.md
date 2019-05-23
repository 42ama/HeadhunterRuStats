# Headhunter.ru Stats

Headhunter.ru Stats - набор скриптов используемых для сбора статистики об каком-то направлении или их ряде с hh.ru.

## Требования

Установленный Python последей версии и pip для сбора необходимых модулей

## Установка и настройка

Перед использованием необходимо произвести сбор необходимых модулей, запустив из директории скрипта

```bash
pip install -r requirements.txt 
```

В данный момент настройка параметров производится через hhrustats_setup.py.
```python
list_pairs_1 = [('Python', 'python'),
				('C#', 'c%23'),
				('Unity', 'unity'),
				('Data science', 'data+science'),
				('JavaScript', 'javascript'),
				(),
				('Россия', ''),
				('Санкт-Петербург', 'area=2'),
				('Самара', 'area=78'),
				(),
				('',''),
				('Нет опыта работы','experience=noExperience&from=cluster_experience&'),
				('1..3 года опыта', 'experience=between1And3&from=cluster_experience'),
				()
				]
```
Каждая запись представляет собой котреж значений: отображение в формате для человека, значение в юрл формате.
Блоки разделены между собой пустым кортежом.

Первый блок, это часть юрл ссылки связанная с параметром текст.
``` html
text=data+science
```

Последующих блоков может быть любое количество и название параметра уже включено в элемент кортежа.
``` html
area=78&experience=noExperience&from=cluster_experience&
```

В результате, в рамках работы скрипта, будет произведено сочетание элементов из каждого блока со всеми элементами других блоков и будет произведен сбор данных о количестве вакансий по ссылкам формата:
``` html
https://samara.hh.ru/search/vacancy?area=2&clusters=true&enable_snippets=true&text=Python+junior&experience=noExperience&from=cluster_experience
```

По результатам работы скрипта в папке json будет добавлен файл с текущей датой, в которым будут сохранены численные результаты сбора информации. Также, если сегодня понедельник или 1ое число месяца в папку plots, будет добавлен ряд графиков отражающих тренды за последнее время (при наличии собранных данных за соответствующие отрезки времени).

При включении тестового режима, сбор информации происходит при каждом запуске - независимо проводился ли он сегодня или нет. Также после каждого сбора будут построенны графики (при наличии собранных данных за соответствующие отрезки времени).
``` python
TESTMODE = True
```

## Запуск
Запускается вручную из каталога, с помощью команды командной строки.
```bash
python _main.py
```

Или же запустите скрипт make_bat.py, который создаст .bat-ник запускающий скрипт. .bat можно включить в автозапуск и тогда сбор информации будет регулярным и автоматическим.

```bash
python make_bat.py
```

## Dev
В папке from_dev_branch находятся два показательных файла с другой ветки - первые шаги для перевода приложения на ООП модель.

##ТуДу:
1)~~Разобраться с нерабочей обработкой данных.~~ *Вроде пока всё норм, нужны преценденты.*
2)Приделать новую модель сбора/обработки данных с dev ветки.
3)Придумать новую модель хранения данных и перевести старые на неё.
4)~~Шаг к проду 0: добавить setup.py и README.md, с описанием запуска и настройки скрипта из под питона.~~
5)Шаг к проду 1: сделать сайт на Django, и выдачу скрипта с кастомными параметрами.
6)Шаг к проду 2: сделать прогу с GUI и собрать её в инсталлер.
7)Подкрутить NLP для обработки соответствия выданной информации на запрос (к примеру на запрос Python, выходит много позиций где он лишь вспомогательный язык - сделать коррекцию вот этого).
8)Собрать все пары с hh, типа ('нет опыта','noExperience').
9)Ускорить сбор данных, путём загрузки не полного html документа, а лишь необходимой части.
10)Сделать макет дизайна в фигме.


##Сделано(с прошлого апдейта):
1)Сделать конструктор класса чтобы в него поступали аргументы для поиска(например поля для поиска text).
*Отказался от этой идеи*
2)подключить **Pandas**(пандас - это для обработки данных, балда нужен **матплотлиб**) начасть собирать данные с файлов и делать гарфики
*Подключен и настроен матплотлиб*
3)выводить это всё на аккаунт в телегу
*Телега не работает без настроенных прокси, в твиттере не дали статус разработчика на аккаунт, чтобы АПИ токен вытащить. Идея отложена из-за более насущных проблем.*
4)переделать сейв/лоад с значением по умолчанию и приходящим значением - чтобы можно было использовать в процессах сбора и обработки информации.
*Сделано.*
5)Произвести здесь уборку, привет MercDev!

## Лицензия
[MIT](https://choosealicense.com/licenses/mit/)