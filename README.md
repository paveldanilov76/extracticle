# Article Extractor (extracticle)

## Распространение
* распространяемый пакет *.whl
* исполняемы файл *.exe

## Установка
    pip install path/to/file/extracticle-1.0-py3-none-any.whl
    
## Использование
* при установке с помощью [pip](#Установка):
        
        extracticle [-h] [-c CONFIG] [-p {0,1}] [-w WIDTH] [-f FOLDER] [-ext EXTENSION] [-v] [--config_example] urls [urls ...]

    Пример:
        
        extracticle https://news.ngs.ru/text/gorod/2020/08/07/69408655/

* при использовании исполняемого модуля:

        extracticle.exe
        > [-h] [-c CONFIG] [-p {0,1}] [-w WIDTH] [-f FOLDER] [-ext EXTENSION] [-v] [--config_example] urls [urls ...]
        ...
        > [-h] [-c CONFIG] [-p {0,1}] [-w WIDTH] [-f FOLDER] [-ext EXTENSION] [-v] [--config_example] urls [urls ...]
        ...

## Описание:
Сервис, извлекающий полезный контент с новостных ресурсов.

Алгоритм извлечения заключается в следущем:
1. В качестве обязательного параметра передаётся URL-адрес ресурса (или несколько через пробел), по которому запрашивается страница. 

2. Из тела страницы извлекаются все [запрещённые контейнеры](#Разрешённые-и-запрещенные-контейнеры).

3. Рекурсивно обходятся все [обязательные(если таковые перечислены) или разрешённые контейнеры](#Разрешённые-и-запрещенные-контейнеры), начиная c нижнего уровня.
Контейнеры, в которых встречается хотябы одно вхождение [шаблона поиска](#Шаблоны-поиска), извлекается из дерева и помещаются в стек.

4. Контейнер из стека, имеющий наибольшее количество вхождений [шаблона поиска](#Шаблоны-поиска) считается целевым.
В случае указания [обязательных](#Разрешённые-и-запрещенные-контейнеры) контейнеров - целевыми являются все контейнеры стека.

5. В вывод помещается текст из всех целевых контейнеров. Ширина выводимого текста регулироуется параметром 
[--width](#Параметры) (по умолчанию - 80 символов).

6. Выводимый текст записывается в файл в директорию, указанную в [*--folder*](#Параметры).

#### Разрешённые и запрещенные контейнеры
Все контейнеры делятся на три типа:
1. **запрещённые** - определяются нахождением названия тега в списке *excluded_tags* 
или совпадением атрибутов узла с перечисленными в списке *excluded_attr*
2. **разрешённые** - определяются нахождением названия тега в списке *included_tags*
3. **обязательные** - определяются совпадением атрибутов узла с перечисленными в списке *included_attr*

**Списки *excluded_tags*, *included_tags*, *excluded_attr* и *included_attr* указываются только в 
[файле](#Файл-конфигурации), передача их через [параметры](#Параметры) невозможна!**

#### Шаблоны поиска
Шаблоны реализуют поиск слов или предложений, в зависимости от передаваемого параметра [--pattern](#Параметры) или [--custom_pattern](#Параметры).
+ предложения, если *[--pattern](#Параметры) = 0 (значение по умолчанию)*
+ слова, если *[--pattern](#Параметры) = 1*
+ значение [--custom_pattern](#Параметры) (если указан)

#### Параметры
* -c или --config - путь до [файла конфигурации](#Файл-конфигурации).
* -p или --pattern - использование стандартного шаблона поиска (игнорируется если указан --custom_pattern). По умолчанию - 1.
* -cp или --custom_pattern - использование кастомного шаблона поиска. Необязательный.
* -w или --width - максимальная ширина строки для выводимого текста. По умолчанию - 80 символов.
* -f или --folder - путь размещения извлечённых статей. По умолчанию - "Документы -> acrticles".
* -ext или --extension - расширение результирующего файла. По умолчанию - "txt".
* -v или --verbose - вывод лога в консоль, если указан (необязательный).
* --config_example - вывод в консоль стандартного файла конфигурации, если указан.

#### Файл конфигурации
Файл с расширеним *.yaml.

При указании [--config](#Параметры) все содержащиеся в указанном файле параметры переопределяются.

Стандартный файл выглядит так:

    trait_pattern: 1
    max_width: 80
    folder: 'C:\articles'
    extension: 'txt'
    user_agent: 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'
    excluded_tags: ['header', 'footer', 'aside', 'nav', 'iframe', 'figure']
    included_tags: ['article', 'div', 'main', 'section']
    excluded_attr: [{'id': 'ChooserPanel'}, {'class': 'footer'}]
    # included_attr: [{'id': 'main-tga'}, {'id': 'main-itd'}]
    included_attr: []
    
## Опробация проводилась на следующих ресурсах:
* https://lenta.ru/news/2020/08/04/50/
* https://lenta.ru/news/2020/08/07/udar/
* https://www.gazeta.ru/business/news/2020/08/06/n_14765683.shtml
* https://www.gazeta.ru/business/news/2020/08/07/n_14767591.shtml
* https://www.kommersant.ru/doc/4443776
* https://www.kommersant.ru/doc/4443404
* https://www.vesti.ru/article/2437523
* https://lenta.ru/news/2020/07/20/zakaz/
* https://www.bbc.com/russian/news-53687887
* https://www.bbc.com/news/uk-53687740
* https://sbis.ru/news/ofd/64865ff6-b3a9-430f-a81d-9b7d107d3733
* https://sbis.ru/news/ereport/e7a147fe-f90d-4436-8e81-287a9af3c50c

Результат представлен в [extracticle/articles](https://github.com/paveldanilov76/extracticle/tree/master/articles)

## Потенциальные улучшения
* Возможность экспорта статей в формат *.pdf, для возможности отображения изображений
* Реализация Web-приложения для вывода извлечённых статей на web-странице вместе с изображениями, видео и т.д, относящимися из контекста статей
   
