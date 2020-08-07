import os
import urllib.parse

from . import settings
from .errors import ExportError


class Exporter:
    """
    Инструменты экспорта
    """
    path = settings.conf.folder
    ext = settings.conf.extension

    @staticmethod
    def _url2path(url: str, dest: str, ext: str) -> str:
        """
        Конвертирует адрес страницы в адрес файловой системы
        :param url: адрес страницы
        :param dest: путь до хранилища экспортируемых файлов
        :param ext: расширение експортируемого файла
        :return: абсолютный путь к создаваемому файлу
        """
        url = urllib.parse.unquote(url)
        parsed_url = urllib.parse.urlparse(url)
        path = parsed_url.path.strip('/')
        path = os.path.splitext(path)[0]
        path = os.path.extsep.join([path, ext])
        path = path.split('/')

        host = parsed_url.hostname.replace('www.', '')
        return os.path.abspath(os.path.join(dest, host, *path))

    @staticmethod
    def to_file(url, content) -> str:
        """
        Экспорт в файл
        :param url: адрес страницы
        :param content: текст для сохранения
        :return: абсолютный путь к созданному файлу
        """
        filename = Exporter._url2path(url, Exporter.path, Exporter.ext)
        try:
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
            with open(filename, 'w', encoding='utf8') as f:
                f.write(content)
        except BaseException as ex:
            raise ExportError(filename, str(ex))

        return filename
