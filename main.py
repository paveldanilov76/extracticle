import argparse
import logging

import extracticle


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str, help='адрес страницы для извлечения')
    args = parser.parse_args()
    url = args.url

    try:
        logging.debug('Открытие страницы "{}"'.format(url))
        extractor = extracticle.Extractor(args.url)
        node = extractor.target_node
        logging.debug('\n' + node.text)
        file = extracticle.Exporter.to_file(extractor.url, node.text)
        logging.info('Статья сохранёна в "{}"'.format(file))
    except BaseException as ex:
        logging.error(ex)


if __name__ == '__main__':
    run()
