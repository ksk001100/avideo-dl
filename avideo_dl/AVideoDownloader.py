import urllib.request
import urllib.error
import sys
from threading import Thread
from multiprocessing import cpu_count
from queue import Queue
import os
from .extractor import URLExtractor


class AVideoDownloader:
    def __init__(self, url):
        """Initialization
        :param str url: Video site URL
        :param int split_num: Thread num
        """
        self.url = url
        self.split_num = 1000
        self.title = None
        self.file_type = None
        self.total_length = None
        self.file_count = 0
        self.extractor = URLExtractor()
        self.video_url, self.title = self.extractor.get_url(url)
        print('title : {}\nvideo_url : {}\n'.format(self.title, self.video_url))

    def split_download(self, queue: Queue):
        """Split download
        :param Queue queue: Queue
        """
        while True:
            num, start, end = queue.get()
            if num is None:
                break
            req = urllib.request.Request(self.video_url)
            req.headers['Range'] = 'bytes=%s-%s' % (start, end)
            while True:
                try:
                    res = urllib.request.urlopen(req)
                    break
                except urllib.error.HTTPError:
                    req.headers.update(self.extractor.headers)
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
            queue.task_done()

    def single_download(self):
        """Single download"""
        def progress(block_count, block_size, total_size):
            percentage = 100.0 * block_count * block_size / total_size
            sys.stdout.write("%.2f %% ( %d KB )\r" % (percentage, total_size / 1024))
        urllib.request.urlretrieve(self.video_url, "{}.mp4".format(self.title), progress)

    def download(self):
        """Download"""
        try:
            info = urllib.request.urlopen(self.video_url).info()
            self.total_length = int(info.get('content-length'))
            self.file_type = info.get('content-type').split('/')[-1]
        except urllib.error.HTTPError:
            req = urllib.request.Request(self.video_url)
            req.headers.update(self.extractor.headers)
            info = urllib.request.urlopen(req).info()
            self.total_length = int(info.get('content-length'))
            self.file_type = info.get('content-type').split('/')[-1]
        except AttributeError:
            print('start single download')
            self.single_download()
            exit()

        queue = Queue()
        total_count = 0
        for i, val in enumerate([(self.total_length + j) // self.split_num for j in range(self.split_num)]):
            if i == 0:
                last = val
                total_count = val
                queue.put((i, 0, last))
            else:
                last = total_count + 1
                total_count += val
                queue.put((i, last, total_count))

        threads = []
        for _ in range(cpu_count()):
            thread = Thread(target=self.split_download, args=(queue,))
            thread.start()
            threads.append(thread)

        queue.join()
        [queue.put((None, None, None)) for _ in range(len(threads))]

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
        """Combine split file
        :param str file_name: file name
        """
        tmp_list = []
        with open("%s.%s" % (file_name, self.file_type), "wb") as file:
            for i in range(self.split_num):
                with open('{}.toyota'.format(i), 'rb') as tmp_file:
                    tmp_list.append(tmp_file.read())
            file.write(b''.join(tmp_list))
        os.system('rm *.toyota')
