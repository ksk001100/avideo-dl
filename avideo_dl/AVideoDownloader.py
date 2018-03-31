import urllib.request
import urllib.error
import sys
import threading
import os
from .extractor import URLExtractor


class AVideoDownloader(URLExtractor):
    def __init__(self, url, split_num=10):
        self.url = url
        self.split_num = split_num
        self.title = None
        self.file_type = None
        self.total_length = None
        self.file_count = 0
        self.video_url, self.title = self.get_url(url)

    def split_download(self, num, start, end):
        req = urllib.request.Request(self.video_url)
        req.headers['Range'] = 'bytes=%s-%s' % (start, end)
        while True:
            try:
                res = urllib.request.urlopen(req)
                break
            except urllib.error.HTTPError:
                req.headers.update(self.headers)
                res = urllib.request.urlopen(req)
                break
            except Exception:
                continue
        while True:
            try:
                binary = res.read()
                break
            except Exception:
                continue
        with open("%s.toyota" % num, "wb") as file:
            file.write(binary)

    def single_download(self):
        def progress(block_count, block_size, total_size):
            percentage = 100.0 * block_count * block_size / total_size
            sys.stdout.write("%.2f %% ( %d KB )\r" % (percentage, total_size / 1024))
        urllib.request.urlretrieve(self.video_url, "{}.mp4".format(self.title), progress)

    def download(self):
        try:
            info = urllib.request.urlopen(self.video_url).info()
            self.total_length = int(info.get('content-length'))
            self.file_type = info.get('content-type').split('/')[-1]
        except AttributeError:
            print('start single download')
            self.single_download()
            exit()
        total_count = 0
        threads = []
        for i, val in enumerate([(self.total_length + j) // self.split_num for j in range(self.split_num)]):
            if i == 0:
                last = val
                thread = threading.Thread(
                    target=self.split_download, args=(i, 0, last))
                threads.append(thread)
                total_count = val
            else:
                last = total_count + 1
                total_count += val
                thread = threading.Thread(
                    target=self.split_download, args=(i, last, total_count))
                threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
            self.file_count += 1
            progress = "=" * int(self.file_count)
            space = " " * (self.split_num - int(self.file_count))
            arrow = ">"
            sys.stdout.write("[{}{}{}{}%]\r".format(
                progress, arrow, space, int(self.file_count * (100 / self.split_num))))
            sys.stdout.flush()

        self.combine(self.title)

    def combine(self, file_name):
        tmp_list = []
        with open("%s.%s" % (file_name, self.file_type), "wb") as file:
            for i in range(self.split_num):
                with open('{}.toyota'.format(i), 'rb') as tmp_file:
                    tmp_list.append(tmp_file.read())
            file.write(b''.join(tmp_list))
        os.system('rm *.toyota')