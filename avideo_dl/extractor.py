import urllib.request
import re


class URLExtractor(object):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
    }

    def get_url(self, url):
        if 'xvideos' in url:
            return self.__xvideos_video_url(url)
        elif 'pornhub' in url:
            return self.__pornhub_video_url(url)
        elif 'share-videos' in url:
            return self.__sharevideos_video_url(url)
        elif 'tube8' in url:
            return self.__tube8_video_url(url)
        elif 'redtube' in url:
            return self.__redtube_video_url(url)
        elif 'xhamster' in url:
            return self.__xhamster_video_url(url)
        elif 'vjav' in url:
            return self.__vjav_video_url(url)
        else:
            raise ValueError("This site is not supported.")

    def __xvideos_video_url(self, url):
        html = str(urllib.request.urlopen(url).read())
        title = re.findall(r'(?<=page-title">).*?(?=<)', html)[0]
        video_url = re.findall(r"(?<=setVideoUrlHigh\(\\').*?(?=\\')", html)[0]
        return video_url, title

    def __pornhub_video_url(self, url):
        request = urllib.request.Request(url=url, headers=self.headers)
        html = str(urllib.request.urlopen(request).read())
        title = re.findall(r'(?<=inlineFree">).*?(?=<)', html)[0]
        video_url = re.findall(
            r'(?<=videoUrl":").*?480P.*?(?=")', str(html))[0].replace('\\', '')
        return video_url, title

    def __sharevideos_video_url(self, url):
        from datetime import datetime
        title = 'share-videos' + datetime.now().strftime('%Y%m%d%H%M%S')
        request = urllib.request.Request(url=url, headers=self.headers)
        html = str(urllib.request.urlopen(request).read())
        iframe = re.findall(r'iframe.*?(?=>)', html)[0]
        next_url = re.findall(r'(?<=src=").*?(?=")', iframe)[0]
        request = urllib.request.Request(url=next_url, headers=self.headers)
        html = str(urllib.request.urlopen(request).read())
        video_url = re.findall(r'(?<=source src=").*?(?=">)', html)[1]
        return video_url, title

    def __tube8_video_url(self, url):
        request = urllib.request.Request(url=url, headers=self.headers)
        html = str(urllib.request.urlopen(request).read())
        title = re.findall(r'(?<=<span class="item">).*?(?=<)', html)[0]
        video_url = re.findall(r'(?<=videoUrl":").*?(?=")',
                               html)[0].replace('\\', '')
        return video_url, title

    def __redtube_video_url(self, url):
        html = str(urllib.request.urlopen(url).read())
        title = re.findall(r'(?<=video_title_text">).*?(?=<)', html)[0]
        video_url = re.findall(r'(?<=videoUrl":").*?(?=")',
                               html)[0].replace('\\', '')
        return video_url, title

    def __xhamster_video_url(self, url):
        html = str(urllib.request.urlopen(url).read())
        title = re.findall(
            r'(?<=entity-info-container__title" itemprop="name">).*?(?=<)', html)[0]
        video_url = re.findall(
            r'(?<="mp4":\[\{"url":").*?(?=")', html)[0].replace('\\', '')
        return video_url, title

    def __vjav_video_url(self, url):
        pass
