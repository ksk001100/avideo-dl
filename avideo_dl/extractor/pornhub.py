import urllib.request
import re
from datetime import datetime

from avideo_dl.extractor.base import BaseExtractor

class PornhubExtractor(BaseExtractor):
    @classmethod
    def get_video_url(cls, url):
        request = urllib.request.Request(url=url, headers=cls.headers)
        html = urllib.request.urlopen(request).read().decode('utf-8')
        title = re.findall(r'(?<=inlineFree">).*?(?=<)', html)[0]
        video_url = re.findall(
            r'(?<=videoUrl":").*?480P.*?(?=")', str(html))[0].replace('\\', '')
        return video_url, title + datetime.now().strftime('%Y%m%d%H%M%S')