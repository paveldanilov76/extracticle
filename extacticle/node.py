import re
import textwrap

import bs4

import config
from .formatter import TagFormatter


class Node:
    content_tags = config.CONTENT_TAGS
    trait_pattern = config.TRAIT_PATTERN
    width = config.MAX_WIDTH

    def __init__(self, item: bs4.Tag, tittle=''):
        """
        Объект реализующий интерфейс потенциального целевого узла страницы
        :param item: объект bs4.Tag
        :param tittle: заголовок страницы
        """
        self._item = item
        self._tittle = tittle
        self._payload = None
        self._accord_trait = None
        self._text = None

    def __lt__(self, other):
        return self.accord_trait < other.accord_trait

    def __str__(self):
        return '{} of {} pcs'.format(self._item.name, len(self.payload))

    @property
    def text(self) -> str:
        """
        Строковое представление целевого узла
        :return: str
        """
        if self._text is None:
            soup = bs4.BeautifulSoup(str(self._item), 'html.parser')
            for tag_name in self.content_tags:
                reformat_function = TagFormatter.of(tag_name)
                for child in soup.findAll(tag_name):
                    reformat_function(child, soup)
            [br.replace_with('\n') for br in soup.find_all('br')]

            text = re.sub('\r', '', soup.text)
            if self._tittle:
                text = '\n\n'.join([self._tittle, text])
            text = '\n'.join(textwrap.fill(x, width=self.width) for x in text.split('\n'))
            self._text = text

        return self._text

    @property
    def accord_trait(self) -> int:
        """
        Характеристика соответствия шаблону поиска
        :return: количество вхождений шаблона
        """
        if self._accord_trait is None:
            self._accord_trait = len(re.findall(self.trait_pattern, self._item.text))
        return self._accord_trait

    @property
    def payload(self) -> list:
        """
        Список тэгов, входящих в целевой узел
        :return: list<bs4.Tag>
        """
        if self._payload is None:
            self._payload = list(self._item.find_all(self.content_tags, recursive=False))
        return self._payload

    @property
    def parent(self) -> bs4.Tag:
        """
        Контейнер, содержащий целевой узел
        :return: bs4.Tag
        """
        return self._item.parent
