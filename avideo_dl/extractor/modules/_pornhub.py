import urllib.request
import re
import os
import http
from datetime import datetime
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from avideo_dl.utils import headers


class PornhubExtractor(object):
    @classmethod
    def get_video_url(cls, url):
        while True:
            try:
                request = urllib.request.Request(url=url, headers=headers())
                html = urllib.request.urlopen(request).read().decode('utf-8')
            except http.client.IncompleteRead:
                continue
            else:
                break
        title = next(iter(os.path.basename(__file__).split('.'))) + datetime.now().strftime('%Y%m%d%H%M%S')
        video_url = re.findall(
            r'(?<=videoUrl":").*?480P.*?(?=")', str(html))[0].replace('\\', '')
        return video_url, title + datetime.now().strftime('%Y%m%d%H%M%S')
