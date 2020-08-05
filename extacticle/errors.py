class RequestError(BaseException):
    def __init__(self, url, message):
        self.url = url
        self.message = message

    def __str__(self):
        return 'Не удалось открыть страницу по адресу {}\n' \
               'Ошибка: {}'.format(self.url, self.message)


class ExtractFailed(BaseException):
    def __str__(self):
        return 'Извлечение полезного содержимого из страницы не удалось'
