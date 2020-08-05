import argparse
import logging

import extracticle


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str, help='адрес страницы для извлечения')
    args = parser.parse_args()

    try:
        extractor = extracticle.Extractor(args.url)
        node = extractor.target_node
        logging.debug(node.text)
    except BaseException as ex:
        logging.error(ex)


if __name__ == '__main__':
    run()
