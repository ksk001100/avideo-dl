from importlib import import_module

import avideo_dl.utils

class URLExtractor(object):
    def __init__(self, url):
        self.url = url
        self.extractor = self.__select_extractor(self.url)

    def get_video_url(self):
        return self.extractor.get_video_url(self.url)
    
    def get_page_url(self):
        return self.extractor.get_video_url(self.url)

    def __select_extractor(self, url):
        service_name = avideo_dl.utils.service_name(url)
        module_name = 'avideo_dl.extractor.' + avideo_dl.utils.snake_case(service_name)
        class_name = avideo_dl.utils.camel_case(service_name) + 'Extractor'
        return getattr(import_module(module_name), class_name)