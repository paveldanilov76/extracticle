import argparse
import logging
import os
import sys
from pathlib import Path

import yaml

TRAIT_PATTERNS = [r'\s*[^.!?]*[.!?]', r'\b\w+\b']


parser = argparse.ArgumentParser()
parser.add_argument('urls', type=str, action='store', nargs='+', help='адрес страницы (можно несколько через пробел)')
parser.add_argument('-c', '--config', type=open, help='файл конфигурации '
                                                      '(имеет приоритет по отношению к передаваемым параметрам')
parser.add_argument('-p', '--pattern', type=int, choices=range(0, len(TRAIT_PATTERNS)), default=1,
                    help='качество текста определяется по количеству: 0 - предложений; 1 - слов;')
parser.add_argument('-w', '--width', type=int, help='ширина текста', default=80)
parser.add_argument('-f', '--folder', type=str, help='путь для сохранения результата',
                    default=os.path.join(str(Path.home()), 'Documents', 'articles'))
parser.add_argument('-ext', '--extension', type=str, help='тип выходного файла', default='txt')
parser.add_argument('-v', '--verbose', action='store_true', help='вывод в консоль')
parser.add_argument('--config_example', action='store_true', help='сгенерировать пример файла конфигурации')

args = parser.parse_args()


class Config:
    urls = args.urls
    trait_pattern = TRAIT_PATTERNS[args.pattern]
    max_width = args.width
    excluded_tags = ['header', 'footer', 'aside', 'nav', 'iframe', 'figure']
    included_tags = ['article', 'div', 'main', 'section']
    excluded_attr = [{'id': 'ChooserPanel'}, {'class': 'footer'}]
    # included_attr = [{'id': 'main-tga'}, {'id': 'main-itd'}]
    included_attr = []
    folder = args.folder
    extension = args.extension
    user_agent = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'

    def __init__(self):
        if args.config:
            data = yaml.load(args.config, Loader=yaml.Loader)
            for key in data:
                if hasattr(self, key):
                    self.__setattr__(key, data[key])

    @classmethod
    def serialize(cls) -> dict:
        return {attr: getattr(cls, attr) for attr in dir(cls)
                if not attr.startswith('__') and not attr.endswith('__') and not callable(getattr(cls, attr))}


if args.config_example:
    print(yaml.dump(Config.serialize()))
    sys.exit(0)

conf = Config()
logging.basicConfig(format=u'%(message)s', level=logging.DEBUG if args.verbose else logging.INFO, stream=sys.stdout)