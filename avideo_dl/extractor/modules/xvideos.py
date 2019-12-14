import urllib.request
import re
import os
from datetime import datetime


class XvideosExtractor(object):
    @classmethod
    def get_video_url(cls, url):
        html = urllib.request.urlopen(url).read().decode('utf-8')
        title = next(iter(os.path.basename(__file__).split('.'))) + datetime.now().strftime('%Y%m%d%H%M%S')
        video_url = re.findall(r"(?<=setVideoUrlHigh\(\').*?(?=\')", html)[0]
        return video_url, title

    @classmethod
    def get_page_url(cls, url):
        html = urllib.request.urlopen(url).read().decode('utf-8')
        page_url = re.findall(r'href=[\'"]?([^\'" >]+)', html)
        return set(filter(lambda x: re.match(r'/video\d', x), page_url))
