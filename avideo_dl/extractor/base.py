from abc import ABCMeta, abstractmethod
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class BaseExtractor(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def get_video_url(cls, url):
        pass