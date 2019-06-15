import urllib.request
import re
from datetime import datetime

from avideo_dl.extractor.base import BaseExtractor


class ShareVideosExtractor(BaseExtractor):
    @classmethod
    def get_video_url(cls, url):
        title = 'share-videos' + datetime.now().strftime('%Y%m%d%H%M%S')
        request = urllib.request.Request(url=url, headers=cls.headers)
        html = urllib.request.urlopen(request).read().decode('utf-8')
        iframe = re.findall(r'iframe.*?(?=>)', html)[0]
        next_url = re.findall(r'(?<=src=").*?(?=")', iframe)[0]
        request = urllib.request.Request(url=next_url, headers=cls.headers)
        html = urllib.request.urlopen(request).read().decode('utf-8')
        video_url = re.findall(r'(?<=source src=").*?(?=">)', html)[1]
        return video_url, title