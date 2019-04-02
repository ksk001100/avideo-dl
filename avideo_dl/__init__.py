import os
import argparse
from .aa import ascii_moji
from .AVideoDownloader import AVideoDownloader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Specify URL')
    args = parser.parse_args()
    print(ascii_moji['start'] + '\r')
    av = AVideoDownloader(args.url)
    try:
        av.download()
    except KeyboardInterrupt:
        os.system('rm *.toyota')
    print('\n\n{}\n\n'.format(ascii_moji['finish']))


if __name__ == '__main__':
    main()