import re
import textwrap

import bs4

from . import settings
from .formatter import TagFormatter


class Node:
    trait_pattern = settings.conf.trait_pattern
    width = settings.conf.max_width

    def __init__(self, item: bs4.Tag, tittle=''):
        """
        Объект реализующий интерфейс потенциального целевого узла страницы
        :param item: объект bs4.Tag
        :param tittle: заголовок страницы
        """
        self._item = item
        self._tittle = tittle
        self._accord_trait = None
        self._text = None

    def __lt__(self, other):
        return self.accord_trait < other.accord_trait

    @property
    def text(self) -> str:
        """
        Строковое представление целевого узла
        :return: str
        """
        if self._text is None:
            soup = bs4.BeautifulSoup(str(self._item), 'html.parser')

            for tag in soup.find_all():
                reformat_function = TagFormatter.of(tag.name)
                reformat_function(tag, soup)

            [br.replace_with('\n') for br in soup.find_all('br')]

            text = re.sub('\r', '', soup.text)
            if self._tittle:
                text = '\n\n'.join([self._tittle, text])
            text = '\n'.join(textwrap.fill(x, width=self.width) for x in text.split('\n'))
            text = re.sub(r'\n{3,}', '\n\n', text)
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
    def parent(self) -> bs4.Tag:
        """
        Контейнер, содержащий целевой узел
        :return: bs4.Tag
        """
        return self._item.parent
