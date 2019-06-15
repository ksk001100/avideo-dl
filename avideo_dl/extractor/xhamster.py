import urllib.request
import re
import json
from datetime import datetime

from avideo_dl.extractor.base import BaseExtractor

class XhamsterExtractor(BaseExtractor):
    @classmethod
    def get_video_url(cls, url):
        html = urllib.request.urlopen(url).read().decode('utf-8')
        title = re.findall(
            r'(?<=entity-info-container__title" itemprop="name">).*?(?=<)', html)[0]
        video_urls = json.loads(re.findall(r'(?<=},"sources":).*?(?<=})', html)[0])
        if video_urls.get('720p'):
            video_url = video_urls['720p']
        elif video_urls.get('480p'):
            video_url = video_urls['480p']
        else:
            video_url = video_urls['240p']
        return video_url, title + datetime.now().strftime('%Y%m%d%H%M%S')