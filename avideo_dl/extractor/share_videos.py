import urllib.request
import re
import os
from datetime import datetime

from avideo_dl.utils import headers
from avideo_dl.extractor.base import BaseExtractor


class ShareVideosExtractor(BaseExtractor):
    @classmethod
    def get_video_url(cls, url):
        title = next(iter(os.path.basename(__file__).split('.'))) + datetime.now().strftime('%Y%m%d%H%M%S')
        request = urllib.request.Request(url=url, headers=headers())
        html = urllib.request.urlopen(request).read().decode('utf-8')
        iframe = next(iter(re.findall(r'iframe.*?(?=>)', html)))
        next_url = next(iter(re.findall(r'(?<=src=").*?(?=")', iframe)))
        request = urllib.request.Request(url=next_url, headers=headers())
        html = urllib.request.urlopen(request).read().decode('utf-8')
        video_url = re.findall(r'(?<=source src=").*?(?=">)', html)[1]
        return video_url, title
