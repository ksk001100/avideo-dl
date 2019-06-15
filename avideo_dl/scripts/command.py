#!/usr/bin/env python3

import sys
import os.path
import os
import argparse
from avideo_dl.aa import ascii_moji
from avideo_dl.downloader import AVideoDownloader

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Specify URL')
    args = parser.parse_args()
    print(ascii_moji['start'] + '\r')
    av = AVideoDownloader(args.url)
    try:
        file_size = av.download()
    except KeyboardInterrupt:
        os.system('rm *.toyota')
    print('\n\nDownloaded file size: ', file_size, '\n')

if __name__ == '__main__':
    main()
