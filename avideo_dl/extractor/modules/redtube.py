import urllib.request
import re
import os
from datetime import datetime


class RedtubeExtractor(object):
    @classmethod
    def get_video_url(cls, url):
        title = next(iter(os.path.basename(__file__).split('.'))) + datetime.now().strftime('%Y%m%d%H%M%S')
        html = urllib.request.urlopen(url).read().decode('utf-8')
        video_url = [h.replace('\\', '') for h in re.findall(
            r'(?<=videoUrl":").*?(?=")', html) if h != ''][0]
        return video_url, title