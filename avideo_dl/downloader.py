import os
import sys
import urllib.error
import urllib.request
from functools import reduce
from multiprocessing import Pool, Value, cpu_count

from avideo_dl.utils import headers


class Downloader(object):
    split_num = 100
    file_type = None
    total_length = None

    def __init__(self, video_url, title):
        self.video_url = video_url
        self.title = title
        print('title : {}'.format(self.title))
        print('video_url : {}\n'.format(self.video_url))

    def split_download(self, args):
        num, start, end = args
        req = urllib.request.Request(self.video_url)
        req.headers['Range'] = 'bytes=%s-%s' % (start, end)
        while True:
            try:
                res = urllib.request.urlopen(req)
                break
            except urllib.error.HTTPError:
                req.headers.update(headers())
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
        with open('{}.tmp'.format(num), 'wb') as file:
            file.write(binary)
        shared_file_count.value += 1
        self.progress_bar(shared_file_count)

    def progress_bar(self, count):
        p_count = int(100 * count.value / self.split_num)
        progress = "=" * p_count
        space = " " * (100 - p_count)
        arrow = ">"
        per = int(count.value * (100 / self.split_num))
        print("\r[{}{}{}]{}%".format(progress, arrow, space, per), end='')

    def download(self):
        try:
            info = urllib.request.urlopen(self.video_url).info()
        except urllib.error.HTTPError:
            req = urllib.request.Request(self.video_url)
            req.headers.update(headers())
            info = urllib.request.urlopen(req).info()
        except AttributeError:
            exit()
        self.total_length = int(info.get('content-length'))
        self.file_type = info.get('content-type').split('/')[-1]
        self.split_num = self.total_length // 300000

        print('Use cpu thread count: ', cpu_count())
        print('Split count: ', self.split_num, '\n')

        l = [(self.total_length + i) //
             self.split_num for i in range(self.split_num)]
        args = [(i, i * val, sum(l[:i]) + val) for i, val in enumerate(l)]

        p = Pool(processes=cpu_count() * 2,
                 initializer=self.pool_init,
                 initargs=(Value('i', 0),))
        p.map(self.split_download, args)
        p.close()
        p.join()

        with open('{}.{}'.format(self.title, self.file_type), 'wb') as f:
            self.combine(f)

        return str(round(os.path.getsize('{}.{}'.format(self.title, self.file_type)) / (1024.0**2), 1)) + 'MB'

    def pool_init(self, count):
        global shared_file_count
        shared_file_count = count

    def combine(self, file):
        file.write(reduce(lambda x, y: x + y, self.binary_files()))
        os.system('rm *.tmp')

    def binary_files(self):
        return map(lambda f: f.read(), (open('{}.tmp'.format(i), 'rb') for i in range(self.split_num)))