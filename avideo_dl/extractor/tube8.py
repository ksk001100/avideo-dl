import urllib.request
import re
from datetime import datetime

from avideo_dl.extractor.base import BaseExtractor

class Tube8Extractor(BaseExtractor):
    @classmethod
    def get_video_url(cls, url):
        html = urllib.request.urlopen(url).read().decode('utf-8')
        title = re.findall(r'(?<=video_title_text">).*?(?=<)', html)[0]
        video_url = [h.replace('\\', '') for h in re.findall(
            r'(?<=videoUrl":").*?(?=")', html) if h != ''][0]
        return video_url, title + datetime.now().strftime('%Y%m%d%H%M%S')