#!/usr/bin/env python3

import sys
import os.path
import os
import argparse
from avideo_dl.aa import ascii_moji
from avideo_dl.downloader import Downloader
from avideo_dl.extractor import URLExtractor

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Specify URL')
    args = parser.parse_args()
    extractor = URLExtractor(args.url)
    video_url, title = extractor.get_video_url
    print(ascii_moji['start'] + '\r')
    dl = Downloader(video_url, title)
    try:
        file_size = dl.download()
    except KeyboardInterrupt:
        os.system('rm -rf *.tmp')
    print('\n\nDownloaded file size: ', file_size, '\n')

if __name__ == '__main__':
    main()
