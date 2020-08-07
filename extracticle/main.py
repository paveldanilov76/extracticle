import logging

import extracticle
from extracticle import settings


def run():
    urls = settings.conf.urls
    if isinstance(urls, str):
        urls = [urls]
    for url in urls:
        try:
            extractor = extracticle.Extractor(url)
            nodes = extractor.target_nodes()
            text = ''
            for node in nodes:
                try:
                    logging.debug(node.text + '\n')
                    text += node.text + '\n'
                except BaseException as ex:
                    logging.error(ex)
            file = extracticle.Exporter.to_file(extractor.url, text.strip())
            logging.info('Статья сохранёна в "{}"'.format(file))
        except BaseException as ex:
            logging.error(ex)


if __name__ == '__main__':
    run()
