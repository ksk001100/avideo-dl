from abc import ABCMeta, abstractmethod
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class BaseExtractor(metaclass=ABCMeta):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
    }

    @classmethod
    @abstractmethod
    def get_video_url(cls, url):
        pass