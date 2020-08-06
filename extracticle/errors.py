class Error(BaseException):
    pass


class RequestError(Error):
    def __init__(self, url, err):
        super(RequestError, self).__init__(
            'Не удалось открыть страницу по адресу {}\n'
            'Ошибка: {}'.format(url, err)
        )


class ExtractFailed(Error):
    def __init__(self):
        super(ExtractFailed, self).__init__('Извлечение полезного содержимого из страницы не удалось')


class ExportError(Error):
    def __init__(self, file, err):
        super(ExportError, self).__init__(
            'Не удалось сохранить файл "{}"\n'
            'Ошибка: {}'.format(file, err)
        )
