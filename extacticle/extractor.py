import urllib.parse
import urllib.request

import bs4

import config
from .errors import ExtractFailed, RequestError
from .node import Node


class Extractor:
    container_tags = config.CONTAINER_TAGS

    def __init__(self, url):
        """
        Реализует логику извлечения "полезной" части страницы
        :param url: адрес страницы
        """
        self._targets = []
        self._target = None
        self._soup = None
        self._title = None
        self._url = url
        self._convert_links()
        self._fill_targets()

    title = property(fget=lambda self: self.soup.find('head').find('title').text)
    url = property(fget=lambda self: self._url)

    @property
    def soup(self) -> bs4.BeautifulSoup:
        if self._soup is None:
            try:
                content = urllib.request.urlopen(self.url).read()
            except BaseException as ex:
                raise RequestError(self.url, str(ex))
            soup = bs4.BeautifulSoup(content, 'html.parser')
            self._soup = soup
        return self._soup

    @property
    def target_node(self) -> Node:
        """
        Получить целевой контейнер страницы.
        В случае неудачной попытки извлечения генерируется исключение ExtractFailed
        :return: Node
        """
        try:
            return self._targets[0]
        except:
            raise ExtractFailed()

    def _convert_links(self):
        """
        Преобразует относительные ссылки в глобальные
        :return:
        """
        for a in self.soup.find_all('a', href=True):
            if a.get('href') and '://' not in a.get('href'):
                a['href'] = urllib.parse.urljoin(self.url, a['href'])

    def _fill_targets(self):
        """
        Извлечение узлов, имеющих потенциал полезности
        :return:
        """
        self._targets = []
        body = self.soup.find('body')
        self._trim(body)
        self._targets.sort(reverse=True)

    def _trim(self, root: bs4.Tag):
        """
        В результате выполнения формируется список объектов Node, реализующих интерфейс работы с 'полезным' текстом
        :param root: локальный корень дерева
        """
        for child in root.find_all(recursive=False):
            self._trim(child)
            if child.name in self.container_tags:
                child.extract()
                node = Node(child, tittle=self.title)
                if node.accord_trait > 0:
                    self._targets.append(node)
