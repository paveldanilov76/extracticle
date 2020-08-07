import argparse
import logging
import os
import sys
from pathlib import Path

import yaml

TRAIT_PATTERNS = [r'\s*[^.!?]*[.!?]', r'\b\w+\b']


parser = argparse.ArgumentParser()
parser.add_argument('urls', type=str, action='store', nargs='+', help='адрес страницы (можно несколько через пробел)')
parser.add_argument('-c', '--config', type=open,
                    help='файл конфигурации (имеет приоритет по отношению к передаваемым параметрам')
parser.add_argument('-p', '--pattern', type=int, choices=range(0, len(TRAIT_PATTERNS)), default=1,
                    help='качество текста определяется по количеству: 0 - предложений; 1 - слов; '
                         'игнорируется при указании [-cp|--custom_pattern]')
parser.add_argument('-cp', '--custom_pattern', type=str, help='кастомный шаблон поиска', default=None)
parser.add_argument('-w', '--width', type=int, help='ширина текста', default=80)
parser.add_argument('-f', '--folder', type=str, help='путь для сохранения результата',
                    default=os.path.join(str(Path.home()), 'Documents', 'articles'))
parser.add_argument('-ext', '--extension', type=str, help='тип выходного файла', default='txt')
parser.add_argument('-v', '--verbose', action='store_true', help='вывод в консоль')
parser.add_argument('--config_example', action='store_true', help='сгенерировать пример файла конфигурации')

try:
    args = parser.parse_args()
except BaseException as ex:
    logging.error(ex)
    sys.exit(1)


class Config:
    def __init__(self):
        self.urls = args.urls
        if args.custom_pattern:
            self.trait_pattern = args.custom_pattern
        else:
            self.trait_pattern = TRAIT_PATTERNS[args.pattern]
        self.max_width = args.width
        self.excluded_tags = ['header', 'footer', 'aside', 'nav', 'iframe', 'figure']
        self.included_tags = ['article', 'div', 'main', 'section']
        self.excluded_attr = [{'id': 'ChooserPanel'}, {'class': 'footer'}]
        # self.included_attr = [{'id': 'main-tga'}, {'id': 'main-itd'}]
        self.included_attr = []
        self.folder = args.folder
        self.extension = args.extension
        self.user_agent = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'

        if args.config:
            data = yaml.load(args.config, Loader=yaml.Loader)
            for key in data:
                if hasattr(self, key):
                    self.__setattr__(key, data[key])

    def serialize(self) -> dict:
        return {attr: getattr(self, attr) for attr in dir(self)
                if not attr.startswith('__') and not attr.endswith('__') and not callable(getattr(self, attr))}


conf = Config()

if args.config_example:
    print(yaml.dump(conf.serialize()))
    sys.exit(0)

logging.basicConfig(format=u'%(message)s', level=logging.DEBUG if args.verbose else logging.INFO, stream=sys.stdout)