from importlib import import_module

import avideo_dl.utils


class URLExtractor(object):
    def __init__(self, url):
        self.url = url
        self.extractor = self.__select_extractor()

    def __getattr__(self, key):
        return getattr(self.extractor, key)(self.url)

    def __select_extractor(self):
        service_name = avideo_dl.utils.service_name(self.url)
        module_name = 'avideo_dl.extractor.modules.' + avideo_dl.utils.snake_case(service_name)
        class_name = avideo_dl.utils.camel_case(service_name) + 'Extractor'
        try:
            return getattr(import_module(module_name), class_name)
        except ModuleNotFoundError:
            print('No supported site...')
            exit()
