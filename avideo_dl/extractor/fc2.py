import urllib.request
import re
from datetime import datetime

from avideo_dl.extractor.base import BaseExtractor

class Fc2Extractor(BaseExtractor):
    @classmethod
    def get_video_url(cls, url):
        html = urllib.request.urlopen(url).read().decode('utf-8')
        title = re.findall(r'(?<=page-title">).*?(?=<)', html)[0]
        video_url = re.findall(r"(?<=setVideoUrlHigh\(\').*?(?=\')", html)[0]
        return video_url, title + datetime.now().strftime('%Y%m%d%H%M%S')
